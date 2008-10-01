import unittest
from time import sleep

from enfold.gsa import gsa

from Products.COL3 import gsa_config
from Products.COL3.config import DEFAULT_QUERY_COLLECTION
from Products.COL3.testing import COL3FunctionalTestCase
from Products.COL3.content.indexer import index, reindex, unindex
from Products.COL3.content.page import addCOLPage

def search(q, start=0):
    user_query = q
    app = gsa.GSA(gsa_config.GSA_HOST, DEFAULT_QUERY_COLLECTION)
    query = app.createQuery(user_query)
    query.setStartRecord(start)
    return app.query(query, xml=False) # native objects

gsa_test_msg = "GSA testing is disabled, see gsa_config.py"

class GSATest(COL3FunctionalTestCase):

    def afterSetUp(self):
        self._remove = []
        self.setRoles(['Member','Community Member'])
        self.portal.workspaces.invokeFactory("Workspace", "ws") 
        self.workspace = self.portal.workspaces['ws']
        self.library = self.portal.library
        self.portal_gsa = self.portal.portal_gsa

    def beforeTearDown(self):
        for o in self._remove:
            unindex(o)

    def test_setup(self):
        props = self.portal_gsa.getToolProps()
        self.assertEquals(props,
                          dict(gsa_host=gsa_config.GSA_HOST,
                               gsa_feed_port=gsa_config.GSA_FEED_PORT,
                               gsa_feed=gsa_config.GSA_FEED,
                               threshold=100,
                               qenabled=True,
                               qlength=0)
                          )

    def test_index(self):
        ws = self.workspace
        lib = self.library
        id = ws.documents.invokeFactory('COLPage', 'page1.htm')
        page = getattr(ws.documents, 'page1.htm')
        page.setText('Curabitur eros metus, varius quis, fermentum non, ornare eget, arcu.')
        index(page)
        print 'page 1 text = ',page.getText()
        # check if the indexing request was queued
        self.assertEquals(self.portal_gsa._qlength.value, 1)
        url = page.absolute_url()
        qentry = self.portal_gsa._queue[url]
        print 'queued entry 1 body = ',qentry['body']
        assert 'Curabitur' in qentry['body']

        # now add a page with non-ascii characters
        id = lib.invokeFactory('LibraryFile', 'page2uni.doc')
        page2 = getattr(lib, 'page2uni.doc')
        page2.setTitle('Some non-Latin unicode and non-printables \xc3\xa9\x11 to see if we break anything .')
        index(page2)
        print 'page 2 title = ',page2.Title()
        # check if the indexing request was queued
        self.assertEquals(self.portal_gsa._qlength.value, 2)
        url = page2.absolute_url()
        qentry = self.portal_gsa._queue[url]
        print 'queued entry 2 metadata = ',qentry['metadata']
        assert 'non-printables' in qentry['metadata']['Title']

        # add a third page, also with non-ascii characters, for a workspace
        id = ws.documents.invokeFactory('COLPage', 'page3uni.txt')
        page3 = getattr(ws.documents, 'page3uni.txt')
        page3.setText('Méco- Planeacióara la Conservacióe Areas (PCA)')
        index(page3)
        print 'page 3 text = ',page3.getText()
        # check if the indexing request was queued
        self.assertEquals(self.portal_gsa._qlength.value, 3)
        url = page3.absolute_url()
        qentry = self.portal_gsa._queue[url]
        print 'queued entry 3 body = ',qentry['body']
        assert 'Conservacióe Areas ' in qentry['body']

        # and a fourth page for a different workspace
        id = ws.documents.invokeFactory('COLPage', 'page4uni.pdf')
        page4 = getattr(ws.documents, 'page4uni.pdf')
        page4.setTitle(u'Grupo de Trabajo de las Agregaciones reproductivas de la Peníula de YucatáOA')
        index(page4)
        print 'page 4 title = ',page4.Title()
        # check if the indexing request was queued
        self.assertEquals(self.portal_gsa._qlength.value, 4)
        url = page4.absolute_url()
        qentry = self.portal_gsa._queue[url]
        print 'queued entry 4 metadata = ',qentry['metadata']
        try:
          assert str(u'de la Peníula de') in qentry['metadata']['Title']
        except:
          pass

        # test the gsa proper
        assert gsa_config.TESTS_ENABLE, gsa_test_msg
        self.assertEquals(self.portal_gsa.flushQueue(),
                          "Processed 4 item(s)")
        sleep(60*gsa_config.TEST_ASYNCH_WAIT_TIME)
        results = search('Curabitur')
        print len(results), 'search for "Curabitur", should be 1'
        assert len(results) == 1 # search engines != accurate
        self._remove.append(page)
        self._remove.append(page2)

    def test_reindex(self):
        ws = self.workspace
        #id = ws.documents.invokeFactory('Page', 'page2')
        addCOLPage(ws.documents, 'page555.html')
        page = getattr(ws.documents, 'page555.html')
        latin = ('Proin eros massa, sodales quis, nonummy non, rhoncus porta,'
                 ' sapien. Proin nisl lorem, imperdiet non, venenatis sed, '
                 ' volutpat id, eros. Maecenas venenatis')

        assert gsa_config.TESTS_ENABLE, gsa_test_msg
        print len(search('volutpat')) == 0, 'should be 0'
        assert len(search('volutpat')) == 0, 'Should be no results.'
        page.setText(latin)
        index(page)
        sleep(60*gsa_config.TEST_ASYNCH_WAIT_TIME)
        print len(search('volutpat')), 'should be 1'
        assert len(search('volutpat')) == 1, 'Should be one result.'

        page.setText('Proin laoreet felis et mauris')
        print len(search('felis')), 'should be 0'
        assert len(search('felis')) == 0, 'Should be no results'
        reindex(page)
        sleep(60*gsa_config.TEST_ASYNCH_WAIT_TIME)
        print len(search('felis')), 'should be 1'
        assert len(search('felis')) == 1, 'We reindexed w/ this token'

        self._remove.append(page)

    def test_unindex(self):
        ws = self.workspace
        #id = ws.documents.invokeFactory('Page', 'page3')
        addCOLPage(ws.documents, 'page666.css')
        page = getattr(ws.documents, 'page666.css')
        page.setText('Vestibulum ut dui')
        index(page)
        assert gsa_config.TESTS_ENABLE, gsa_test_msg
        sleep(60*gsa_config.TEST_ASYNCH_WAIT_TIME)
        print len(search('Vestibulum')), 'should be 1'
        assert len(search('Vestibulum')) == 1, 'Should be 1 result.'

        unindex(page)
        assert gsa_config.TESTS_ENABLE, gsa_test_msg
        sleep(60*gsa_config.TEST_ASYNCH_WAIT_TIME)
        print len(search('Vestibulum')), 'should be 0'
        assert len(search('Vestibulum')) == 0, 'Should have 0 results'

        self._remove.append(page)

    def test_filter(self):
        """ 
        This workspace, All workspaces, Library and All site
        """
        pass

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GSATest))
    return suite



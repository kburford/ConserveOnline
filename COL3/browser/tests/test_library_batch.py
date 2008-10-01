# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: test_security.py 12505 2007-05-17 16:37:49Z jens $

import unittest

from Acquisition import Implicit
from Testing.makerequest import makerequest
from Products.CMFPlone.utils import _createObjectByType

import Products.COL3.browser.batch
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.library import LibraryByAuthorBatchProvider
from Products.COL3.browser.library import LibraryBySearchtermsBatchProvider
from Products.COL3.browser.library import LibraryViewAllBatchProvider
from Products.COL3.testing import COL3FunctionalTestCase

LibraryByAuthorBatchFragment = BatchFragmentFactory(LibraryByAuthorBatchProvider)
LibraryBySearchtermsBatchFragment = BatchFragmentFactory(LibraryBySearchtermsBatchProvider)
LibraryViewAllBatchFragment = BatchFragmentFactory(LibraryViewAllBatchProvider)

def make_author_content(context):
    context.invokeFactory('LibraryFile', id='test-file-1', title='test file 1')
    context['test-file-1'].update(authors=['Magoo, Mister'])
    context.invokeFactory('LibraryFile', id='test-file-2', title='test file 2')
    context['test-file-2'].update(authors=['Montana, Moe'])
    context.invokeFactory('LibraryFile', id='test-file-3', title='test file 3')
    context['test-file-3'].update(authors=['McDonald, Old', 'McDonald, Ronald'])
    context.invokeFactory('LibraryFile', id='test-file-4', title='test file 4')
    context['test-file-4'].update(authors=['Magoo, Mister', 'Woodpecker, Woody'])
    context.invokeFactory('LibraryFile', id='test-file-5', title='test file 5')
    context['test-file-5'].update(authors=['Nozzle, Bastian'])
    context.invokeFactory('LibraryFile', id='test-file-6', title='test file 6')
    context['test-file-6'].update(authors=['Hammond, Fred', 'Hammond, Mark'])

def make_keyword_content(context):
    context.invokeFactory('LibraryFile', id='test-file-1', title='test file 1')
    context['test-file-1'].update(keywords=['Mustard'])
    context.invokeFactory('LibraryFile', id='test-file-2', title='test file 2')
    context['test-file-2'].update(keywords=['Salami', 'Ham'])
    context.invokeFactory('LibraryFile', id='test-file-3', title='test file 3')
    context['test-file-3'].update(keywords=['Honey Mustard', 'Cheese'])
    context.invokeFactory('LibraryFile', id='test-file-4', title='test file 4')
    context['test-file-4'].update(keywords=['Pepper', 'Ham'])
    context.invokeFactory('LibraryFile', id='test-file-5', title='test file 5')
    context['test-file-5'].update(keywords=['Catchup', 'Cheese'])
    context.invokeFactory('LibraryFile', id='test-file-6', title='test file 6')
    context['test-file-6'].update(keywords=['Spam', 'Ham'])

class LibraryByAuthorBatchTest(COL3FunctionalTestCase):

    def testBatchAsElement(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_author_content(self.portal.library)

        batch = LibraryByAuthorBatchFragment(self.portal.library, request)

        # Assert asElement doesn't blow up.
        request['startswith'] = 'H'
        self.failUnless(batch.asElement())

    def testByAuthorFilterStartsWith(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_author_content(self.portal.library)

        batch = LibraryByAuthorBatchFragment(self.portal.library, request)
        provider = batch.provider(self.portal.library, request)

        request['startswith'] = 'H'
        results = provider.query({'start': 0, 'end': 2})

        info = batch.info({'start': 0, 'end': 2,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 2)
        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 2)

    def testByAuthorFilterStartsWithBiggerThanBatch(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_author_content(self.portal.library)

        batch = LibraryByAuthorBatchFragment(self.portal.library, request)
        provider = batch.provider(self.portal.library, request)

        request['startswith'] = 'M'
        results = provider.query({'start': 0, 'end': 2})

        info = batch.info({'start': 0, 'end': 2,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 4)
        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 2)

    def testBatchFragmentInfo(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_author_content(self.portal.library)

        batch = LibraryByAuthorBatchFragment(self.portal.library, request)
        provider = batch.provider(self.portal.library, request)

        # 'end' fetch at least 10 items, if they are available.
        results = provider.query({'start': 0, 'end': 10})

        info = batch.info({'start': 0, 'end': 2,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 8)
        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 2)

        self.assertEquals(len(info['pages']), 4)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], True)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], False)

        self.assertEquals(info['pages'][2]['url'], 'http://nohost?start:int=4&sze:int=2')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failIf(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['next']['url'], 'http://nohost?start:int=2&sze:int=2')

        # Now move it to the second batch and do it all over again
        info = batch.info({'start': 2, 'end': 4,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 8)
        self.assertEquals(info['start'], 3)
        self.assertEquals(info['end'], 4)

        self.assertEquals(len(info['pages']), 4)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], False)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], True)

        self.assertEquals(info['pages'][2]['url'], 'http://nohost?start:int=4&sze:int=2')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failUnless(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['prev']['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['next']['url'], 'http://nohost?start:int=4&sze:int=2')


class LibraryBySearchtermsBatchTest(COL3FunctionalTestCase):

    def testBatchAsElement(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_keyword_content(self.portal.library)

        batch = LibraryBySearchtermsBatchFragment(self.portal.library, request)
        self.failUnless(batch.asElement())

    def testBatchFragmentInfo(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_keyword_content(self.portal.library)

        batch = LibraryBySearchtermsBatchFragment(self.portal.library, request)
        provider = batch.provider(self.portal.library, request)

        # 'end' fetch at least 10 items, if they are available.
        results = provider.query({'start': 0, 'end': 10})

        info = batch.info({'start': 0, 'end': 2,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 8)
        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 2)

        self.assertEquals(len(info['pages']), 4)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], True)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], False)

        self.assertEquals(info['pages'][2]['url'], 'http://nohost?start:int=4&sze:int=2')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failIf(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['next']['url'], 'http://nohost?start:int=2&sze:int=2')

        # Now move it to the second batch and do it all over again
        info = batch.info({'start': 2, 'end': 4,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 8)
        self.assertEquals(info['start'], 3)
        self.assertEquals(info['end'], 4)

        self.assertEquals(len(info['pages']), 4)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], False)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], True)

        self.assertEquals(info['pages'][2]['url'], 'http://nohost?start:int=4&sze:int=2')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failUnless(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['prev']['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['next']['url'], 'http://nohost?start:int=4&sze:int=2')


class LibraryViewAllBatchTest(COL3FunctionalTestCase):

    def testBatchAsElement(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_keyword_content(self.portal.library)

        request['startswith'] = 'T'
        batch = LibraryViewAllBatchFragment(self.portal.library, request)
        self.failUnless(batch.asElement())


class LibraryCatalogsTest(COL3FunctionalTestCase):

    def testLibraryFilePresentInBothCatalogs(self):
        obj = _createObjectByType('LibraryFile', self.portal.library, 'foo')

        # Make sure the object is indexed by portal_catalog...
        results = self.portal.portal_catalog(portal_type='LibraryFile')
        self.failUnlessEqual(len(results), 1)
        self.failUnlessEqual(results[0].getObject(), obj)

        # ...and also by the notification_catalog
        results = self.portal.notification_catalog()
        self.failUnlessEqual(len(results), 1)
        self.failUnlessEqual(results[0].getObject(), obj)

    def testColFilePresentInBothCatalogs(self):
        obj = _createObjectByType('COLFile', self.portal.library, 'foo')

        # Make sure the object is indexed by portal_catalog...
        results = self.portal.portal_catalog(portal_type='COLFile')
        self.failUnlessEqual(len(results), 1)
        self.failUnlessEqual(results[0].getObject(), obj)

        # ...and also by the notification_catalog
        results = self.portal.notification_catalog()
        self.failUnlessEqual(len(results), 1)
        self.failUnlessEqual(results[0].getObject(), obj)

    def testColPagePresentInBothCatalogs(self):
        obj = _createObjectByType('COLPage', self.portal.library, 'foo')

        # Make sure the object is indexed by portal_catalog...
        results = self.portal.portal_catalog(portal_type='COLPage')
        self.failUnlessEqual(len(results), 1)
        self.failUnlessEqual(results[0].getObject(), obj)

        # ...and also by the notification_catalog
        results = self.portal.notification_catalog()
        self.failUnlessEqual(len(results), 1)
        self.failUnlessEqual(results[0].getObject(), obj)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LibraryByAuthorBatchTest))
    suite.addTest(unittest.makeSuite(LibraryBySearchtermsBatchTest))
    suite.addTest(unittest.makeSuite(LibraryViewAllBatchTest))
    suite.addTest(unittest.makeSuite(LibraryCatalogsTest))
    return suite


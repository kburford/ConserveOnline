import unittest

from Products.ZCatalog.ZCatalog import manage_addZCatalog

from Products.COL3.testing import COL3FunctionalTestCase
from Products.COL3.tests.utils import make_request

from Products.COL3.content.label import Label, Labeller
from Products.COL3.content.file import COLFile as File

"""

  >>> self.setRoles(['Member','Community Member'])
  >>> app.plone.workspaces.invokeFactory("Workspace", "ws") and None
  >>> workspace = app.plone.workspaces['ws']
  >>> self.login()

"""

class SpikeSolutionTest(COL3FunctionalTestCase):
    
    def afterSetUp(self):
        self.setRoles(['Member','Community Member'])
        self.portal.workspaces.invokeFactory("Workspace", "ws") and None
        self.workspace = self.portal.workspaces['ws']
        
        # Add catalog per Workspace
        manage_addZCatalog(self.workspace, 'ws_catalog', 'Label Catalog')
        cat = self.workspace.ws_catalog
        
        #add search indexes
        cat.addIndex('public_count', 'FieldIndex')
        cat.addIndex('total_count', 'FieldIndex')
        cat.addIndex('is_private', 'FieldIndex')
        cat.addIndex('meta_type', 'FieldIndex')
        cat.addIndex('primarylabel', 'FieldIndex')
        cat.addIndex('otherlabels', 'KeywordIndex')
        
        # Add metadata so we can see in brains
        cat.addColumn('metadata1')
        cat.addColumn('metadata2')
        cat.addColumn('metadata3')
        cat.addColumn('metadata4')
        cat.addColumn('metadata5')
        cat.addColumn('public_count')
        cat.addColumn('total_count')
        cat.addColumn('is_private')
        cat.addColumn('id')
        cat.addColumn('meta_type')
        cat.addColumn('title')
        cat.addColumn('primarylabel')
        cat.addColumn('otherlabels')
        
        #self.setRoles(['Manager', 'Owner'])
        
        f1 = File('f1', title='File 1')
        f2 = File('f2', title='File 2')
        f3 = File('f3', title='File 3')
        self.workspace.documents._setOb('f1', f1)
        self.workspace.documents._setOb('f2', f2)
        self.workspace.documents._setOb('f3', f3)
        
        attrs = ['metadata1', 
                 'metadata2',
                 'metadata3',
                 'metadata4',
                 'metadata5',]
        
        l1 = Label('l1', title='Label 1')
        l2 = Label('l2', title='Label 2')
        l3 = Label('l3', title='Label 3')
        
        l4 = Label('x4', title='Label 4')
        l5 = Label('x5', title='Label 5')
        l6 = Label('x6', title='Label 6')
        
        for attr in attrs:
            setattr(l1,attr,attr.upper())
        self.workspace.labels._setOb('l1', l1)
        for attr in attrs:
            setattr(l2,attr,attr.upper())
        self.workspace.labels._setOb('l2', l2)
        for attr in attrs:
            setattr(l3,attr,attr.upper())
        self.workspace.labels._setOb('l3', l3)
        for attr in attrs:
            setattr(l4,attr,attr.upper())
        self.workspace.labels._setOb('x4', l4)
        for attr in attrs:
            setattr(l5,attr,attr.upper())
        self.workspace.labels._setOb('x5', l5)
        for attr in attrs:
            setattr(l6,attr,attr.upper())
        self.workspace.labels._setOb('x6', l6)
        self.request = make_request()
        self.labeller = Labeller(self.workspace)
        #self.login()
    
    def testLabelCode(self):
        labeller = self.labeller
        docs = self.workspace.documents
        labels = self.workspace.labels
        
        f1 = docs.f1
        f2 = docs.f2
        
        l1 = labels.l1
        l2 = labels.l2
        l3 = labels.l3
        l4 = labels.x4
        l5 = labels.x5
        l6 = labels.x6
        
        labeller.addPrimaryLabel(f1, l1)
        assert labeller.getPrimaryLabelFor(f1) == u'l1'
        
        labeller.addPrimaryLabel(f2, l2)
        assert labeller.getPrimaryLabelFor(f2) == u'l2'
        
        metadata1 = f1.getMetadata1()
        assert metadata1 == 'METADATA1'
        metadata2 = f1.getMetadata2()
        assert metadata2 == 'METADATA2'
        metadata3 = f1.getMetadata3()
        assert metadata3 == 'METADATA3'
        metadata4 = f1.getMetadata4()
        assert metadata4 == 'METADATA4'
        metadata5 = f1.getMetadata5()
        assert metadata5 == 'METADATA5'
        
        labeller.addSecondaryLabels(f1, l2, l3)
        assert len(labeller.getSecondaryLabels(f1)) == 2
        labeller.addSecondaryLabels(f2, l1, l4, l5, l6)
        assert len(labeller.getSecondaryLabels(f2)) == 4
        
        all_labels = labeller.getLabelsFor(f2)
        all_labels = (all_labels['primary'],) + all_labels['secondary']
        assert all_labels == (u'l2',u'l1', u'x4', u'x5', u'x6')
        
        label_list = labeller.listLabels()
        labelids = ['l1','l2','l3','x4','x5','x6']
        for label in label_list:
            assert label['href'][len(label['href'])-2:] in labelids
        label_list = labeller.listLabels(startswith='x')
        for label in label_list:
            assert label['href'][len(label['href'])-2:] in ['x4','x5','x6']
        
        docs = labeller.listContentByLabel('l1')
        assert len(docs) == 2
        
        labeller.delLabel(f2, 'x6')
        assert len(labeller.getSecondaryLabels(f2)) == 3
        
def test_suite():
    #from zope.testing.doctest import DocTestSuite
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(SpikeSolutionTest))
    return suite

import unittest
from Products.COL3.testing import COL3FunctionalTestCase
from Products.CMFPlone.utils import _createObjectByType


class SetupTest(COL3FunctionalTestCase):

    def test_site_structure_created_after_install(self):
        expected = {
            'workspaces': 'Workspaces Container',
            'library': 'Large Plone Folder',
            'about': 'Large Plone Folder',
            'subscriptions': 'Large Plone Folder',
        }
        for content, portal_type in expected.items():
            self.failUnless(content in self.portal.objectIds())
            self.failUnless(self.portal[content].portal_type, portal_type)

    def test_content_isnt_purged_on_reinstall(self):
        self.setRoles(['Manager'])
        # Create some initial content
        _createObjectByType('LibraryFile', self.portal.library, 'lf')
        _createObjectByType('Workspace', self.portal.workspaces, 'ws')
        _createObjectByType('Document', self.portal.about, 'doc')
        _createObjectByType('Folder', self.portal.subscriptions, 'folder')
        # Reinstall COL3
        self.portal.portal_quickinstaller.reinstallProducts(['COL3'])
        # The existing content should still be there
        self.failUnless('lf' in self.portal.library.objectIds())
        self.failUnless('ws' in self.portal.workspaces.objectIds())
        self.failUnless('doc' in self.portal.about.objectIds())
        self.failUnless('folder' in self.portal.subscriptions.objectIds())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SetupTest))
    return suite

# COL3
# Copyright(C), 2007, Enfold Systems, Inc. - ALL RIGHTS RESERVED
#
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied
# this software.  Any inquiries concerning the scope or
# enforceability of the license should be addressed to:
#
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope import interface

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View

from Products.Archetypes.public import * #@UnusedWildImport
from Products.ATContentTypes.content.folder import ATBTreeFolder

from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.interfaces.workspace import IWorkspaceNeedsSetup
from Products.COL3.interfaces.workspace import IWorkspaceDocumentsFolder
from Products.COL3.interfaces.workspace import IWorkspaceCalendar
from Products.COL3.interfaces.workspace import IWorkspaceMembers
from Products.COL3.content.base import IsPrivateMixin
from Products.COL3.content.base import Taxonomy

def addWorkspace(self, id, title='', description=''):
    """ Create a new workgroup
    """
    wg = Workspace(id, title=title, description=description)
    self._setObject(id, wg)

class Workspace(ATBTreeFolder, Taxonomy, IsPrivateMixin):
    """ The COL3 workgroup
    """
    security = ClassSecurityInfo()
    workspaceschema = Schema((
        StringField('title'),
        TextField('content',
                  widget=RichWidget(label='Content')),
        StringField('language'),
        StringField('license'),
    ))

    archetype_name = portal_type = meta_type = 'Workspace'
    schema = (ATBTreeFolder.schema.copy() + #@UndefinedVariable
              IsPrivateMixin.schema.copy() + #@UndefinedVariable
              Taxonomy.schema.copy() + #@UndefinedVariable
              workspaceschema)

    interface.implements(IWorkspace)

    def _setupWorkspaceContent(self):
        # create area for documents and pages
        self.invokeFactory("Large Plone Folder", "documents")
        self['documents'].update(title="Files & Pages",
                                 description="Repository for workspace files and pages")
        interface.directlyProvides(self['documents'], IWorkspaceDocumentsFolder)
        # create area for events
        self.invokeFactory("Large Plone Folder", "calendar")
        self['calendar'].update(title="Calendar",
                                description="Repository for workspace events")
        interface.directlyProvides(self['calendar'], IWorkspaceCalendar)
        self.invokeFactory("Large Plone Folder", "wsmembers")
        self['wsmembers'].update(title="Members",
                                description="Somehing to register list members view against")
        interface.directlyProvides(self['wsmembers'], IWorkspaceMembers)
        # create discussion board
        self.invokeFactory("PloneboardForum", "discussion")
        self['discussion'].update(title="Discussions",
                                  description="Workspace area for discussions among members")
        self.invokeFactory("Image", "workspacelogo")
        self['workspacelogo'].update(title='Workspace Logo',
                            description="A unique image to identify your workspace")
        self.invokeFactory("Image", "workspaceicon")
        self['workspaceicon'].update(title='Workspace Icon',
                            description="A unique icon to identify your workspace")

    def _setupWorkspaceSecurity(self):
        IWorkspaceMemberManagement(self).setUp()

    security.declareProtected(View, 'getWorkspaceCountry')
    def getWorkspaceCountry(self):
        """ Only return country if inside the Workspaces
        """
        if 'workspaces' in self.getPhysicalPath():
            return self.getCountry()
        return None


registerType(Workspace)

def markWorkspaceNeedsSetup(ob, event):
    """ Mark workspace as needing set-up """
    # We can't set-up the workspace directly at the objectAddedEvent since CMF
    # setup of the object is not finished yet. So we mark it with an interface
    # to be removed when the object is set-up for real.
    # With this we can subscribe to this interface and IAfterTransitionEvent
    # which will remove this interface so it doesn't match on other workspace
    # transitions than the first
    interface.directlyProvides(ob, IWorkspaceNeedsSetup)

def finishWorkspaceSetup(ob, event):
    IWorkspaceMemberManagement(ob).setUp()
    ob._setupWorkspaceContent()
    interface.noLongerProvides(ob, IWorkspaceNeedsSetup)

def tearDownWorkspaceSetup(ob, event):
    IWorkspaceMemberManagement(ob).tearDown()

def workspaceEventPrinter(ob, event):
    evIfs = list(interface.providedBy(event))
    print "/".join(ob.getPhysicalPath()), ob.__dict__.get('portal_type','unset'), evIfs

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

import logging, random
from zope.component import getSiteManager
from Acquisition import aq_inner
from smtplib import SMTPRecipientsRefused
from zope import interface
from Globals import InitializeClass
from AccessControl.SecurityInfo import ClassSecurityInfo
from datetime import datetime
from DateTime.DateTime import DateTime
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.utils import SimpleItemWithProperties

from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.interfaces.tools import IInvitationManager
from Products.COL3.interfaces.tools import IInvitation
from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3 import config

logger = logging.getLogger('Products.COL3.tools')

CATALOG_ID = '.invitationCatalog'

valid = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

def generate_key():
    return ''.join([random.choice(valid) for i in range(6)]) #@UnusedVariable

class InvitationsTool(UniqueObject, BTreeFolder2):
    
    interface.implements(IInvitationManager)
    id = 'workspace_invitations'
    meta_type = 'ConserveOnline Invitation Tool'

    security = ClassSecurityInfo()

    def _setupCatalog(self):
        c = ZCatalog(id=CATALOG_ID, title="Invitation Catalog")
        self._setOb(CATALOG_ID, c)
        c = self[CATALOG_ID]
        c.addIndex('getId', 'FieldIndex')
        c.addIndex('workspaceID', 'FieldIndex')
        c.addIndex('email', 'FieldIndex')
    
    def _getCatalog(self):
        return self[CATALOG_ID]

    security.declarePrivate('searchResults')
    def searchResults(self, *args, **kw):
        return self._getCatalog().searchResults(*args, **kw)

    security.declarePrivate('getInvitationsForWorkspace')
    def getInvitationsForWorkspace(self, workspace):
        for result in self.searchResults(workspaceID=workspace.getId()):
            yield result.getObject()

    security.declarePrivate('getInvitationsForEmail')
    def getInvitationsForEmail(self, email):
        for result in self.searchResults(email=email):
            yield result.getObject()

    security.declarePrivate('getInvitationById')
    def getInvitationById(self, invitationID):
        return self[invitationID]

    def _generateInvitationId(self):
        ids = self.objectIds()
        while True:
            timestamp = datetime.now().isoformat('_').replace(':','-')
            invitationID = timestamp + '-' + generate_key()
            if invitationID not in ids:
                return invitationID

    security.declarePrivate('inviteToWorkspace')
    def inviteToWorkspace(self, workspace, emails):
        wID = workspace.getId()
        pm = getToolByName(workspace, 'portal_membership')
        inviterID = pm.getAuthenticatedMember().getId()
        invitationIDs = []
        for email in emails:
            invitationID = self._generateInvitationId()
            invitation = Invitation(invitationID, wID, inviterID, email)
            self._setObject(invitationID, invitation)
            self.mailInvitationById(invitationID)
            invitationIDs.append(invitationID)
        return invitationIDs

    security.declarePrivate('getInviterFor')
    def getInviterFor(self, invitation):
        invtool = getToolByName(self, 'portal_membership')
        return invtool.getMemberById(invitation.inviterID)

    security.declarePrivate('getWorkspaceFor')
    def getWorkspaceFor(self, invitation):
        # XXX parameterize the workspace container name
        return self.aq_parent.workspaces[invitation.workspaceID]

    security.declarePrivate('mailInvitationById')
    def mailInvitationById(self, invitationID):
        invitation = self[invitationID]
        mailhost = getToolByName(self, 'MailHost')

        # using the workspace itself instead of a catalog brain shouldn't be
        # a problem, as it'll be in cache anyway since the user will probably
        # be looking at a view of it when this method get's called

        membership = getToolByName(self, 'portal_membership')
        sender = membership.getMemberById(invitation.inviterID)

        workspace = self.getWorkspaceFor(invitation)
        # url will be different if e-mail already in the system or not
        portal = getSiteManager()
        purl = portal.absolute_url()
        if purl.find('/Plone') != -1:
            purl = purl[:purl.find('/Plone')]
        if list(membership.searchForMembers(email=invitation.email)):
            url_pattern = '%s/accept-invitation.html?id=%s'
        else:
            url_pattern = '%s/register-invite.html?invitationid=%s'

        accept_url = url_pattern % (purl, invitation.getId())

        invitation_info = {}
        invitation_info['invitation_url'] = accept_url
        invitation_info['workspace_name'] = workspace.Title()
        invitation_info['workspace_overview'] = workspace.Description()
        invitation_info['workspace_manager'] = sender.getId()
        invitation_info['username'] = invitation.email
        invitation_info['title'] = invitation.email
        body = config.INVITATION_EMAIL_BODY % invitation_info
        subject = config.INVITATION_EMAIL_SUBJECT % invitation_info

        # mfrom = sender.getProperty('email')

        mfrom = config.NOREPLY_SENDER_ADDRESS
        mto = invitation.email
        try:
            mailhost.secureSend(body, mto=mto, mfrom=mfrom, subject=subject)
        except SMTPRecipientsRefused:
            logger.info('Failed to send invitation for '+mto)
        invitation.lastSent = DateTime()

    security.declarePrivate('cancelInvitationsById')
    def cancelInvitationsById(self, invitationIds):
        invalidIds = []
        for invId in invitationIds:
            try:
                invitation = self[invId]
                self._delObject(invId)
                workspace = self.getWorkspaceFor(invitation) 
                smt = simple_mail_tool()
                try:
                    smt.sendEmailRejection(workspace, invitation.email)
                except SMTPRecipientsRefused:
                    pass #XXX the email address is invalid, figure out what to do
                # the object pre-removal subscribers should do the rest of the
                # invitation cancelation dance
            except KeyError:
                # BTreeFolders raise KeyError if the object doesn't exist
                invalidIds.append(invId)
        return invalidIds

    def acceptInvitation(self, invId, member):
        """ Handles adding a workspace memeber form the accept invitation page"""
        invalidIds = []
        try:
            invitation = self[invId]
            workspace = self.getWorkspaceFor(invitation) 
            self._delObject(invId)
            IWorkspaceMemberManagement(workspace).addMember(member)
        except KeyError:
            # BTreeFolders raise KeyError if the object doesn't exist
            invalidIds.append(invId)
        return invalidIds
            
        
    security.declarePrivate('cancelInvitation')
    def rejectInvitation(self, invId):
        """ Handles cancelling a single invitation request from the accept invitation page"""
        invalidIds = []
        try:
            invitation = self[invId]
            inviterId = invitation.get('inviterID', None)
            self._delObject(invId)
            workspace = self.getWorkspaceFor(invitation) 
            smt = simple_mail_tool()
            try:
                managerlist = IWorkspaceMemberManagement(workspace).listManagerMembers()
                for manager in managerlist:
                    if manager.getId() == inviterId:
                        smt.sendInvitationRejection(workspace, manager.getProperty('email'))
            except SMTPRecipientsRefused:
                pass #XXX the email address is invalid, figure out what to do
            # the object pre-removal subscribers should do the rest of the
            # invitation cancelation dance
        except KeyError:
            # BTreeFolders raise KeyError if the object doesn't exist
            invalidIds.append(invId)
        return invalidIds

    security.declarePrivate('reSendInvitationsById')
    def reSendInvitationsById(self, invitationIds):
        invalidIds = []
        for invId in invitationIds:
            try:
                self.mailInvitationById(invId)
            except KeyError:
                # BTreeFolders raise KeyError if the object doesn't exist
                invalidIds.append(invId)
        return invalidIds

InitializeClass(InvitationsTool)

def invitationManagerAddedHandler(ob, event): #@UnusedVariable
    """Finish configuration of the invitation tool."""
    ob._setupCatalog()

class Invitation(SimpleItemWithProperties):

    interface.implements(IInvitation)

    _properties = (
                   dict(id='workspaceID', type='string', mode='w'),
                   dict(id='inviterID', type='string', mode='w'),
                   dict(id='email', type='string', mode='w'),
                   dict(id='lastSent', type='date', mode='w'),
                  )
    
    def __init__(self, id, workspaceID, inviterID, email):
        self.id = id
        self.workspaceID = workspaceID
        self.inviterID = inviterID
        self.email = email
        self.lastSent = None
        # will get a proper lastSent date on InvitationsTool.mailInvitation()

def invitationAddedHandler(ob, event): #@UnusedVariable
    """Handle invitation adding: catalog it."""
    uid = '/'.join(ob.getPhysicalPath())
    ob.aq_inner.aq_parent._getCatalog().catalog_object(ob, uid)

def invitationWillBeRemovedHandler(ob, event): #@UnusedVariable
    """Handle invitation removal: uncatalog it."""
    uid = '/'.join(ob.getPhysicalPath())
    ob.aq_inner.aq_parent._getCatalog().uncatalog_object(uid)


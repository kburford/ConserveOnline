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

import logging

from zope import interface
from Globals import InitializeClass
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from smtplib import SMTPRecipientsRefused
from Products.ZCatalog.ZCatalog import ZCatalog
from Products.CMFCore.utils import SimpleItemWithProperties
from Products.CMFCore.utils import getToolByName
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2
from datetime import datetime
from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.interfaces import IJoinRequestsManager
from Products.COL3.exceptions import JoinRequestAlreadySubmited
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.exceptions import AlreadyWorkspaceMember
from Products.COL3.interfaces.tools import IJoinRequest
import random

CATALOG_ID = '.joinRequestsCatalog'

valid = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

def generate_key():
    return ''.join([random.choice(valid) for i in range(6)]) #@UnusedVariable

class JoinRequestsTool(UniqueObject, BTreeFolder2):
    
    logger = logging.getLogger('Products.COL3.browser')
    
    interface.implements(IJoinRequestsManager)

    id = 'workspace_join_requests'
    meta_type = 'ConserveOnline Join Requests Tool'

    security = ClassSecurityInfo()

    def _setupCatalog(self):
        c = ZCatalog(id=CATALOG_ID, title="Join Requests Catalog")
        self._setOb(CATALOG_ID, c)
        c = self[CATALOG_ID]
        c.addIndex('getId', 'FieldIndex')
        c.addIndex('workspaceID', 'FieldIndex')
        c.addIndex('memberID', 'FieldIndex')
    
    def _getCatalog(self):
        return self[CATALOG_ID]

    security.declarePrivate('searchResults')
    def searchResults(self, *args, **kw):
        return self._getCatalog().searchResults(*args, **kw)

    security.declarePrivate('getJoinRequestsForWorkspace')
    def getJoinRequestsForWorkspace(self, workspace):
        for result in self.searchResults(workspaceID=workspace.getId()):
            yield result.getObject()

    security.declarePrivate('getJoinRequestForMemberAndWorkspace')
    def getJoinRequestForWorkspaceIDAndMemberID(self, workspaceID, memberID):
        for result in self.searchResults(memberID=memberID,
                                         workspaceID=workspaceID):
            return result.getObject()
        return None

    def _generateJoinRequestId(self):
        ids = self.objectIds()
        while True:
            timestamp = datetime.now().isoformat('_').replace(':','-')
            objId = timestamp + '-' + generate_key()
            if objId not in ids:
                return objId

    security.declarePrivate('addJoinRequest')
    def addJoinRequest(self, workspace, reason):
        pm = getToolByName(workspace, 'portal_membership')
        member = pm.getAuthenticatedMember()
        self.checkJoinRequest(workspace, member)
        jrID = self._generateJoinRequestId()
        joinRequest = JoinRequest(jrID, workspace.getId(), member.getId(),
                                  reason)
        self._setObject(jrID, joinRequest)
        self.notifyWorkspaceManagers(workspace, member)
        return jrID

    security.declarePrivate('notifyWorkspaceManagers')
    def notifyWorkspaceManagers(self, workspace, member):
        wm = IWorkspaceMemberManagement(workspace)
        smt = simple_mail_tool()
        for manager in wm.listManagerMembers():
            smt.sendJoinRequestNotification(workspace, manager.getProperty('email'))

    def _getWorkspaceFor(self, joinRequest):
        # XXX parameterize the workspace container name
        return self.aq_parent.workspaces[joinRequest.workspaceID]

    security.declarePrivate('cancelJoinRequestsById')
    def cancelJoinRequestsById(self, joinRequestIds):
        invalidIds = []
        for jrId in joinRequestIds:
            try:
                joinRequest = self[jrId]
                self._delObject(jrId)
                workspace = self._getWorkspaceFor(joinRequest) 
                pm = getToolByName(workspace, 'portal_membership')
                member = pm.getMemberById(joinRequest.memberID)
                smt = simple_mail_tool()
                try:
                    smt.sendEmailRejection(workspace, member.getProperty('email'))
                except SMTPRecipientsRefused:
                    pass #XXX the email address is invalid, figure out what to do
                # the object pre-removal subscribers should do the rest of the
                # cancelation dance
            except KeyError:
                # BTreeFolders raise KeyError if the object doesn't exist
                invalidIds.append(jrId)
        return invalidIds

    def checkJoinRequest(self, workspace, member):
        memberID = member.getId()
        # check if join-request already exists
        if self.getJoinRequestForWorkspaceIDAndMemberID(workspace.getId(),
                                                        memberID) is not None:
            raise JoinRequestAlreadySubmited(memberID)
        # check if member is not already in the workspace        
        wm = IWorkspaceMemberManagement(workspace)
        if memberID in wm.listManagerMemberIds():
            raise AlreadyWorkspaceMember(memberID)

    security.declarePrivate('acceptJoinRequestsById')
    def acceptJoinRequestsById(self, joinRequestIds):
        invalidIds = []
        for jrId in joinRequestIds:
            try:
                joinRequest = self[jrId]
            except KeyError:
                # BTreeFolders raise KeyError if the object doesn't exist
                invalidIds.append(jrId)
            else:
                ws = self._getWorkspaceFor(joinRequest)
                wm = IWorkspaceMemberManagement(ws)
                wm.addMemberByID(joinRequest.memberID)
                self._delObject(jrId)
                ##send an email
                pm = getToolByName(ws, 'portal_membership')
                member = pm.getMemberById(joinRequest.memberID)
                smt = simple_mail_tool()
                try:
                    smt.sendEmailAcceptance(ws, member.getProperty('email'))
                except SMTPRecipientsRefused:
                    logger.info('Email was not able to be processed for address (if blank, no address for the user found)... '+member.getProperty('email'))
        return invalidIds


InitializeClass(JoinRequestsTool)

def joinRequestsManagerAddedHandler(ob, event):
    """Finish configuration of the join-request tool."""
    ob._setupCatalog()

class JoinRequest(SimpleItemWithProperties):

    interface.implements(IJoinRequest)
    
    _properties = (
                   dict(id='workspaceID', type='string', mode='w'),
                   dict(id='memberID', type='string', mode='w'),
                  )

    reason = None # the reason given for joining this workspace

    def __init__(self, id, workspaceID, memberID, reason):
        self.id = id
        self.workspaceID = workspaceID
        self.memberID = memberID
        self.reason = reason

def joinRequestAddedHandler(ob, event):
    """Handle join-request adding: catalog it."""
    uid = '/'.join(ob.getPhysicalPath())
    ob.aq_inner.aq_parent._getCatalog().catalog_object(ob, uid)

def joinRequestWillBeRemovedHandler(ob, event):
    """Handle join-request removal: uncatalog it."""
    uid = '/'.join(ob.getPhysicalPath())
    ob.aq_inner.aq_parent._getCatalog().uncatalog_object(uid)


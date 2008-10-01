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

from os.path import join
import tempfile
from smtplib import SMTPRecipientsRefused

from zope import schema, interface, component
from zope.formlib import form
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_inner, aq_parent

from Products.CMFCore import utils as cmfutils
from Products.Five.formlib.formbase import FormBase
from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.content.indexer import index as gsa_index
from Products.COL3 import config
from Products.COL3.etree import Element, SubElement
from Products.COL3.etree import tostring
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.interfaces.workspace import IInviteByEmailSchema
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagementSchema
from Products.COL3.interfaces.workspace import ICancelInvitationSchema
from Products.COL3.interfaces.workspace import IReSendInvitationSchema
from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.base import XMLView
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.formlib import xmlform, schema as colschema
from Products.COL3.validators import check_email
from Products.COL3.browser.utils import toStringWithPreamble
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.interfaces.workspace import IWorkspace
from Products.CMFCore.utils import getToolByName
from zope.interface.interface import invariant
from Products.COL3.validators import validateWorkspaceTitle

class WorkspaceCreationView(Fragment):
    """ View class for workspace add views
    """

    def asElement(self):
        # <view name="add.html" type="workspace" section="workspaces"
        #       title="Create a Workspace"/>

        view_node = Element('view', type="workspace",
                            name="add.html",
                            section="workspaces",
                            title="Create a Workspace")
        return view_node

class WorkspaceCreationForm(xmlform.FormFragment):

    class form_schema(interface.Interface):
        title = schema.TextLine(
            title=u'Workspace Name (up to 50 characters)',
            description=u"""Examples: Colorado Federal Public Lands Strategy, Western State Trust """
            u"""Lands, Kenya's Biodiversity Mapping Project.""",
            max_length=50,
            required=True,
            constraint=validateWorkspaceTitle)
        id = colschema.SubdomainField(
            title=u'Web Site Address (up to 25 characters)',
            description=u'A shorter name is better for your web site address. Example: If your '
            'workspace is called Colorado Federal Public Lands, your web site address might '
            'be "copubliclands". The full URL for the workspace would then be '
            'http://conserveonline.org/workspaces/copubliclands.',
            required=True)
        description = schema.Text(
            title=u'What is the purpose, goal, or mission statement for your workspace? (up to 250 characters)',
            description=u"This description will appear on the home page of your workspace",
            max_length=250,
            required=False)
        country = colschema.VocabularyChoice(
            vocabulary=config.NATIONS,
            default=config.NATIONS_DEFAULT,
            title=u"What region or country is your work based in?",
            required=True)
        biogeographic_realm = colschema.VocabularyChoice(
            vocabulary=config.BIOGEOGRAPHIC_REALMS,
            default=config.BIO_REALMS_DEFAULT,
            title=u"What biogeographic realm is your work based in?",
            required=True)
        habitat = colschema.ChoiceSet(
            title=u'Habitat type',
            vocabulary=config.HABITAT_VOCABULARY,
            required=False)
        conservation = colschema.ChoiceSet(
            title=u'Conservation action',
            vocabulary=config.CONSERVATION_VOCABULARY,
            required=False)
        directthreat = colschema.ChoiceSet(
            title=u'Direct threat',
            vocabulary=config.DIRECT_THREAT_VOCABULARY,
            required=False)
        monitoring = colschema.ChoiceSet(
            title=u'Monitoring type',
            vocabulary=config.MONITORING_VOCABULARY,
            description=u'The methods used to determine whether the conservation actions described in this document are succeeding',
            required=False)
        organization = schema.TextLine(
            title=u"Organization",
            description=u"Examples: The Nature Conservancy, World Wildlife Fund, IUCN.",
            required=False)
        is_private = schema.Choice(
            title=u"Is the workspace public or private?",
            vocabulary=config.WORKGROUP_ISPRIVATE_OPTIONS,
            default=config.WORKGROUP_ISPRIVATE_DEFAULT,
            required=True)
        keywords = colschema.Keywords(
            title=u'Other Search Terms',
            description=u'Examples: biodiversity, freshwater, Natural Heritage Programs, panthera leo',
            missing_value=(),
            required=False)
        license = colschema.VocabularyChoice(
            vocabulary=config.LICENSES_VOCABULARY,
            default=config.LICENCES_DEFAULT,
            title=u"License",
            required=True)

    form_fields = form.FormFields(form_schema)

    def reAuthenticate(self):
        """ Refresh authentication of the current user to get permissions
        to the workspace that were granted in this request """
        user = getSecurityManager().getUser()
        uid = user.getId()
        uf = aq_parent(aq_inner(user))
        user = uf.getUserById(uid)
        newSecurityManager(None, user)

    @form.action("Create", name="create")
    def form_create(self, action, data): #@UnusedVariable
        message = 'Note: You can always change this or add more people later.'
        import hotshot
        dev_profile_path = tempfile.gettempdir()
        #dev_profile_path = '/opt/buildout/var/profiling/'
        #my_profile_path = 'c:\\plone\\buildout\\profiling'
        profile_update = hotshot.Profile(join(dev_profile_path,
                                              'ws_update_call.txt'))
        profile_getObjectData = hotshot.Profile(join(dev_profile_path,
                                                     'getObjectData.txt'))
        profile_invokeFactory = hotshot.Profile(join(dev_profile_path,
                                                     'invokeFactory.txt'))
        getToolByName(self.context, 'plone_utils').addPortalMessage(message)
        self.context.invokeFactory(config.WORKSPACE_TYPE, data['id'])
        ws = self.context._getOb(data['id'])
        self.reAuthenticate()
        # re-auth is necessary to pass the workflow transition guard
        # exercised by the is_private field that might get changed next.
        ws.update(**data)
        ws._data = data.copy()
        # Do not index if 'is private'
        if not ws.getIs_private():
            gsa_index(ws)
        # redirect user to member management view
        raise SafeRedirect(ws.absolute_url() + "/wsmembers/workspace-members.html")

    @form.action("Cancel", name="cancel",
                 validator=xmlform.NO_VALIDATION)
    def form_cancel(self, action, data):
        raise SafeRedirect(self.context.absolute_url())

class WorkspaceCreationPage(Page):
    views = (WorkspaceCreationView, WorkspaceCreationForm) + COMMON_VIEWS

class MemberURLProfileMixin:

    def _getProfileURLFor(self, member):
        """ Return the profile URL if this member has permission to see the
        profile URL, None otherwise """
        # TODO check to see if profile is viewable
        ut = cmfutils.getToolByName(self.context, "portal_url")
        url = '%s/view-profile.html?userid=%s' % (ut(), member.getId())
        return url

class AllMembersListView(XMLView, MemberURLProfileMixin):
    """ View class for the xml listing of workspace members """

    def _renderMemberList(self, memberlist, adminIds):
        members_node = Element('members')
        for member in memberlist:
            # calculate the member tag attributes
            memberId=member.getId()
            kw = dict(id=memberId)
            if memberId in adminIds:
                kw['manager'] = str(True)
            # create the <member> tag with the attributes above
            member_node = SubElement(members_node, 'member', **kw)

            firstname = member.getProperty('firstname')
            lastname = member.getProperty('lastname')
            email = member.getProperty('email')
            # create the <member> subtags:
            SubElement(member_node, 'firstname').text = firstname
            SubElement(member_node, 'lastname').text = lastname
            SubElement(member_node, 'email').text = email
            profile_url = self._getProfileURLFor(member)
            if profile_url:
                # the current user might not have permission to view the
                # profile
                SubElement(member_node, 'profile', href=profile_url)

        return members_node

    def __call__(self):
        workspace = self.context
        wm = IWorkspaceMemberManagement(workspace)
        adminIds = set(member.getId() for member in wm.listManagerMembers())
        memberlist = wm.listAllMembers()

        xml = self._renderMemberList(memberlist, adminIds)
        return tostring(xml)

class WorkspaceMemberManagementAdapter(object):
    """ Provides the IWorkspaceMemberManagement API by adapting a workspace
    """

    interface.implements(IWorkspaceMemberManagement)
    component.adapts(IWorkspace)

    def __init__(self, workspace):
        self.workspace = workspace
        wid = workspace.getId()
        self._admin_group = wid + config.WORKSPACE_ADMIN_GROUP_SUFFIX
        self._member_group = wid + config.WORKSPACE_MEMBER_GROUP_SUFFIX
        self.groupsTool = cmfutils.getToolByName(self.workspace,
                                                 'portal_groups')
    def setUp(self):
        """ Create security set-up for recently created workspace """
        workspace = self.workspace
        # create the security groups
        members_group = self._member_group
        admins_group = self._admin_group
        uf = cmfutils.getToolByName(workspace, 'acl_users')
        uf.source_groups.addGroup(members_group, ())
        uf.source_groups.addGroup(admins_group, ())
        # give the groups the expected roles in the workspace
        workspace.manage_addLocalRoles(members_group,
                                       (config.WORKGROUP_MEMBER_ROLE,))
        workspace.manage_addLocalRoles(admins_group,
                                       (config.WORKGROUP_ADMINISTRATOR_ROLE,))
        # make the currently authenticated user a workspace manager
        m = cmfutils.getToolByName(workspace,
                                   'portal_membership').getAuthenticatedMember()
        if m is not None:
            self.addManager(m)

    def tearDown(self):
        """ Remove security set-up for a workspace to be removed """
        uf = cmfutils.getToolByName(self.workspace, 'acl_users')
        uf.source_groups.removeGroup(self._member_group)
        uf.source_groups.removeGroup(self._admin_group)
        # everything else will be removed with the group itself

    def listAllMembers(self):
        group = self.groupsTool.getGroupById(self._member_group)
        return group.getGroupMembers()

    def listAllMemberIds(self):
        group = self.groupsTool.getGroupById(self._member_group)
        return group.getGroupMemberIds()

    def listManagerMembers(self):
        group = self.groupsTool.getGroupById(self._admin_group)
        return group.getGroupMembers()

    def listManagerMemberIds(self):
        group = self.groupsTool.getGroupById(self._admin_group)
        return group.getGroupMemberIds()

    def isWorkspaceMember(self, member):
        return member.id in self.listAllMemberIds()
    
    def isWorkspaceManager(self, member):
        return member.id in self.listManagerMemberIds()

    def addMember(self, member):
        self.addMemberByID(member.getId())

    def addMemberByID(self, memberID):
        self.groupsTool.addPrincipalToGroup(memberID, self._member_group)

    def addManager(self, member):
        memberID = member.getId()
        self.addManagerByID(memberID)

    def addManagerByID(self, memberID):
        self.addMemberByID(memberID) # managers are members too
        self.groupsTool.addPrincipalToGroup(memberID, self._admin_group)

    def demoteMemberById(self, memberId):
        group = self.groupsTool.getGroupById(self._admin_group)
        if len(group.getGroupMembers()) > 1:
            self.groupsTool.removePrincipalFromGroup(memberId, self._admin_group)

    def promoteMemberById(self, memberId):
        self.groupsTool.addPrincipalToGroup(memberId, self._admin_group)

    def removeMemberById(self, memberId):
        # Here we take advantage of the fact that removing a principal from a
        # group doesn't fail even if it wasn't a member of the group to begin
        # with.
        self.groupsTool.removePrincipalFromGroup(memberId, self._admin_group)
        self.groupsTool.removePrincipalFromGroup(memberId, self._member_group)
        memTool = cmfutils.getToolByName(self.workspace,'portal_membership')
        member = memTool.getMemberById(memberId)
        if member.getProperty('email'):
            smt = simple_mail_tool()
            try:
                smt.sendEmailRemoved(self.workspace, member.getProperty('email'))
            except SMTPRecipientsRefused:
                pass #XXX email refused...need to figure out what to do...

class AddInvitationForm(FormBase):

    form_fields = form.Fields(IInviteByEmailSchema)

    def _getWorkspaceInvitedEmails(self):
        invtool = cmfutils.getToolByName(self.context,
                                         "workspace_invitations")
        invitations = invtool.getInvitationsForWorkspace(self.context)
        return set(invitation.email for invitation in invitations)

    def _getWorkspaceMemberEmails(self):
        wsMemberManager = IWorkspaceMemberManagement(self.context)
        members = wsMemberManager.listAllMembers()
        return set(member.getProperty('email') for member in members)

    def _sieveEmails(self, emails):
        toInvite = []
        alreadyInvited = []
        alreadyMember = []
        invalid = []

        workspaceInvitedEmails = self._getWorkspaceInvitedEmails()
        workspaceMemberEmails = self._getWorkspaceMemberEmails()
        for email in emails:
            email = email.strip()
            if not check_email(email):
                invalid.append(email)
            elif email in workspaceInvitedEmails:
                alreadyInvited.append(email)
            elif email in workspaceMemberEmails:
                alreadyMember.append(email)
            else:
                toInvite.append(email)

        return toInvite, alreadyInvited, alreadyMember, invalid

    @form.action('Add Invitations', name='invite')
    def handle_invitations(self, action, data): #@UnusedVariable
        """ Invite the provided e-mails to this workspace
        """
        MAX_ALLOWED_AT_ONE_TIME = 25
        workspace = self.context
        invtool = cmfutils.getToolByName(workspace, 'workspace_invitations')

        memberEmails = data['memberEmails'].split(',')
        (toInvite, alreadyInvited,
         alreadyMember, invalid) = self._sieveEmails(memberEmails)
        if toInvite:
            invtool.inviteToWorkspace(workspace, toInvite[:MAX_ALLOWED_AT_ONE_TIME])

        accepted = len(toInvite)

        # now render the response
        status_node = Element('status')
        emailsaccepted = str(accepted)
        if toInvite[MAX_ALLOWED_AT_ONE_TIME:]:
            msg = 'Only 25 invites can be sent at one time, %s invitations were not sent. %s'
            numbernotsent = str(len(toInvite[MAX_ALLOWED_AT_ONE_TIME:]))
            numbersent = str(len(toInvite[:MAX_ALLOWED_AT_ONE_TIME]))
            emailsaccepted = msg % (numbernotsent, numbersent)
        SubElement(status_node, 'accepted').text = emailsaccepted
        if alreadyMember or alreadyInvited or invalid:
            errors_node = SubElement(status_node, 'errors')
            for email in alreadyMember:
                SubElement(errors_node, 'member').text = email
            for email in alreadyInvited:
                SubElement(errors_node, 'invite').text = email
            for email in invalid:
                SubElement(errors_node, 'invalid').text = email

        self.request.RESPONSE.setHeader('Content-Type',
                                        'text/xml; charset=' + config.CHARSET)
        return tostring(status_node)

class WorkspaceMembershipManagementForm(FormBase):

    form_fields = form.Fields(IWorkspaceMemberManagementSchema)

    def _getAuthenticatedMemberId(self):
        pm = cmfutils.getToolByName(self.context, "portal_membership")
        return pm.getAuthenticatedMember().getId()


    def processRemovals(self, memberIds):
        """ remove the members in memberIds from the workspace.

        return a set of user ids from memberIds that weren't members to begin
        with. """
        memberIds = set(memberIds)
        wm = IWorkspaceMemberManagement(self.context)
        currentMemberIds = set(wm.listAllMemberIds())
        # filter userIds that are not even members and the current auth user
        # the latter is to avoid removing the last manager from a workspace
        invalids = (memberIds - (currentMemberIds -
                                 set([self._getAuthenticatedMemberId()])))
        for memberId in memberIds - invalids:
            wm.removeMemberById(memberId)
        return invalids

    def processPromotions(self, memberIds):
        """ promote the members in memberIds to workspace managers.

        return a set of user ids from memberIds that weren't members to begin
        with, or that were already managers """
        memberIds = set(memberIds)
        wm = IWorkspaceMemberManagement(self.context)
        currentMemberIds = set(wm.listAllMemberIds())
        currentManagerIds = set(wm.listManagerMemberIds())
        # filter out managers and non-members
        invalids = ((memberIds - currentMemberIds) |
                    (memberIds & currentManagerIds))
        for memberId in memberIds - invalids:
            wm.promoteMemberById(memberId)
        return invalids

    def processDemotions(self, memberIds):
        """ demote the members in memberIds from the workspace.
        return a set of user ids from memberIds that weren't managers to begin
        with. """
        memberIds = set(memberIds)
        wm = IWorkspaceMemberManagement(self.context)
        currentManagerIds = set(wm.listManagerMemberIds())
        # filter out non-managers and the current auth user the latter is to
        # avoid removing the last manager from a workspace
        invalids = (memberIds - currentManagerIds)
        if len(currentManagerIds) > 1 and (len(memberIds) != len(currentManagerIds)):
            for memberId in memberIds - invalids:
                    wm.demoteMemberById(memberId)
        return invalids

    @form.action('Manage Membership', name='manageMembership')
    def handle_member_management(self, action, data): #@UnusedVariable
        """ Handle the requested membership changes
        """
        accepted = 0

        toRemove = set(userId.strip()
                       for userId in data['removeMembers'].split(','))
        invalidRemovals = self.processRemovals(toRemove)
        accepted += len(toRemove) - len(invalidRemovals)

        toPromote = set(userId.strip()
                        for userId in data['promoteMembers'].split(','))
        invalidPromotions = self.processPromotions(toPromote)
        accepted += len(toPromote) - len(invalidPromotions)

        toDemote = set(userId.strip()
                       for userId in data['demoteMembers'].split(','))
        invalidDemotions = self.processDemotions(toDemote)
        accepted += len(toDemote) - len(invalidDemotions)

        # now render the response
        status_node = Element('status')
        SubElement(status_node, 'accepted').text = str(accepted)
        if invalidRemovals or invalidPromotions or invalidDemotions:
            errors_node = SubElement(status_node, 'errors')
            for invalidId in invalidRemovals:
                SubElement(errors_node, 'removal').text = invalidId
            for invalidId in invalidPromotions:
                SubElement(errors_node, 'promotion').text = invalidId
            for invalidId in invalidDemotions:
                SubElement(errors_node, 'demotion').text = invalidId
        self.request.RESPONSE.setHeader('Content-Type',
                                        'text/xml; charset=' + config.CHARSET)
        return tostring(status_node)

class WorkspaceInvitationListingView(XMLView, MemberURLProfileMixin):
    """ View class for the xml listing of workspace invitations """

    def __call__(self):
        context = self.context
        invitations_tag = Element('invitations')
        invtool = cmfutils.getToolByName(context, 'workspace_invitations')
        membership_tool = cmfutils.getToolByName(context, 'portal_membership')
        for invitation in invtool.getInvitationsForWorkspace(context):
            invitation_tag = SubElement(invitations_tag, 'invitation', iid=invitation.getId())
            SubElement(invitation_tag, 'email').text = invitation.email
            SubElement(invitation_tag, 'lastcontact').text = invitation.lastSent.strftime('%B %d, %Y')
            # add profile information if present
            membersByEmail = membership_tool.searchForMembers(email=invitation.email)
            if membersByEmail:
                invitedMember = membersByEmail[0]
                firstname = invitedMember.getProperty('firstname')
                lastname = invitedMember.getProperty('lastname')
                SubElement(invitation_tag, 'firstname').text = firstname
                SubElement(invitation_tag, 'lastname').text = lastname
                SubElement(invitation_tag, 'profile', href=self._getProfileURLFor(invitedMember))
        return toStringWithPreamble(invitations_tag)

class CancelInvitationForm(FormBase):

    form_fields = form.Fields(ICancelInvitationSchema)

    def processCancelations(self, invitationIds):
        invtool = cmfutils.getToolByName(self.context, 'workspace_invitations')
        return invtool.cancelInvitationsById(invitationIds)

    @form.action('Cancel Invitations', name='cancelInvitations')
    def handle_invitation_cancelation(self, action, data): #@UnusedVariable
        toCancel = [invitadionId.strip()
                    for invitadionId in data['invitationIds'].split(',')]
        invalidCancelations = self.processCancelations(toCancel)
        accepted = len(toCancel) - len(invalidCancelations)

        # render the XML
        status_tag = Element('status') # <status>...
        # <status><accepted>23</accepted>...
        SubElement(status_tag, 'accepted').text=str(accepted)
        if invalidCancelations:
            # <status
            #   ...
            #   <errors>
            #      <invalid>foo</invalid>
            #      <invalid>bar</invalid>
            #   </errors>
            # </status>
            errors_tag = SubElement(status_tag, 'errors')
            for invId in invalidCancelations:
                SubElement(errors_tag, 'invalid').text = str(invId)

        self.request.RESPONSE.setHeader('Content-Type',
                                        'text/xml; charset=' + config.CHARSET)
        return toStringWithPreamble(status_tag)

class ReSendInvitationForm(FormBase):

    form_fields = form.Fields(IReSendInvitationSchema)

    def processReSends(self, invitationIds):
        invtool = cmfutils.getToolByName(self.context, 'workspace_invitations')
        return invtool.reSendInvitationsById(invitationIds)

    @form.action('Re-send Invitations', name='reSendInvitations')
    def handle_invitation_resending(self, action, data): #@UnusedVariable
        toReSend = [invitadionId.strip()
                    for invitadionId in data['invitationIds'].split(',')]
        invalidReSendings = self.processReSends(toReSend)
        accepted = len(toReSend) - len(invalidReSendings)

        # render the XML
        status_tag = Element('status') # <status>...
        # <status><accepted>23</accepted>...
        SubElement(status_tag, 'accepted').text=str(accepted)
        if invalidReSendings:
            # <status
            #   ...
            #   <errors>
            #      <invalid>foo</invalid>
            #      <invalid>bar</invalid>
            #   </errors>
            # </status>
            errors_tag = SubElement(status_tag, 'errors')
            for invId in invalidReSendings:
                SubElement(errors_tag, 'invalid').text = str(invId)

        self.request.RESPONSE.setHeader('Content-Type',
                                        'text/xml; charset=' + config.CHARSET)
        return toStringWithPreamble(status_tag)

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

import re

from Acquisition import aq_parent, aq_inner
from Products.COL3.etree import Element, SubElement
from Products.COL3.etree import tostring
from Products.CMFCore import utils as cmfutils
from Products.COL3.interfaces import IUserPreferencesSchema
from Products.Five.formlib.formbase import FormBase
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapts
from zope.formlib.form import action
from zope.formlib.form import Fields
from zope.interface import implementsOnly
from Products.COL3.browser.base import XSLTView
from Products.COL3 import config
from zExceptions import NotFound
from zope.app.component.hooks import getSite
from Products.COL3.browser.base import XMLView
from Products.COL3.browser.base import Page, Fragment
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.interfaces.workspace import IMemberSearchSchema

class MemberDisplayView(XSLTView):
    """ View class for the member resource """

    def update(self):
        """ gather field display information in view for the template """
        context = self.context
        self.fields = []
        for fieldname in config.PROFILE_PERCENTAGE_FIELDS:
            field = context.getField(fieldname)
            accessor = field.getAccessor(context)
            info = dict(name=fieldname,
                        label=field.widget.Label(context),
                        value=accessor())
            self.fields.append(info)


class UserPreferencesView(FormBase):
    #template = ViewPageTemplateFile('preferences.pt')
    form_fields = Fields(IUserPreferencesSchema)

    def __init__(self, context, request):
        super(UserPreferencesView, self).__init__(context, request)

        # A member is not a content object. Setting render_context will
        # make sure our SiteMemberAdapter is used in preference to
        # grabbing everything from the real context, which is the site.
        for field in self.form_fields:
            field.render_context = True

    @action(u'Set preferences')
    def handle_edit(self, action, data): #@UnusedVariable
        """ Handle preferences changes
        """
        membership_tool = cmfutils.getToolByName(self.context,
                                                 'portal_membership')
        member = membership_tool.getAuthenticatedMember()
        member.setMemberProperties(data)
        member_id = member.getId()

        if data.get('portrait'):
            # Unlike in Zope 2, the Zope 3 file widget hands back a string
            # containing the image data, not a FileUpload instance. However,
            # the request does contain a real FileUpload, so we use it
            # because the Plone portrait mechanism can only deal with that.
            file = self.request.get('%s.portrait' % self.prefix)

            # Need to "rewind" it to the zero file position first since it
            # has been read once already and the pointer is at the end of the
            # file data.
            file.seek(0)

            membership_tool.changeMemberPortrait(file, member_id)

        self.status = u'Preferences changed for user %s' % member_id

class MemberAdapter(object):
    """ Provides the IUserPreferencesSchema API and adapts to the member """

    implementsOnly(IUserPreferencesSchema)

    # Fields that need special treatment
    complex_fields = ('portrait',)

    def __init__(self, member):
        self.member = member
        self.field_names = [ x for x in IUserPreferencesSchema.names()
                               if x not in self.complex_fields ]

    def __getattr__(self, name, default=None):
        """ Retrieve the schema properties from the member
        """
        if name in self.field_names:
            return self.member.getProperty(name)
        if name in self.complex_fields:
            return None

        return super(MemberAdapter, self).__getattr__(name, default)

    @property
    def portrait(self):
        """ Retrieve the personal portrait through the membership tool
        """
        mtool = cmfutils.getToolByName(self, 'portal_membership')
        return mtool.getPersonalPortrait(self.member.getId())


class SiteMemberAdapter(MemberAdapter):
    """ Provides the IUserPreferencesSchema API and adapts to the site

    We need to adapt to the site because the preferences.html view will
    be invoked at the site root.
    """
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        self.context = context
        membership_tool = cmfutils.getToolByName(self.context,
                                                 'portal_membership')
        member = membership_tool.getAuthenticatedMember()
        MemberAdapter.__init__(self, member)


class MemberWorkspacesMixin:
    # XXX THIS CLASS HAS KNOWLEDGE ABOUT THE MAPPING OF WORKSPACE
    # MEMBERSHIP TO PLONE GROUPS AND USERS. MAYBE REFACTOR INTO ITS OWN
    # MODULE ALONG WITH WorkspaceMemberManagerAdapter?

    def _getMemberWorkspaceIds(self, member):
        pg = cmfutils.getToolByName(self.context, 'portal_groups')
        groupIds = pg.getGroupsForPrincipal(member)
        # find the workspace Ids from the group membership
        workspaceIdsAsManager = set()
        workspaceIdsAsMember = set()
        ADMIN_SUFFIX_LEN = len(config.WORKSPACE_ADMIN_GROUP_SUFFIX)
        MEMBER_SUFFIX_LEN = len(config.WORKSPACE_MEMBER_GROUP_SUFFIX)
        for groupId in groupIds:
            if groupId.endswith(config.WORKSPACE_ADMIN_GROUP_SUFFIX):
                workspaceIdsAsManager.add(groupId[:-ADMIN_SUFFIX_LEN])
            elif groupId.endswith(config.WORKSPACE_MEMBER_GROUP_SUFFIX):
                workspaceIdsAsMember.add(groupId[:-MEMBER_SUFFIX_LEN])

        return workspaceIdsAsManager, workspaceIdsAsMember

    def _getWorkspaceColleaguesIds(self):
        au = cmfutils.getToolByName(self.context, 'acl_users')
        (workspaceIdsAsManager, workspaceIdsAsMember) = self._getAuthenticatedMemberWorkspaceIds()
        # XXX this line is not necessary as all workspaces as managers are
        # are a subset of workspaces as member
        allWorkspaceIds = workspaceIdsAsMember | workspaceIdsAsManager
        memberIds = set()
        for workspaceId in allWorkspaceIds:
        # XXX Need to enforce search limit.
            group = au.getGroupByName(workspaceId + config.WORKSPACE_MEMBER_GROUP_SUFFIX)
            memberIds.update(group.getMemberIds())

        return memberIds

    def _getAuthenticatedMemberWorkspaceIds(self):
        pm = cmfutils.getToolByName(self.context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        (workspaceIdsAsManager,
         workspaceIdsAsMember) = self._getMemberWorkspaceIds(member)

        return workspaceIdsAsManager, workspaceIdsAsMember

    def _workspaceRecordsFromIds(self, workspaceIds):
        # get workspace information in the catalog
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')
        query = dict(getId=list(workspaceIds),
                     portal_type=config.WORKSPACE_TYPE,
                     sort_on="sortable_title")
        allWorkspaceRecords = catalog(query)
        return allWorkspaceRecords

class MemberWorkspacesListView(XMLView, MemberWorkspacesMixin):
    """XML listing of the workspaces the current auth user is a member of

     for the benefit of ajax views"""

    def __call__(self):
        (workspaceIdsAsManager,
         workspaceIdsAsMember) = self._getAuthenticatedMemberWorkspaceIds()
        # group managers are also group members, so we only need to query
        # the groups where the user is a member, so tecnically, the next line
        # isn't needed
        allWorkspaceIds = workspaceIdsAsManager | workspaceIdsAsMember
        allWorkspaceRecords = self._workspaceRecordsFromIds(allWorkspaceIds)

        # render the result
        workspaces_tag = Element('workspaces')
        manager_tag = SubElement(workspaces_tag, 'manager')
        member_tag = SubElement(workspaces_tag, 'member')
        for record in allWorkspaceRecords:
            if record.getId in workspaceIdsAsManager:
                tag = manager_tag
            elif record.getId in workspaceIdsAsMember:
                # user can be both member and manager of the workspace so we
                # only include in the member list if he's not manager
                tag = member_tag
            else:
                continue # XXX does it ever happen?
            SubElement(tag, 'memberlist',
                       href=record.getURL() + "/workspace-members.xml",
                       ).text = record.Title

        return tostring(workspaces_tag)

class MemberSearchForm(FormBase, MemberWorkspacesMixin):

    form_fields = Fields(IMemberSearchSchema)

    def _renderInvitationMemberList(self, memberlist):
        members_tag = Element('members')
        for member in memberlist:
            member_tag = SubElement(members_tag, 'member', id=member.getId())
            firstname = member.getProperty('firstname')
            lastname = member.getProperty('lastname')
            email = member.getProperty('email')
            # create the <member> subtags:
            SubElement(member_tag, 'firstname').text = firstname
            SubElement(member_tag, 'lastname').text = lastname
            SubElement(member_tag, 'email').text = email

        return members_tag

    @action('Search For Members', name='search')
    def handle_search(self, action, data): #@UnusedVariable
        name = data['name']
        memberList = self._searchForName(name)
        element = self._renderInvitationMemberList(memberList)
        self.request.RESPONSE.setHeader('Content-Type',
                                        'text/xml; charset=' + config.CHARSET)
        return tostring(element)

    def _searchForName(self, name):
        # Search on the prefix of the first or last name (or, in this case,
        # any middle name as well)
        # XXX doing linear scan, will be slow with lots of members
        nameMatches = re.compile(r'\b' + re.escape(name),
                                 re.IGNORECASE).search
        pm = cmfutils.getToolByName(self.context, 'portal_membership')
        portal = getSite()
        people = portal.people_catalog.searchResults(sort_on='lastname')
        # previous listMembersIds was self._getWorkspaceColleaguesIds()
        # which made only would show members whom you are 'colleagues' with

        memberList = []
        for person in people:
            #member = pm.getMemberById(person.userid)
            #fullname = member.getProperty('fullname')
            fullname = person.firstname +' '+person.lastname
            if nameMatches(fullname):
                member = pm.getMemberById(person.userid)
                memberList.append((fullname, member))

        return [member for fullname, member in sorted(memberList)]

class ProfileTooltip(XMLView, MemberWorkspacesMixin):
    """ Traversable view of portal_membership that renders the profile tooltip
    """

    def renderXML(self, userid=None):
        context = self.context
        request = self.request
        if userid is None:
            userid = request['id']
        mt = cmfutils.getToolByName(context, 'portal_membership')
        ut = cmfutils.getToolByName(context, 'portal_url')
        portal = ut.getPortalObject()

        member = mt.getMemberById(userid)
        if member is None:
            return 'failed'

        self.memberInfo = dict(member_id=userid)

        fname = member.getProperty('firstname', 'firstname')
        lname = member.getProperty('lastname', 'lastname')
        email = member.getProperty('email', 'NO EMAIL')
        loc = member.getProperty('location', 'location')
        org = member.getProperty('organization', 'organization')
        history = '%s/workspaces/%s/documents/withauthor-documents.html?userid=%s'
        history = history % (portal.absolute_url(), context.id, userid)
        profile = '/portal_membersip/%s' % userid
        preferences = '/profile/%s/preferences.html' % userid
        image = '/static/images/defaultUser.gif'

        tooltip = Element('profile')

        #XXX _getMemberWorkspaceIds must be wrong.
        #    not sure what leo is doing. NEEDS HELP!
        #    why are you returning a SET???!!!!!

        mgrs, members = self._getMemberWorkspaceIds(member)
        dic = {}
        for x in ([x for x in mgrs] + [x for x in members]):
            dic[x] = None
        ids = dic.keys()

        workspaces = SubElement(tooltip, 'workspaces')
        for id in ids:
            ws = portal.workspaces[id] 				#XXX HARDCODED!!
            workspace = SubElement(workspaces, 'workspace')
            SubElement(workspace, 'id').text = ws.id
            SubElement(workspace, 'title').text = ws.title
            SubElement(workspace, 'url').text = ws.absolute_url()

        interests = SubElement(tooltip, 'interests')
        for interest in interests:
            SubElement(interests, 'interest').text = interest

        SubElement(tooltip, 'firstname').text = fname
        SubElement(tooltip, 'lastname').text = lname
        SubElement(tooltip, 'location').text = loc
        SubElement(tooltip, 'organization').text = org
        SubElement(tooltip, 'history_url').text = history
        SubElement(tooltip, 'profile_url').text = profile
        SubElement(tooltip, 'preferences').text = preferences
        SubElement(tooltip, 'image_url').text = image
        SubElement(tooltip, 'email').text = email

        self.request.RESPONSE.setHeader('Content-Type',
                                        'text/xml; charset=' + config.CHARSET)
        return tostring(tooltip)

    memberInfo = None

    def __getitem__(self, name):
        """ Make view traversable. When traversed, prepare the view for
        handling a specific member and return the view itself """
        if self.memberInfo is not None:
            # trying to traverse twice?
            raise NotFound(name)
        self.memberInfo = dict(member_id=name)
        return self

    def update(self):
        if self.memberInfo is None:
            raise NotFound("Please traverse to user id")
        member = self.context.getMemberById(self.memberInfo['member_id'])
        properties_adapter = MemberAdapter(member)
        self.memberInfo.update(member=member,
                               properties=properties_adapter,)

    def getTop5MemberWorkspaceRecords(self):
        # XXX in which order?
        (workspaceIdsAsManager,
         workspaceIdsAsMember) = self._getMemberWorkspaceIds(self.memberInfo['member'])[:5]
        wids = workspaceIdsAsManager | workspaceIdsAsMember
        if wids:
            return self._workspaceRecordsFromIds(wids)
        return []

    def getFullProfileURL(self):
        memberId = self.memberInfo['member_id']
        return self.context.absolute_url() + '/profile_by_id/' + memberId

class MemberPanelViewFragment(Fragment):
    def asElement(self):
        """ the view section for the member panel view"""
        root = Element('view')
        root.attrib['id'] = 'colmember-panel'
        elem = SubElement(root, 'formcontroller')
        elem.attrib['action'] = '..'
        elem.attrib['mode'] = 'add'
        elem.attrib['type'] = 'COLMember'
        return root

#XXX Context should go away I believe...BJS
class MemberPanelContextFragment(Fragment):
    def asElement(self):
        """ the context section for the member panel view """
        context = self.context
        root = Element('context')
        parent = aq_parent(aq_inner(context))
        elem = SubElement(root, 'parent')
        elem.attrib['href'] = parent.absolute_url()
        elem.text = 'Portal Members'
        return root

class MemberPanelView(Page):
    views = COMMON_VIEWS +(MemberPanelViewFragment,
                           MemberPanelContextFragment)



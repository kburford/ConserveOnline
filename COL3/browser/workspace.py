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
from urllib import urlencode
from Acquisition import aq_parent, aq_inner, aq_chain
from datetime import datetime, timedelta

from Products.COL3.etree import Element, SubElement

#XXX Things that will probably go away
from zope.formlib import form
from zExceptions.unauthorized import Unauthorized
from Products.COL3.etree import fromstring
from Products.COL3.interfaces.workspace import IWorkspaceJoinSchema
#XXX Things that will probably go away

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import utils as cmfutils

from Products.COL3 import calendar
from Products.COL3.content.label import sortable_title
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.base import Fragment, Page, AjaxPage
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.browser.batch import BatchFragment
from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.browser.workgroup import MemberURLProfileMixin
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.exceptions import JoinRequestAlreadySubmited, AlreadyWorkspaceMember
from Products.COL3.browser.common import MenuFragment
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.formlib.xmlform import EditFormFragment
from Products.COL3.browser.user import ViewProfileFragment
from Products.COL3.permissions import MANAGE_WORKSPACE_PERMISSION
from Products.COL3.interfaces.workspace import IWorkspaceEditPropertiesSchema
from Products.COL3.content.label import Labeller

class WorkspaceViewFragment(Fragment):
    """ View fragment for default workspace view """
    def asElement(self):
        context = self.context
        return Element('view',
                       name="view-workspace.html",
                       type="workspace",
                       title=context.Title(),
                       section="workspaces"
                       )

class WorkspaceMenuFragment(MenuFragment):

    additems = (('Join Workspace', 'add-joinrequest.html'),)

    def _showAddMenu(self):
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getAuthenticatedMember()
        wm = IWorkspaceMemberManagement(context)
        return member.id not in wm.listAllMemberIds()

class WorkspaceKeywordsFragment(Fragment):
    """Fragment to display all labels in the workspace in a format used for the workspace
    homepage.

    NOTE - At the beginning of the project what are now called "keywords" were referred
    to as "labels".  End users didn't like "labels" so the decision was made to change
    to "labels" to "keywords".  Any reference to labels is due to not wanting to change
    the underlying machinery that handles labelling (i.e. Labeller object below reflects this)
    """
    def asElement(self):
        labeller = Labeller(self.context)
        keywords = labeller.listLabelObjects()
        keywords_tag = Element('workspacekeywords')
        withkeyword_url = '/documents/withkeyword-documents.html?'
        href = self._getWorkspaceUrl() + withkeyword_url
        for keyword in keywords:
            current_keyword = keyword['label']
            sortable_title = keyword['sortable_title']
            count = len(current_keyword.getTraversableBRefs(self.context))
            if count > 0:
                params = urlencode(dict(keyword=sortable_title))
                keywordelem = SubElement(keywords_tag, 'keyword', href=href + params)
                SubElement(keywordelem, 'title').text = current_keyword.Title()
                SubElement(keywordelem, 'description').text = current_keyword.Description()
                SubElement(keywordelem, 'count').text = str(count)
        if len(keywords_tag):
            return keywords_tag

    def _getWorkspaceUrl(self):
        for link in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(link):
                return link.absolute_url()

class WorkspacePage(Page):
    views = (WorkspaceViewFragment,
             WorkspaceKeywordsFragment,
             WorkspaceMenuFragment) + COMMON_VIEWS

class CalendarMenuFragment(Fragment):
    """ Gets addables from the base, generates any utility menus """

    _additems = (('Add Event', '@@add-event.html'),)
    _utilitems = (('Monthly', 'monthly.html'),
                 ('Listing', 'listing.html'), )
    _current = ''

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('addmenu')
        for label, relative_url in self._additems:
            try:
                context.restrictedTraverse(relative_url)
            except Unauthorized:
                pass
            else:
                SubElement(actionmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label
        utilmenu = SubElement(menu_tag, 'utilitymenu')
        for label, href in self._utilitems:
            utilelem = SubElement(utilmenu, 'entry')
            utilelem.text = label
            utilelem.attrib['href'] = '%s/%s' % (url, href)
            if label.strip() == self._current:
                utilelem.attrib['current'] = 'current'
        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        return menu_tag

class MonthlyCalendarmenuFragment(CalendarMenuFragment):
    _current = 'Monthly'

class CalendarmenuListingFragment(CalendarMenuFragment):
    _current = 'Listing'

class CalendarFragment(Fragment):
    """ Fragment for monthly calendar and calendar listing views"""

    querystr = ''

    def asElement(self):

        context = self.context
        request = self.request

        now = datetime.now()
        nyear = str(now.year)
        nmonth = str(now.month).zfill(2)

        wsurl = context.absolute_url()
        current = request.get('ym', nyear+nmonth)

        nextdelta = timedelta(days=31)
        prevdelta = timedelta(days=2)
        year  = int(current[:4])
        month = int(current[4:])

        curr_year = str(year)
        prev_year = str(year-1)
        next_year = str(year+1)

        startdate = datetime(year, month, 1)
        enddate = datetime(year, month, calendar.monthrange(year, month)[1])
        next = startdate + nextdelta
        prev = startdate - prevdelta
        root = Element('calendar')
        if now.month == month and now.year == year:
            root.attrib['current'] = now.strftime('%Y-%m-%d')
        else:
            root.attrib['current'] = '%s-%s-01' % (str(year).zfill(2), str(month).zfill(2))

        months = [r for r in range(12)]
        monthnames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        linkelem = SubElement(root, 'calendarlinks')
        SubElement(linkelem, 'prevyearlink', href=wsurl+'/'+self.querystr+prev_year+'12').text=prev_year
        SubElement(linkelem, 'nextyearlink', href=wsurl+'/'+self.querystr+next_year+'01').text=next_year
        for month in months:
            url = wsurl+'/'+self.querystr+curr_year+str(month+1).zfill(2)
            currelem = SubElement(linkelem, 'calendarlink', href=url)
            currelem.text = monthnames[month]
            if str(month+1).zfill(2) == current[4:]:
                currelem.attrib['current'] = 'current'

        nav = SubElement(root, 'navigation')
        nextelem = SubElement(nav, 'next')
        nextelem.attrib['href'] = '%s/%s%s%s' % (wsurl,
                                                 self.querystr,
                                                 str(next.year),
                                                 str(next.month).zfill(2))
        nextelem.text = '%s-%s-%s' % (next.year, str(next.month).zfill(2), '01')
        prevelem = SubElement(nav, 'previous')
        prevelem.attrib['href'] = '%s/%s%s%s' % (wsurl,
                                                 self.querystr,
                                                 str(prev.year),
                                                 str(prev.month).zfill(2))
        prevelem.text = '%s-%s-%s' % (prev.year, str(prev.month).zfill(2), '01')
        ctool = cmfutils.getToolByName(context, 'portal_catalog')
        eventsquery = ctool(portal_type='Event',
                            path='/'.join(context.getPhysicalPath()),
                            start={'query': startdate, 'range': 'min'},
                            end={'query': enddate, 'range': 'max'})
        if len(eventsquery) > 0:
            eventselem = SubElement(root, 'events')
            for event in eventsquery:
                eventelem = SubElement(eventselem, 'event')
                eventelem.attrib['href'] = event.getURL()
                elem = SubElement(eventelem, 'title')
                elem.text = event.Title
                elem = SubElement(eventelem, 'startDate')
                elem.text = event.start.ISO8601()
                elem = SubElement(eventelem, 'endDate')
                elem.text = event.end.ISO8601()
        return root

class MonthlyCalendarFragment(CalendarFragment):
    querystr = 'monthly.html?ym='

class CalendarListingFragment(CalendarFragment):
    querystr = 'listing.html?ym='

class CalendarViewFragment(Fragment):

    def asElement(self):
        request = self.request

        today = datetime.now() #as a backup incase year and month
                               #aren't provided
        bu_month = str(today.month).zfill(2)
        bu_year = str(today.year)
        current = request.get('ym', bu_year+bu_month)
        year  = int(current[:4])
        month = int(current[4:])
        calendarmonth = datetime(int(year), int(month), int('01'))

        root = Element('view')
        root.attrib['type'] = 'calendar'
        root.attrib['title'] = '%s %s' % (calendarmonth.strftime('%B'), year)
        root.attrib['section'] = 'workspaces'
        return root

class MonthlyCalendarViewFragment(CalendarViewFragment):
    def asElement(self):
        elem = super(MonthlyCalendarViewFragment, self).asElement()
        elem.attrib['name'] = 'monthly.html'
        return elem

class CalendarListingViewFragment(CalendarViewFragment):
    def asElement(self):
        elem = super(CalendarListingViewFragment, self).asElement()
        elem.attrib['name'] = 'listing.html'
        return elem

class MonthlyCalendarPage(Page):
    views = (MonthlyCalendarViewFragment,
             MonthlyCalendarmenuFragment,
             MonthlyCalendarFragment) + COMMON_VIEWS

class CalendarListingPage(Page):
    views = (CalendarListingViewFragment,
             CalendarmenuListingFragment,
             CalendarListingFragment) + COMMON_VIEWS

class OutstandingRequestsFragment(Fragment):
    """ Fragment to return outstanding workspace requests """
    def asElement(self):
        elem = Element('requests')
        context = self.context

        tool = cmfutils.getToolByName(context, 'workspace_join_requests')
        mt = cmfutils.getToolByName(context, 'portal_membership')

        for req in tool.getJoinRequestsForWorkspace(context):
            userid = req.memberID
            member = mt.getMemberById(userid)
            if userid is None: continue
            entryelem = SubElement(elem, 'entry')
            subelem = SubElement(entryelem, 'id').text = req.id
            subelem = SubElement(entryelem, 'firstname')
            subelem.text = member.getProperty('firstname', 'N/A')
            subelem = SubElement(entryelem, 'lastname')
            subelem.text = member.getProperty('lastname', 'N/A')
            subelem = SubElement(entryelem, 'email')
            subelem.text = member.getProperty('email', 'N/A')
            subelem = SubElement(entryelem, 'message').text = req.reason
        return elem

class OutstandingRequestsPage(AjaxPage):

    views = (OutstandingRequestsFragment,)

###########################################
##        Workspace Join View Start       ##
#########################################
##XXX - More refactoring work needs to be done here XXX
class WorkspaceJoinView(Fragment):

    def rejectRequests(self):
        """ XXX Needs error handling """
        context = self.context
        request = self.request

        ids = request.get('request_ids')
        try:
            ids = ids.split(',')
        except AttributeError:
            return 'failure'

        # XXX This is not good enough.  We need to send a 'rejection notification'
        #     the tool should grow this not the client API
        tool = cmfutils.getToolByName(context, 'workspace_join_requests')
        tool.cancelJoinRequestsById(ids)
        return 'success'

    def acceptRequests(self):
        """ XXX Needs error handling """
        context = self.context
        request = self.request
        ids = request.get('request_ids')
        try:
            ids = ids.split(',')
        except AttributeError:
            return 'failure'

        tool = cmfutils.getToolByName(context, 'workspace_join_requests')
        invalids = tool.acceptJoinRequestsById(ids)
        if invalids:
            tool.cancelJoinRequestsById(invalids)
            return 'failure'
        return 'success'

class AddJoinRequestViewFragment(Fragment):

    def asElement(self):
        pmem = getToolByName(self.context, 'portal_membership')
        self.request['userid'] = pmem.getAuthenticatedMember().id
        root = Element('view',
               type="workspace",
               name="add-joinrequest.html",
               title="Request to Join Workspace",
               section="workspaces")
        return root

class AddJoinRequestForm(EditFormFragment):

    form_fields = form.FormFields(IWorkspaceJoinSchema)

    def getDataFromContext(self):
        return {}

    def applyChangesAndReturnURL(self, data):
        context = self.context
        ws_url = context.absolute_url()
        reason = data.get('reason', '')
        join_requests_tool = cmfutils.getToolByName(context, 'workspace_join_requests')
        try:
            join_requests_tool.addJoinRequest(context, reason=reason)
            statusmsg = 'Your request to join the %s workspace has been sent.' % context.title_or_id()
            cmfutils.getToolByName(context, 'plone_utils').addPortalMessage(statusmsg)
            raise SafeRedirect(ws_url)
        except JoinRequestAlreadySubmited:
            errmsg = 'Your request to join the %s workspace has been received and the workspace manager has been notified.' % context.title_or_id()
            cmfutils.getToolByName(context, 'plone_utils').addPortalMessage(errmsg)
            raise SafeRedirect(ws_url)
        except AlreadyWorkspaceMember:
            errmsg = 'You are already a member of the %s workspace' % context.title_or_id()
            cmfutils.getToolByName(context, 'plone_utils').addPortalMessage(errmsg)
            raise SafeRedirect(ws_url)

    def cancelURL(self):
        return self.context.absolute_url()

class AddJoinRequestPage(Page):
    views = (AddJoinRequestViewFragment,
             AddJoinRequestForm,
             ViewProfileFragment, ) + COMMON_VIEWS

############################################
##        Workspace Join View End         ##
############################################

##################################333##########
## Edit Workspace Configuration View Start   ##
###############################333#############

class EditWorkspacePropertiesView(Fragment):
    """ The view portion of the workspace edit config form xml
        <view name="edit-properties.html" type="workspace" title="Workspace Settings" section="workspaces"/>
    """
    def asElement(self):
        return Element('view',
                       name="edit-properties.html",
                       type="workspace",
                       title="Workspace Settings",
                       section="workspaces")

class EditWorkspacePropertiesForm(EditFormFragment):
    """ class that handles the processing of workspace config data
    """
    form_fields = form.FormFields(IWorkspaceEditPropertiesSchema)

    def getDataFromContext(self):
        """Supplies the data to populate the edit form fields"""
        context = aq_inner(self.context)
        return dict(title=context.Title(),
                    description=context.Description(),
                    logo=None,
                    content = context.getRawContent(),
                    language=context.getLanguage(),
                    country=context.getCountry(),
                    biogeographic_realm=context.getBiogeographic_realm(),
                    habitat=context.getHabitat(),
                    conservation=context.getConservation(),
                    directthreat=context.getDirectthreat(),
                    organization=context.getOrganization(),
                    monitoring=context.getMonitoring(),
                    keywords=context.getKeywords(),
                    is_private=context.getIs_private(),
                    license=context.getLicense())

    def applyChangesAndReturnURL(self, data):
        """ Collects input data and performs update """
        context = aq_inner(self.context)
        if data['workspacelogo'] is None:
            if data['remove_logo'] == 'yes': #
                context['workspacelogo'].setImage('DELETE_IMAGE')
                context['workspaceicon'].setImage('DELETE_IMAGE')
        elif data['remove_logo'] == 'yes':                    #this shouldn't really happen, but just in case...
            context['workspacelogo'].setImage('DELETE_IMAGE') #this means they entered a value for the logo, but then
            context['workspaceicon'].setImage('DELETE_IMAGE') #chose to return to defaults
        else: #set the logo on the workspace
            try:
                context['workspacelogo'].setImage(data['workspacelogo'])
            except AttributeError:
                pass #pass #the workspace was created before the logo attrib was added
            if not data['workspaceicon']: #set the icon to the logo, remove icon from data dict
                try:
                    context['workspaceicon'].setImage(data['workspacelogo'])
                except AttributeError:
                    pass #pass #the workspace was created before the icon attrib was added
        if data.get('workspaceicon'): #set the workspace icon to the icon supplied
            try:
                context['workspaceicon'].setImage(data['workspaceicon'])
            except AttributeError:
                pass #pass #the workspace was created before the icon attrib was added
        context.update(**data)
        return context.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class EditWorkspacePropertiesPage(Page):
    views = (EditWorkspacePropertiesView,
             EditWorkspacePropertiesForm) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'Workspace Settings',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(EditWorkspacePropertiesPage, self).getResponse()

##################################333##########
## Edit Workspace Configuration View End     ##
###############################333#############

class EventViewFragment(Fragment):
    def asElement(self):
        """ <view name="view.html" type="event" title="View Event" section="workspaces"/> """
        elem = Element('view')
        elem.attrib['name'] = 'view.html'
        elem.attrib['type'] = 'event'
        elem.attrib['title'] = 'View Event - '+self.context.Title()
        elem.attrib['section'] = 'workspaces'
        return elem

class EventMenuFragment(Fragment):
    """ Menu fragment for events """
    _actionmenu_items = ((u'Edit','@@edit.html'),
                      (u'Delete','@@delete.html'),)

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('actionmenu')
        for label, relative_url in self._actionmenu_items:
            try:
                context.restrictedTraverse(relative_url)
            except Unauthorized:
                pass
            else:
                SubElement(actionmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label
        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        return menu_tag

class EventView(Page):
    views = (EventViewFragment, EventMenuFragment,) + COMMON_VIEWS

################################################
##  Code for workspace member mgmt page start ##
################################################

class MembershipManagementView(Fragment):
    """<view type="workspace" name="manage-members.html" section="workspaces" title="Manage Members"/>
       OR, if you're not a manager then...
       <view type="workspace" name="list-members.html" section="workspaces"title="Members"/>"""
    def asElement(self):
        context = self.context
        name = ''
        title = ''
        mt = cmfutils.getToolByName(context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        workspace = aq_parent(aq_inner(context))
        if member.getUser().has_permission(MANAGE_WORKSPACE_PERMISSION, workspace):
            name = 'manage-members.html'
            title = 'Manage Workspace Members'
        else:
            name = 'list-members.html'
            title = 'Members'
        return Element('view',
                       name=name,
                       type='workspace',
                       title=title,
                       section='workspaces')

class WSMemberListBatchProvider(BatchProvider, MemberURLProfileMixin):
    """Batch Provider to Provide a Member Listing"""

    def query(self, params):
        items = []
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getAuthenticatedMember()
        wm = IWorkspaceMemberManagement(aq_parent(aq_inner(context)))
        isWorkspaceMember = wm.isWorkspaceMember(member)
        showEmail = not(not isWorkspaceMember or member is None or pmem.isAnonymousUser())
        workspacemembers = wm.listAllMembers()
        for member in workspacemembers:
            href = self._getProfileURLFor(member)
            organization = member.getProperty('organization')
            if organization is None:
                organization = 'None Given'
            items.append({'href': href,
                          'firstname':member.getProperty('firstname'),
                          'lastname':member.getProperty('lastname'),
                          'role': wm.isWorkspaceManager(member) and 'Manager' or 'Member',
                          'email':showEmail and member.getProperty('email') or '',
                          'organization':organization})
        sort_on='lastname'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class WSMemberListBatchFragment(BatchFragment):
    """ Batch Fragment fed by WSMemberListBatchProvider above"""
    def asElement(self):
        context = self.context
        request = self.request
        columns = (('lastname', {'default_order':'asc',
                                 'label': 'Last Name'}),
                   ('firstname', {'default_order':'asc',
                                  'label': 'First Name'}),
                   ('role', {'default_order':'asc',
                              'label': 'Role'}),
                   ('email', {'default_order':'asc',
                              'label': 'Email'}),
                   ('organization', {'default_order':'asc',
                                     'label': 'Organization'}),)

        batchfragment = BatchFragmentFactory(WSMemberListBatchProvider,
                                             columns = columns,)
        if request.get('sort_on', None) is None:
            request['sort_on'] = 'lastname'
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class MembershipManagementPage(Page):

    views = (MembershipManagementView, )

    def __call__(self):
        context = self.context
        request = self.request
        mt = cmfutils.getToolByName(context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        wm = IWorkspaceMemberManagement(aq_parent(aq_inner(context)))
        if wm and wm.isWorkspaceManager(member):
            self.views = self.views + COMMON_VIEWS
        else:
            self.views = self.views + (WSMemberListBatchFragment, ) + COMMON_VIEWS
        return super(MembershipManagementPage, self).__call__()

################################################
##  Code for workspace member mgmt page end   ##
################################################

class WorkspaceSubscriptionSuccessView(Fragment):
    """ view for workspaces subscription page """
    def asElement(Fragment):
        return Element('view',
                       name="subscribe.html",
                       type="workspace",
                       title='Subscribe To This Workspace',
                       section="workspaces"
                       )
        
class WorkspaceSubscriptionPage(Page):
    views = (WorkspaceSubscriptionSuccessView, ) + COMMON_VIEWS

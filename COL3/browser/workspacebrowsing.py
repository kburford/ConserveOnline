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
from Products.COL3.browser.member import MemberWorkspacesMixin
import logging
from urllib import quote_plus

from zExceptions import Redirect
from Acquisition import aq_inner
from zExceptions.unauthorized import Unauthorized
from Products.COL3.etree import Element, SubElement #@UnresolvedImport

from Products.CMFCore.utils import getToolByName

from Products.COL3.browser.base import Fragment
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.batch import BatchFragment
from Products.COL3.browser.base import Page
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.config import NATIONS, titleWithoutStopword
from Products.COL3.browser.base import ResultSet


class WorkspaceBrowserMenuFragment(Fragment):
    """ the menus items for the doc browser page"""
    """ Menu fragment for topic list view """

    _additems = (('Add Workspace', '@@add-workspace.html'), )
    _utilmenu_items = ()

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        self._utilmenu_items = self._generateUtilMenu(url)
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
                           href=url + '/' + relative_url).text = label
        url = context.absolute_url()
        if self._utilmenu_items:
            utilmenu = SubElement(menu_tag, 'utilitymenu', label="By:")
            for label, url in self._utilmenu_items:
                elem = SubElement(utilmenu, 'entry', href=url)
                elem.text = label
                if self._isSelected(label, self.request):
                    elem.attrib['current'] = 'current'
        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        return menu_tag

    def _generateUtilMenu(self, url):
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        if pmem.isAnonymousUser():
            return ((u'All', '%s/%s' % (url, 'all.html')),
                    (u'Regions/Countries', '%s/%s' % (url, 'bycountry.html')),
                    (u'Search Terms', '%s/%s' % (url, 'bysearchterm.html')),
                    )
        else:
            return ((u'My Workspaces','%s/%s' % (url, 'byauthuser.html')),
                    (u'Regions/Countries', '%s/%s' % (url, 'bycountry.html')),
                    (u'Search Terms', '%s/%s' % (url, 'bysearchterm.html')),
                    (u'All', '%s/%s' % (url, 'all.html')),)

    def _isSelected(self, label, request):
        pages = {'bycountry.html':'Regions/Countries',
                 'bysearchterm.html':'Search Terms',
                 'byauthuser.html':'My Workspaces',
                 'all.html':'All',}
        url = request.get('URL').split('/')
        url.reverse()
        return pages.has_key(url[0]) and pages[url[0]] == label

class WorkspaceBrowseByBatchFragment(BatchFragment):
    """ Batch fragment which is fed by custom batch above """
    letters_param='REMOVE'
    _browsebykey = ''
    _browsebylabel = ''
    _batchprovider = None
    def asElement(self):
        context = self.context
        request = self.request
        columns = ((self._browsebykey, {'default_order':'asc',
                                'label': self._browsebylabel}),
                   ('count', {'default_order':'asc',
                              'label': 'Count'}),)
        batchfragment = BatchFragmentFactory(self._batchprovider,
                                             columns = columns,
                                             letters_param=self.letters_param)
        if request.get('sort_on', None) is None:
            request['sort_on'] = self._browsebykey
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class WorkspaceBrowsingWithBatchFragment(BatchFragment):
    """ Batch fragment which is fed by the batch provider above """
    _batchprovider = None
    letters_param='REMOVE'
    def asElement(self):
        context = self.context
        request = self.request
        columns = (('title', {'default_order':'asc',
                              'label': 'Workspace Title'}),
                   ('dateupdated', {'default_order':'asc',
                                    'label': 'Date Updated'}),)
        batchfragment = BatchFragmentFactory(self._batchprovider,
                                             columns = columns,
                                             letters_param=self.letters_param)
        if request.get('sort_on', None) is None:
            request['sort_on'] = 'title'
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch


########################################################################
##                  Start WorkspaceListing Code                       ##
########################################################################

class WorkspaceListingViewFragment(Fragment):
    def asElement(self):
        return Element('view',
                       name='all-workspaces.html',
                       type='workspaces',
                       title='List All Workspaces',
                       section='workspaces')

class WorkspaceListingBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """
    def query(self, params):
        items = []
        sortable_values = {'title':'sortable_title',
                           'date':'modified',
                           'country':'getCountry',}
        context = self.context
        request = self.request
        pcat = getToolByName(context, 'portal_catalog')
        sort_on='sortable_title'
        ws_name_startswith = ''
        sort_order=''
        if params.get('sort_on'):
            sort_on = sortable_values.get(params.get('sort_on'), sort_on)
        if params.get('sort_order') == 'desc':
            sort_order = 'reverse'
        if request.get('startswith'):
            ws_name_startswith = request.get('startswith').lower()+'*'
        workspaces = pcat.searchResults(portal_type='Workspace',
                                        sort_on=sort_on,
                                        sort_order=sort_order,
                                        Title=ws_name_startswith)
        if ws_name_startswith:
            for workspace in workspaces:
                localTitle = titleWithoutStopword(workspace.Title)
                if localTitle and localTitle.lower().startswith(ws_name_startswith[:1]):
                    items.append({'href':workspace.getURL(),
                                  'title':workspace.Title,
                                  'date':workspace.modified.ISO8601(),
                                  'country':workspace.getCountry,
                                  })
        else:
            for workspace in workspaces:
                items.append({'href':workspace.getURL(),
                              'title':workspace.Title,
                              'date':workspace.modified.ISO8601(),
                              'country':workspace.getCountry,
                              })
        title_sort=('title', 'sortable_title')
        if sort_on in title_sort:
            if ws_name_startswith:
                items.sort(lambda a, b: cmp(
                    (titleWithoutStopword(a.get('title'))).lower(),
                    titleWithoutStopword(b.get('title')).lower()))
        return items


class WorkspaceListingBatchFragment(Fragment):
    def asElement(self):
        letters_param='startswith'
        context = self.context
        request = self.request
        columns = (('title', {'default_order':'asc',
                              'label': 'Title'}),
                   ('country', {'default_order':'asc',
                                'label': 'Region/Country'}),
                   ('date', {'default_order':'asc',
                             'label': 'Date Updated'}),)

        batchfragment = BatchFragmentFactory(WorkspaceListingBatchProvider,
                                             columns = columns,
                                             letters_param=letters_param)
        if request.get('sort_on', None) is None:
            request['sort_on'] = 'title'
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class WorkspaceListingPage(Page):
    views = (WorkspaceListingViewFragment,
             WorkspaceBrowserMenuFragment,
             WorkspaceListingBatchFragment,) + COMMON_VIEWS

########################################################################
##                  End WorkspaceListing Code                         ##
########################################################################

########################################################################
##              Start WorkspaceBrowseByCountry Code                   ##
########################################################################

class WorkspaceByCountryViewFragment(Fragment):
    """ name="bycountries-workspaces.html"
        type="workspaces"
        title="Browse Workspaces By Region/Country"
        section="workspaces"
    """
    def asElement(self):
        return Element('view',
                       name='bycountries-workspaces.html',
                       type='workspaces',
                       title='Browse Workspaces By Region/Country',
                       section='workspaces')

class WorkspaceByCountryBatchProvider(BatchProvider):
    """ Batch provider that provides a list of workspaces associated
        with a particular couintry
    """
    def query(self, params):
        items = []
        context = self.context
        pcat = getToolByName(context, 'portal_catalog')
        url = context.absolute_url()
        portal = context.portal_url.getPortalObject()
        workspaces_path = aq_inner(portal).getPhysicalPath() + ('workspaces',)
        cat_countries = pcat.uniqueValuesFor('getWorkspaceCountry')

        # We are only interested in the intersection
        intersection = set(cat_countries).intersection(set(NATIONS.by_value))

        # Keep a mapping from name -> data
        count_map = {}
        base = '%s/withcountry-workspaces.html?country=' % url
        for country in intersection:
            term = NATIONS.getTerm(country)
            count_map[country] = {'count': 0,
                                  'href': base + country,
                                  'country': term.title}

        # Don't merge the Result Set, since we are only interested
        # in the count and not in the Results.
        results = pcat.searchResults(
            _merge=False,
            portal_type='Workspace',
            path={'query': '/'.join(workspaces_path), 'depth': 1},
            getWorkspaceCountry=list(intersection))

        for item in results:
            count_map[item.getCountry]['count'] += 1

        items = count_map.values()

        sort_on='country'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))

        if params.get('sort_order') == 'desc':
            items.reverse()

        return items

class WorkspaceByCountryBatchFragment(WorkspaceBrowseByBatchFragment):
    """ Batch fragment which is fed by the batch provider above """
    _browsebykey = 'country'
    _browsebylabel = 'Region/Country'
    _batchprovider = WorkspaceByCountryBatchProvider

class WorkspaceByCountryPage(Page):
    """ Class that ties together all the fragments that make up the total
        xml for the view rendering
    """
    views = (WorkspaceByCountryViewFragment,
             WorkspaceBrowserMenuFragment,
             WorkspaceByCountryBatchFragment,) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'Browse Workspaces By Region/Country',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(WorkspaceByCountryPage, self).getResponse()

########################################################################
##                End WorkspaceBrowseByCountry Code                   ##
########################################################################

########################################################################
##            Start WorkspaceBrowseWithCountry Code                   ##
########################################################################

class WorkspaceWithCountryViewFragment(Fragment):
    """ name="withcountry-workspaces.html"
        type="workspaces"
        title="List Workspaces For Region/Country - United States of America"
        section="workspaces"
    """
    def asElement(self):
        countryId = NATIONS.getTerm(self.request.get('country'))
        return Element('view',
                       name="withcountry-workspaces.html" ,
                       type='workspaces',
                       title='List Workspaces For Region/Country - ' + countryId.title,
                       section='workspaces')

class WorkspaceWithCountryBatchProvider(BatchProvider):
    """ Batch provider that provides a list of countries and the number of
        workspaces associated with that country, countries with zero or less
        workspaces associated will not be returned
    """
    def query(self, params):
        items = []
        context = self.context
        request = self.request
        pcat = getToolByName(context, 'portal_catalog')
        url = context.absolute_url()
        workspaces = pcat.searchResults(portal_type='Workspace',
                                        getCountry=request.get('country'))
        for workspace in workspaces:
            href = url+ '/' + workspace.id
            items.append({'href':href,
                          'title':workspace.Title,
                          'dateupdated':workspace.modified.ISO8601(),})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'dateupdated':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class WorkspaceWithCountryBatchFragment(WorkspaceBrowsingWithBatchFragment):
    """ Batch fragment which is fed by the batch provider above """
    _batchprovider = WorkspaceWithCountryBatchProvider

class WorkspaceWithCountryPage(Page):
    """ Class that ties together all the fragments that make up the total
        xml for the view rendering
    """
    views = (WorkspaceWithCountryViewFragment,
             WorkspaceWithCountryBatchFragment,) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        country = 'Region/Country Not Found'
        try:
            countryId = NATIONS.getTerm(self.request.get('country'))
            country = countryId.title
        except LookupError, le:
            error = '%s%s%s' % (le.__class__.__name__, ":", str(le))
            logger = logging.getLogger('Products.COL3.browser.workspacebrowsing')
            logger.error('***** '+error+' *****')
        self.xtra_breadcrumb_ids = ({'title':'List Workspaces For Region/Country - '+country,
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(WorkspaceWithCountryPage, self).getResponse()

########################################################################
##           End WorkspaceBrowseWithCountryCountry Code               ##
########################################################################

########################################################################
##              Start WorkspaceBrowseBySearchterm Code                   ##
########################################################################

class WSBrowseBySearchtermViewFragment(Fragment):
    """ name="bysearchterms-workspaces.html"
        type="workspaces"
        title="Browse Workspaces by Search Terms"
        section="workspaces"
        NOTE - this used to be called WSBrowseByKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def asElement(self):
        return Element('view',
                       name="bysearchterms-workspaces.html" ,
                       type='workspaces',
                       title='Browse Workspaces by Search Terms',
                       section='workspaces')

class WSBrowseBySearchtermBatchProvider(BatchProvider):
    """ Batch provider that provides a list of searchterms and the number of
        workspaces associated with that searchterm, searchterms with zero or less
        workspaces associated will not be returned
        NOTE - this used to be called WSBrowseByKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def query(self, params):
        items = []
        context = self.context
        url = context.absolute_url()
        portal = context.portal_url.getPortalObject()
        workspaces_path = aq_inner(portal).getPhysicalPath() + ('workspaces',)
        pcat = getToolByName(context, 'portal_catalog')
        keywords = pcat.uniqueValuesFor('getWorkspaceKeywords')

        # Keep the total number of keywords around, will be used for
        # returning the 'result set' object.
        total = len(keywords)

        # Restrict keywords to only those required for the batch.
        keywords = keywords[params['start']:params['end']]

        # Keep a mapping from name -> data
        count_map = {}
        base = '%s/withsearchterm-workspaces.html?searchterm=' % url
        for keyword in keywords:
            count_map[keyword] = {'count': 0,
                                  'href': base + quote_plus(keyword),
                                  'searchterm': keyword}

        # Don't merge the Result Set, since we are only interested
        # in the count and not in the Results.
        results = pcat.searchResults(
            _merge=False,
            portal_type='Workspace',
            path={'query': '/'.join(workspaces_path), 'depth': 1},
            getWorkspaceKeywords=keywords)

        for item in results:
            for keyword in item.getKeywords:
                if not count_map.has_key(keyword):
                    # An item might have multiple keywords, some of
                    # which will *not* be selected for this batch,
                    # so we skip counting them.
                    continue
                count_map[keyword]['count'] += 1

        items = count_map.values()

        sort_on='searchterm'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()

        return ResultSet(items, total)

class WSBrowseBySearchtermBatchFragment(WorkspaceBrowseByBatchFragment):
    """ Batch fragment which is fed by the batch provider above
        NOTE - this used to be called WSBrowseByKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    _browsebykey = 'searchterm'
    _browsebylabel = 'Search Term'
    _batchprovider = WSBrowseBySearchtermBatchProvider

class WSBrowseBySearchtermPage(Page):
    """ Class that ties together all the fragments that make up the total
        xml for the view rendering
        NOTE - this used to be called WSBrowseByKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    views = (WSBrowseBySearchtermViewFragment,
             WorkspaceBrowserMenuFragment,
             WSBrowseBySearchtermBatchFragment,) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'Browse Workspaces By Search Term',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(WSBrowseBySearchtermPage, self).getResponse()

########################################################################
##             End WorkspaceBrowseBySearchterm Code                   ##
########################################################################

########################################################################
##             Start WorkspaceBrowseBySearchterm Code                 ##
########################################################################

class WSBrowseWithSearchtermViewFragment(Fragment):
    """ name="withsearchterm-workspaces.html"
        type="workspaces"
        title="List Workspaces For Search Term - Rainforests"
        section="workspaces"
        NOTE - this used to be called WSBrowseWithKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def asElement(self):
        return Element('view',
                       name="withsearchterm-workspaces.html" ,
                       type='workspaces',
                       title='List Workspaces For Search Term - '+self.request.get('searchterm'),
                       section='workspaces')

class WSBrowseWithSearchtermBatchProvider(BatchProvider):
    """ Batch provider that provides a list of workspaces associated
        with a particular searchterm
        NOTE - this used to be called WSBrowseWithKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def query(self, params):
        items = []
        context = self.context
        request = self.request
        pcat = getToolByName(context, 'portal_catalog')
        url = context.absolute_url()
        workspaces = pcat.searchResults(portal_type='Workspace',
                                        getKeywords=request.get('searchterm'))
        for workspace in workspaces:
            href = url + '/' + workspace.id
            items.append({'href':href,
                          'title':workspace.Title,
                          'dateupdated':workspace.modified.ISO8601(),})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'dateupdated':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class WSBrowseWithSearchtermBatchFragment(WorkspaceBrowsingWithBatchFragment):
    """ NOTE - this used to be called WSBrowseWithKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    _batchprovider = WSBrowseWithSearchtermBatchProvider

class WSBrowseWithSearchtermPage(Page):
    """ Class that ties together all the fragments that make up the total
        xml for the view rendering
        NOTE - this used to be called WSBrowseWithKeywordXXX.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    views = (WSBrowseWithSearchtermViewFragment,
             WSBrowseWithSearchtermBatchFragment,) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'List Workspaces For Search Term - '+self.request.get('searchterm'),
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(WSBrowseWithSearchtermPage, self).getResponse()

########################################################################
##                End WorkspaceBrowseWithSearchterm Code              ##
########################################################################

########################################################################
##                   Start BrowseMyWorkspaces Code                    ##
########################################################################

class BrowseMyWorkspacesViewFragment(Fragment):
    """ name="browsemine-workspaces.html"
        type="workspaces"
        title="Browse My Workspaces"
        section="workspaces"
    """
    def asElement(self):
        return Element('view',
                       name='browsemine-workspaces.html',
                       type='workspaces',
                       title='Browse My Workspaces',
                       section='workspaces')

class BrowseMyWorkspacesBatchProvider(BatchProvider, MemberWorkspacesMixin):
    """ Batch provider that provides a list of workspaces associated
        with a particular keyword
    """
    def query(self, params):
        items = []
        workspacesadded = []
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        authmember = pmem.getAuthenticatedMember()
        if authmember:
            mgr_ws_ids, member_ws_ids = self._getMemberWorkspaceIds(authmember)
            if mgr_ws_ids or member_ws_ids:
                mgrworkspaces = self._workspaceRecordsFromIds(mgr_ws_ids)
                memberworkspaces = self._workspaceRecordsFromIds(member_ws_ids)
                querystr = context.absolute_url()+'/%s'
                for workspace in mgrworkspaces:
                    href = querystr % workspace.id
                    items.append({'href':href,
                                  'title':workspace.Title,
                                  'dateupdated':workspace.modified.ISO8601(),})
                    workspacesadded.append(workspace.Title)
                for workspace in memberworkspaces:
                    try:
                        workspacesadded.index(workspace.Title)
                    except ValueError:
                        href = querystr % workspace.id
                        items.append({'href':href,
                                      'title':workspace.Title,
                                      'dateupdated':workspace.modified.ISO8601(),})
            sort_on='title'
            if params.get('sort_on'):
                sort_on = params.get('sort_on')
            if sort_on == 'dateupdated':
                items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
            else:
                items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
            if params.get('sort_order') == 'desc':
                items.reverse()
        return items

class BrowseMyWorkspacesBatchFragment(WorkspaceBrowsingWithBatchFragment):
    """ Batch fragment which is fed by the batch provider above """
    _batchprovider = BrowseMyWorkspacesBatchProvider

class BrowseMyWorkspacesPage(Page):
    """ Class that ties together all the fragments that make up the total
        xml for the view rendering
    """
    views = (BrowseMyWorkspacesViewFragment,
             WorkspaceBrowserMenuFragment,
             BrowseMyWorkspacesBatchFragment,) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        if pmem.isAnonymousUser():
            raise Redirect(context.absolute_url()+'/all.html')
        self.xtra_breadcrumb_ids = ({'title':'Browse My Workspaces',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(BrowseMyWorkspacesPage, self).getResponse()

########################################################################
##                     End BrowseMyWorkspaces Code                    ##
########################################################################

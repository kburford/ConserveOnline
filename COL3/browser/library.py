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

import Missing
from urllib import quote_plus
from itertools import islice
from DateTime import DateTime
from zope import interface
from zope.formlib import form
from zope.component import queryMultiAdapter #@UnresolvedImport
from Products.COL3.etree import Element, SubElement
from Acquisition import aq_inner, aq_chain
from zExceptions.unauthorized import Unauthorized
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note

from contentratings.interfaces import IUserRating
from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.browser.base import Page
from Products.COL3.browser.base import Fragment
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.common import BaseBatchFragment, BatchFragmentFactory
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.browser.helper import _calculateSize
from Products.COL3.content.indexer import index as gsa_index
from Products.COL3.content.indexer import reindex as gsa_reindex
from Products.COL3.formlib.xmlform import AddFormFragment, EditFormFragment
from Products.COL3.interfaces.file import IGISDataFile
from Products.COL3.interfaces.library import ILibraryFileSchema, ILibraryFileEditSchema
from Products.COL3.content.base import generateOID, idFromTitle
from Products.COL3.config import MIMETYPES, titleWithoutStopword
from Products.COL3.content.label import Labeller
from Products.COL3.browser.base import ResultSet

#=============================================================================
#                         Start LibraryByAll Code
#=============================================================================

class LibraryViewAllViewFragment(Fragment):
    """view fragment for view all in library view"""
    def asElement(self):
        return Element('view',
                       name="bysearchterms.html",
                       type="library",
                       title="Browse All Library" ,
                       section="library",)

class LibraryViewAllMenuFragment(Fragment):
    """ the menus items for the doc browser page"""
    """ Menu fragment for topic list view """

    _addmenu_items = ((u'Add File', '@@add-libraryfile.html'),)
    _utilmenu_items = ()

    def asElement(self):
        context = self.context
        portal = context.portal_url.getPortalObject()
        portalurl = aq_inner(portal).absolute_url()
        self._utilmenu_items = self._generateUtilMenu(portalurl)
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        addmenu_tag = Element('addmenu')
        url = context.absolute_url()
        for label, relative_url in self._addmenu_items:
            try:
                context.restrictedTraverse(relative_url)
            except (Unauthorized, AttributeError):
                pass
            else:
                SubElement(addmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label
        if self._utilmenu_items:
            utilmenu = SubElement(menu_tag, 'utilitymenu', label="By:")
            for label, url in self._utilmenu_items:
                elem = SubElement(utilmenu, 'entry', href=url)
                elem.text = label
                if self._isSelected(label, self.request):
                    elem.attrib['current'] = 'current'
        if addmenu_tag:
            # do not append if empty
            menu_tag.append(addmenu_tag)
        return menu_tag

    def _generateUtilMenu(self, url):
        return ((u'Search Terms','%s/library/%s' % (url, 'bysearchterms.html')),
                (u'Authors', '%s/library/%s' % (url, 'byauthor.html')),
                (u'Recently Added', '%s/library/%s' % (url, 'byrecentadded.html')),
                (u'All', '%s/library/%s' % (url, 'byall.html')),)

    def _isSelected(self, label, request):
        pages = {'bysearchterms.html':'Search Terms',
                 'byauthor.html':'Authors',
                 'byrecentadded.html':'Recently Added',
                 'byall.html':'All',}
        url = request.get('URL').split('/')
        url.reverse()
        return pages.has_key(url[0]) and pages[url[0]] == label

class LibraryWithItemMenuFragment(LibraryViewAllMenuFragment):
    """This is for all the withXXXX views so the utility menu doesn't get added"""
    _addmenu_items = ()
    _utilmenu_items = ()
    def _generateUtilMenu(self, url):
        return self._utilmenu_items

class LibraryViewAllBatchProvider(BatchProvider):
    """ Batch provider to return all documents in the library as a batch """
    def query(self, params):
        items = []
        filename_startswith = ''
        context = self.context
        request = self.request
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        pcat = getToolByName(context, 'portal_catalog')

        if request.get('startswith'):
            filename_startswith = request.get('startswith').lower()+'*'

        # Don't merge, we do the sorting ourselves below.
        results = pcat.searchResults(
            path={'query': '/'.join(library_path),
                  'depth': 1},
            Title=filename_startswith)

        for result in results:
            if filename_startswith:
                try:
                    localTitle = titleWithoutStopword(result.Title)
                except AttributeError:
                    result = result[2](result[1][2])
                    localTitle = titleWithoutStopword(result.Title)
                if not localTitle.lower().startswith(filename_startswith[:1]):
                    continue
            mimetype = MIMETYPES.get(result.getContentType, 'No Mapping')
            if result.is_folderish:
                mimetype = 'folder'
            authored = result.getDateauthored
            if authored == Missing.Value or not authored:
                authored = result.created
            items.append({'href':'%s/view.html' % result.getURL(),
                          'mimetype':mimetype,
                          'title':result.Title and result.Title or result.id,
                          'size':_calculateSize(result.getObjSize),
                          'date': authored.ISO8601()})

        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        ## This code will not win any awards for it's elegance, but it works just fine...BJS
        if sort_on == 'size': #it's a number, just pass it to the cmp function
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            if filename_startswith: #it's a string, and we have to ignore the stopword at the beginning
                                    #of the filename if the filename begins with a stop word
                items.sort(lambda a, b: cmp(titleWithoutStopword(a.get(sort_on)).lower(),
                                            titleWithoutStopword(b.get(sort_on)).lower()))
            else: #we just deal with this as a plain old string and pass it as is to the cmp function
                items.sort(lambda a, b: cmp(a.get(sort_on).lower(),
                                            b.get(sort_on).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class LibraryViewAllBatchFragment(Fragment):
    """ Batch fragment that is fed by the batch provider above """
    def asElement(self):
        context = self.context
        request = self.request
        columns = (('title', {'default_order':'asc',
                              'label': 'Title'}),
                  ('mimetype', {'default_order':'asc',
                               'label': 'Format'}),
                  ('size', {'default_order':'asc',
                            'label': 'Size'}),
                  ('date', {'default_order':'asc',
                            'label': 'Date Contributed'}),)
        batchfragment = BatchFragmentFactory(LibraryViewAllBatchProvider,
                                             columns = columns,
                                             letters_param='startswith')
        if request.get('sort_on', None) is None:
            request['sort_on'] = 'title'
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class LibraryViewAllPage(Page):
    """ The page that collects all the fragments """
    views = (LibraryViewAllViewFragment,
             LibraryViewAllBatchFragment,
             LibraryViewAllMenuFragment, ) + COMMON_VIEWS

#=============================================================================
#                         End LibraryByAll Code
#=============================================================================

#=============================================================================
#                       Start LibraryByAuthor Code
#=============================================================================
class LibraryByAuthorViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="byauthors.html",
                       title="Browse Library By Authors",
                       type="library",
                       section="library"
                       )

class LibraryByAuthorBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    def query(self, params):
        context = self.context
        request = self.request
        pcat = getToolByName(context, 'portal_catalog')
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        authors = pcat.uniqueValuesFor('getLibraryAuthors')

        if request.get('startswith'):
            # Filter authors on 'startswith'
            match = request.get('startswith').lower()
            authors = [a for a in authors if a.lower().startswith(match)]

        # Keep the total number of authors around, will be used for
        # returning the 'result set' object.
        total = len(authors)

        # Restrict author names to only those required for the batch.
        authors = authors[params['start']:params['end']]

        # Keep a mapping from name -> data
        count_map = {}
        qs = '/library/withauthor-library.html?author='
        base = aq_inner(portal).absolute_url() + qs
        for author in authors:
            count_map[author] = {'count': 0,
                                 'href': base + quote_plus(author),
                                 'name': author}

        # Don't merge the Result Set, since we are only interested
        # in the count and not in the Results.
        results = pcat.searchResults(
            _merge=False,
            path={'query': '/'.join(library_path),
                  'depth': 1},
            getLibraryAuthors=authors)

        for item in results:
            for author in item.getAuthors:
                if not count_map.has_key(author):
                    # A LibraryFile might have multiple authors, some
                    # of which will *not* be selected for this batch,
                    # so we skip counting them.
                    continue
                count_map[author]['count'] += 1

        items = count_map.values()
        sort_on='name'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return ResultSet(items, total)


class LibraryByAuthorBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = 'name'
    letters_param='startswith'
    columns = (('name', {'default_order':'asc',
                         'label': 'Name'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    batch_provider = LibraryByAuthorBatchProvider

class LibraryByAuthorPage(Page):
    """ The one class to rule them all and in the xslt bind them """
    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Library By Authors',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(LibraryByAuthorPage, self).__init__(context, request)

    views = (LibraryByAuthorViewFragment,
             LibraryByAuthorBatchFragment,
             LibraryViewAllMenuFragment) + COMMON_VIEWS

#=============================================================================
#                       End LibraryByAuthor Code
#=============================================================================

#=============================================================================
#                       Start LibraryWithAuthor Code
#=============================================================================
class LibraryWithAuthorViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="withauthor-library.html",
                       title="Documents Matching Author - "+self.request.get('author', ''),
                       type="library",
                       section="library"
                       )

class LibraryWithAuthorBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    def query(self, params):
        items = []
        context = self.context
        author = self.request.get('author', '')
        pcat = getToolByName(context, 'portal_catalog')
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        if author:
            results = pcat.searchResults(
                path = {'query': '/'.join(library_path),
                        'depth': 1},
                getAuthors=author)
            for result in results:
                mimetype = MIMETYPES.get(result.getContentType, 'No Mapping')
                dateAuthored = result.getDateauthored
                dateAuthored = dateAuthored and dateAuthored.ISO8601() or result.created.ISO8601()
                items.append({'href': '%s/view.html' % result.getURL(),
                              'title':result.Title,
                              'mimetype':mimetype,
                              'size':_calculateSize(result.getObjSize),
                              'date':dateAuthored})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'size':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class LibraryWithAuthorBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = 'title'
    columns = (('title', {'default_order':'asc',
                         'label': 'Title'}),
               ('mimetype', {'default_order':'asc',
                             'label': 'Format'}),
               ('size', {'default_order':'asc',
                         'label': 'Size'}),
               ('date', {'default_order':'asc',
                         'label': 'Date Contributed'}),)
    batch_provider = LibraryWithAuthorBatchProvider

class LibraryWithAuthorPage(Page):
    """ The one class to rule them all and in the xslt bind them """
    def __init__(self, context, request):
        author = request.get('author', '')
        self.xtra_breadcrumb_ids = ({'title':'Library Documents By Author - '+author,
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(LibraryWithAuthorPage, self).__init__(context, request)

    views = (LibraryWithAuthorViewFragment,
             LibraryWithAuthorBatchFragment, ) + COMMON_VIEWS

#=============================================================================
#                       End LibraryWithAuthor Code
#=============================================================================

#=============================================================================
#                       Start LibraryBySearchterms Code
#=============================================================================
class LibraryBySearchtermsViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="bysearchterms.html",
                       title="Browse Library By Search Terms",
                       type="library",
                       section="library"
                       )

class LibraryBySearchtermsBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    def query(self, params):
        context = self.context
        request = self.request
        pcat = getToolByName(context, 'portal_catalog')
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        keywords = pcat.uniqueValuesFor('getLibraryKeywords')

        if request.get('startswith'):
            # Filter keywords on 'startswith'
            match = request.get('startswith').lower()
            keywords = [a for a in keywords if a.lower().startswith(match)]

        # Keep the total number of keywords around, will be used for
        # returning the 'result set' object.
        total = len(keywords)

        # Restrict keywords to only those required for the batch.
        keywords = keywords[params['start']:params['end']]

        # Keep a mapping from name -> data
        count_map = {}
        qs = '/library/withsearchterm-library.html?searchterm='
        base = aq_inner(portal).absolute_url() + qs
        for keyword in keywords:
            count_map[keyword] = {'count': 0,
                                  'href': base + quote_plus(keyword),
                                  'searchterm': keyword}

        # Don't merge the Result Set, since we are only interested
        # in the count and not in the Results.
        results = pcat.searchResults(
            _merge=False,
            path={'query': '/'.join(library_path),
                  'depth': 1},
            getLibraryKeywords=keywords)

        for item in results:
            try:
                for keyword in item.getKeywords:
                    if not count_map.has_key(keyword):
                        # A LibraryFile might have multiple authors, some
                        # of which will *not* be selected for this batch,
                        # so we skip counting them.
                        continue
                    count_map[keyword]['count'] += 1
            except AttributeError:
                continue
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

class LibraryBySearchtermsBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = 'searchterm'
    columns = (('searchterm', {'default_order':'asc',
                         'label': 'Name'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    letters_param = 'startswith'
    batch_provider = LibraryBySearchtermsBatchProvider

class LibraryBySearchtermsPage(Page):
    """ The one class to rule them all and in the xslt bind them """
    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Library By Search Terms',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(LibraryBySearchtermsPage, self).__init__(context, request)

    views = (LibraryBySearchtermsViewFragment,
             LibraryBySearchtermsBatchFragment,
             LibraryViewAllMenuFragment) + COMMON_VIEWS

#=============================================================================
#                       End LibraryByAuthor Code
#=============================================================================

#=============================================================================
#                       Start LibraryWithAuthor Code
#=============================================================================
class LibraryWithSearchtermViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="withsearchterm-library.html",
                       title="Documents Matching Search Term - "+self.request.get('searchterm', ''),
                       type="library",
                       section="library"
                       )

class LibraryWithSearchtermBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    def query(self, params):
        items = []
        context = self.context
        searchterm = self.request.get('searchterm', '')
        pcat = getToolByName(context, 'portal_catalog')
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        if searchterm:
            results = pcat.searchResults(
                path={'query': '/'.join(library_path),
                      'depth': 1},
                getKeywords=searchterm)
            for result in results:
                mimetype = MIMETYPES.get(result.getContentType, 'No Mapping')
                dateAuthored = result.getDateauthored
                # use create date if authored date is missing -- bwm per jadams
                dateAuthored = dateAuthored and dateAuthored.ISO8601() or result.created.ISO8601()
                docsize = _calculateSize(result.getObjSize)
                items.append({'href': '%s/view.html' % result.getURL(),
                              'title':result.Title,
                              'mimetype':mimetype,
                              'size':docsize,
                              'date':dateAuthored})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'size':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class LibraryWithSearchtermBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = 'title'
    columns = (('title', {'default_order':'asc',
                         'label': 'Title'}),
               ('mimetype', {'default_order':'asc',
                             'label': 'Format'}),
               ('size', {'default_order':'asc',
                         'label': 'Size'}),
               ('date', {'default_order':'asc',
                         'label': 'Date Contributed'}),)
    batch_provider = LibraryWithSearchtermBatchProvider

class LibraryWithSearchtermPage(Page):
    """ The one class to rule them all and in the xslt bind them """
    def __init__(self, context, request):
        searchterm = request.get('searchterm', '')
        self.xtra_breadcrumb_ids = ({'title':'Library Documents By Search Term - '+searchterm,
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(LibraryWithSearchtermPage, self).__init__(context, request)

    views = (LibraryWithSearchtermViewFragment,
             LibraryWithSearchtermBatchFragment, ) + COMMON_VIEWS

#=============================================================================
#                       End LibraryWithSearchterm Code
#=============================================================================

#=============================================================================
#                       Start LibraryByRecentlyAdded Code
#=============================================================================
class LibraryByRecentlyAddedViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="recentadded.html",
                       title="Browse Library By Recently Added",
                       type="library",
                       section="library"
                       )

class LibraryByRecentlyAddedBatchProvider(BatchProvider):
    """ Provides a list of two columns the first column is the 'when' (i.e. Past X Days or Today)
        and a count column indicating how many files have been added in the past X number of days
    """

    def query(self, params):
        items = []
        offsets = (('Today',0),
                   ('Past 7 Days',7),
                   ('Past 30 Days',30),
                   ('Past 90 Days',90),
                   ('Past 180 Days',180))
        context = self.context
        today = DateTime(DateTime().Date())
        pcat = getToolByName(context, 'portal_catalog')
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        for label, offset in offsets:
            # Don't merge the Result Set, since we are only interested
            # in the count and not in the Results.
            results = pcat.searchResults(
                _merge=False,
                path={'query': '/'.join(library_path),
                      'depth':1},
                created={'query':(today-offset),
                         'range':'min'})
            querystr = '/library/withrecent-library.html?offset='+str(offset)
            items.append({'href':(aq_inner(portal)).absolute_url()+querystr,
                          'when':label,
                          'count':len(results)})
        return items


class LibraryByRecentlyAddedBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = ''
    columns = (('when', {'default_order':'',
                         'label': 'When'}),
               ('count', {'default_order':'',
                          'label': 'Count'}),)
    batch_provider = LibraryByRecentlyAddedBatchProvider

class LibraryByRecentlyAddedPage(Page):
    """ The one class to rule them all and in the xslt bind them """
    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Library By Recently Added',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(LibraryByRecentlyAddedPage, self).__init__(context, request)

    views = (LibraryByRecentlyAddedViewFragment,
             LibraryByRecentlyAddedBatchFragment,
             LibraryViewAllMenuFragment) + COMMON_VIEWS

#=============================================================================
#                       End LibraryByRecentlyAdded Code
#=============================================================================

#=============================================================================
#                       Start LibraryWithRecentlyAdded Code
#=============================================================================
class LibraryWithRecentlyAddedViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        offsets = {'0':'Today',
                   '7':'Past 7 Days',
                   '30':'Past 30 Days',
                   '90':'Past 90 Days',
                   '180':'Past 180 Days'}
        offset = self.request.get('offset')
        if not offset:
            offset = '180'
        return Element('view',
                       name="byrecentlibrary.html",
                       title="Browse Library Matching Recent Added - "+offsets[offset],
                       type="library",
                       section="library"
                       )

class LibraryWithRecentlyAddedBatchProvider(BatchProvider):
    """ Provides a library files created in the past n number of days, specified by the offset """

    def query(self, params):
        items = []
        context = self.context
        request = self.request
        if request.get('offset'):
            offset = int(request.get('offset'))
        else: #XXX if we get here by mistake with no offset in query return last 180 days?
            offset = 180
        today = DateTime(DateTime().Date())
        pcat = getToolByName(context, 'portal_catalog')
        portal = context.portal_url.getPortalObject()
        library_path = aq_inner(portal).getPhysicalPath() + ('library', )
        results = pcat.searchResults(path={'query': '/'.join(library_path),'depth':1},
                                     created={'query':(today-offset), 'range':'min'})
        for result in results:
            mimetype = MIMETYPES.get(result.getContentType, 'No Mapping')
            dateAuthored = result.getDateauthored
            # use create date if author date is missing -- bwm per jadams
            dateAuthored = dateAuthored and dateAuthored.ISO8601() or result.created.ISO8601()
            if result.Type == 'LibraryFile':
                items.append({'href': '%s/view.html' % result.getURL(),
                              'title':result.Title,
                              'mimetype':mimetype,
                              'size':_calculateSize(result.getObjSize),
                              'date':dateAuthored})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'size':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class LibraryWithRecentlyAddedBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = 'title'
    columns = (('title', {'default_order':'asc',
                         'label': 'Title'}),
               ('mimetype', {'default_order':'asc',
                             'label': 'Format'}),
               ('size', {'default_order':'asc',
                         'label': 'Size'}),
               ('date', {'default_order':'asc',
                         'label': 'Date Contributed'}),)
    batch_provider = LibraryWithRecentlyAddedBatchProvider

class LibraryWithRecentlyAddedPage(Page):
    """ The one class to rule them all and in the xslt bind them """
    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Library By Recently Added',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(LibraryWithRecentlyAddedPage, self).__init__(context, request)

    views = (LibraryWithRecentlyAddedViewFragment,
             LibraryWithRecentlyAddedBatchFragment,) + COMMON_VIEWS

#=============================================================================
#                       End LibraryWithRecentlyAdded Code
#=============================================================================

class LibraryFileAddForm(AddFormFragment):

    form_fields = form.FormFields(ILibraryFileSchema)

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)
        unique_id=idFromTitle(title=data['title'], container=context)
        # code taken from plone_scripts/createObject:
        new_id = context.invokeFactory(id=unique_id, type_name='LibraryFile')
        if not new_id:
           new_id = unique_id
        obj = context[new_id]
        transaction_note('Created %s with id %s in %s' %
                         (obj.getTypeInfo().getId(), new_id,
                          context.absolute_url()))
        # end code taken from plone_scripts/createObject
        data['oid'] = generateOID(container=context)
        obj.update(**data)
        crossref_tool = getToolByName(self.context, 'crossreference_tool')
        crossref_tool.queueLibraryFile(obj)
        gsa_index(obj)

        return obj.absolute_url() + "/@@view.html"

    def cancelURL(self):
        return self.context.absolute_url()

class LibraryFileAddView(Fragment):
    """ View fragment for file add views
    """

    def asElement(self):
        # <view name="add.html" type="libraryfile" title="Add Library File"
        # section="library"/>
        return Element('view',
                       name="add.html",
                       type="libraryfile",
                       title="Add Library File",
                       section="library")

class LibraryFileAddPage(Page):

    views = (LibraryFileAddView, LibraryFileAddForm, ) + COMMON_VIEWS

class LibraryFileEditForm(EditFormFragment):

    form_fields = form.FormFields(ILibraryFileEditSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        data = {'file':None}
        for field in self.form_fields.omit('file'):
            name = field.__name__
            __traceback_info__ = name
            accessor = context.getField(name).getAccessor(context)
            value = accessor()
            data[name] = value
        return data

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        if data['file'] is None:
            # if no file upload, don't change anything
            del data['file']
        if data['gisdata'] is None:
            del data['gisdata']
        context.update(**data)
        gsa_reindex(context)
        return context.absolute_url() + "/view.html"

    def cancelURL(self):
        return self.context.absolute_url() + "/view.html"


class LibraryFileEditView(Fragment):
    """ View fragment for file edit views
    """

    def asElement(self):
        # <view name="edit.html" type="libraryfile"
        #       title="Edit Library File: Some File" section="library"/>
        return Element('view',
                       name="edit.html",
                       type="libraryfile",
                       title="Edit Library File: " + self.context.Title(),
                       section="library")

class LibraryFileEditPage(Page):

    views = (LibraryFileEditView, LibraryFileEditForm, ) + COMMON_VIEWS

class LibraryFileViewView(Fragment):
    """ View class for viewing files
    """

    def asElement(self):
        #<view name="view.html" type="libraryfile"
        #       title="My Library File Title" section="library"/>
        return Element('view',
                       name="view.html",
                       type="libraryfile",
                       title=self.context.Title(),
                       section="library")

class LibraryFileViewActionMenu(Fragment):

    _actionmenu_entries = (# title, relative-url
                           (u'Edit', "edit.html"),
                           (u'Delete', "delete.html"),
                           )

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('actionmenu')
        for label, relative_url in self._actionmenu_entries:
            if queryMultiAdapter((context, self.request),
                                 name=relative_url) is None:
                continue # skip unavailable views
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
        if menu_tag:
            # do not return empty elements
            return menu_tag


class RatingFragment(Fragment):
    """ Most Popular topics and topics batch """
    def asElement(self):
        manager = IUserRating(self.context)
        root = Element('ratings')
        count_tag = Element('count')
        count_tag.text = str(manager.numberOfRatings)
        root.append(count_tag)
        score_tag = Element('score')
        # 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, ..., 5.0
        score = round(manager.averageRating*2)/2
        # 00, 05, 10, 15, 20, 25, ... 50
        score_tag.text = str(score).replace('.', '')
        root.append(score_tag)
        return root


class LibraryFileViewPage(Page):

    views = (LibraryFileViewView,
             RatingFragment,
             LibraryFileViewActionMenu, ) + COMMON_VIEWS



class WorkspaceLibraryFileAddForm(AddFormFragment):

    form_fields = form.FormFields(ILibraryFileSchema).omit('file')

    def getLabelInstance(self):
        for label in Labeller(self.context).getLabelInstancesForContent(self.context):
            # get the first one only
            return label
        # returns None ir there are no labels

    def getWorkspace(self):
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                return ob

    label_fields = set('''language country biogeographic_realm habitat
                       conservation directthreat organization monitoring
                       keywords text'''.split())
    workspace_fields = set('''country biogeographic_realm habitat conservation
                           conservation directthreat organization monitoring
                           description license'''.split())
    def provideInitialDefaults(self):
        """ Provide initial suggestion for values based on the file primary
        label and on the workspace, in this order"""
        # get the title default from this file
        defaults = {'title':self.context.Title()}

        label = self.getLabelInstance() #Label is now Keyword on the frontend
        try:
            label_schema = label.Schema()
        except AttributeError:
            pass #this means that the doc was imported and has no Keywords

        workspace = self.getWorkspace()
        workspace_schema = workspace.Schema()
        # calculate the defaults
        for field in self.form_fields:
            name = field.__name__
            value = None
            # try to get the value from the label
            if (label is not None and
                name in self.label_fields and
                name in label_schema):
                accessor = label_schema[name].getAccessor(label)
                value = accessor()
            # and then from the workspace, if couldn't get meaningful value
            # from the label
            if (not value and
                name in self.workspace_fields and
                name in workspace_schema):
                accessor = workspace_schema[name].getAccessor(workspace)
                value = accessor()
            # if we got anything maningful (not None AND not empty) set as
            # default for the field
            if value:
                defaults[name] = value
        return defaults

#    def becomePortalOwner(self):
#        portal = self.getPortal()
#        owner = portal.getWrappedOwner()
#        self._current_user = getSecurityManager().getUser()
#        newSecurityManager(self.request, owner)
#
#    def unbecomePortalOwner(self):
#        newSecurityManager(self.request, self._current_user)
#        del self._current_user
#
    def getPortal(self):
        return getToolByName(aq_inner(self.context),
                             'portal_url').getPortalObject()

    def createAddAndReturnURL(self, data):
        library = self.getPortal()['library']

        unique_id=idFromTitle(title=data['title'], container=library)

        # code taken from plone_scripts/createObject:
        new_id = library.invokeFactory(id=unique_id, type_name='LibraryFile')
        if not new_id:
           new_id = unique_id
        library_file_obj = library[new_id]
        transaction_note('Created %s with id %s in %s' %
                         (library_file_obj.getTypeInfo().getId(), new_id,
                          library.absolute_url()))
        # end code taken from plone_scripts/createObject
        oid = generateOID(container=library_file_obj)
        self.context.setLibraryreference(library_file_obj.UID())
        #file = self.context.getFile()
        library_file_obj.setFile(self.context.getFile())
        data['oid'] = oid
        self.context.setAuthors(data['authors'])
        if data.get('gisdata'):
            gisdata = data.get('gisdata')
            del data['gisdata']
            library_file_obj.setGisdata(gisdata, mimetype='application/octet-stream')
            interface.directlyProvides(library_file_obj.getGisdata(), IGISDataFile)
        library_file_obj.update(**data)
        crossref_tool = getToolByName(self.context, 'crossreference_tool')
        crossref_tool.queueLibraryFile(library_file_obj)
        gsa_index(library_file_obj)
        return self.context.absolute_url() + "/@@view.html"

    def cancelURL(self):
        return self.context.absolute_url() + "/@@view.html"

class WorkspaceLibraryFileAddView(Fragment):
    """ View fragment for file add views
    """

    def asElement(self):
        return Element('view',
                       name="addtolibrary-file.html",
                       type="file",
                       title="Add to Library: " + self.context.Title(),
                       section="workspaces")

class WorkspaceLibraryFileAddPage(Page):
    """ Page to tie together fragments for add workspace file to library """
    views = (WorkspaceLibraryFileAddView,
             WorkspaceLibraryFileAddForm, ) + COMMON_VIEWS

class WorkspaceLibraryFileUpdateForm(AddFormFragment):

    form_fields = form.FormFields(ILibraryFileSchema).omit('file')

    def getWorkspace(self):
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                return ob

    label_fields = set('''language country biogeographic_realm habitat
                       conservation directthreat organization monitoring
                       keywords description authors'''.split())

    def provideInitialDefaults(self):
        """ Provide initial defaults from values on current file for update"""
        # get the title default from this file
        defaults = {'title':self.context.Title()}
        context = self.context
        workspace = self.getWorkspace()
        if workspace:
            defaults['license'] = workspace.getLicense()
        file_schema = context.Schema()
        # calculate the defaults
        for field in self.form_fields:
            name = field.__name__
            value = None
            # try to get the value from this file
            if (name in self.label_fields):
                accessor = file_schema[name].getAccessor(context)
                value = accessor()
            # if we got anything maningful (not None AND not empty) set as
            # default for the field
            if value:
                defaults[name] = value
        return defaults

    def createAddAndReturnURL(self, data):
        library_file_obj = self.context.getLibraryreference()
        self.context.setAuthors(data['authors'])
        if data.get('gisdata'):
            gisdata = data.get('gisdata')
            del data['gisdata']
            library_file_obj.setGisdata(gisdata, mimetype='application/octet-stream')
            interface.directlyProvides(library_file_obj.getGisdata(), IGISDataFile)
        library_file_obj.update(**data)
        gsa_index(library_file_obj)
        return self.context.absolute_url() + "/@@view.html"

    def cancelURL(self):
        return self.context.absolute_url() + "/@@view.html"

class WorkspaceLibraryFileUpdateView(Fragment):
    """ View fragment for file add views
    """
    def asElement(self):
        return Element('view',
                       name="addtolibrary-file.html",
                       type="file",
                       title="Update Library : " + self.context.Title(),
                       section="workspaces")

class WorkspaceLibraryFileUpdatePage(Page):
    """ Page to tie together fragments for update workspace file to library """
    views = (WorkspaceLibraryFileUpdateView,
             WorkspaceLibraryFileUpdateForm, ) + COMMON_VIEWS

class ViewLibraryRecommendationsViewFragment(Fragment):
    def asElement(self):
        return Element('view',
                       name="view-recommendations.html",
                       type="libraryfile",
                       title="View Recommendations : " + self.context.Title(),
                       section="libraryfile")

class ViewLibraryRecommendationsFragment(Fragment):
    """ Fragment that displays all library recommendations in desc order by date """
    def asElement(self):
        root = None
        context = self.context
        rating = IUserRating(context)
        pmem = getToolByName(context, 'portal_membership')
        purl = getToolByName(context, 'portal_url')
        portal_url = purl.getPortalObject().absolute_url()
        ratingsList = [r for r in rating.all_user_ratings() if not r.badcontent]
        ratingsList.sort(key=lambda obj: obj.timestamp, reverse=True)
        if ratingsList:
            root = Element('reviews')
            for rating in ratingsList:
                userid = rating.userid
                member = pmem.getMemberById(userid)
                review = SubElement(root, 'review')
                SubElement(review, 'rating').text = str(int(rating))+'0'
                SubElement(review, 'title').text = rating.rating_title
                SubElement(review, 'comment').text = rating.rating_text
                SubElement(review, 'reviewer').text = member.getProperty('firstname')+' '+member.getProperty('lastname')
                SubElement(review, 'username').text = userid
                SubElement(review, 'modified').text = rating.timestamp.isoformat()
                SubElement(review, 'bio').attrib['href'] = portal_url +'/view-profile.html?userid='+userid
        return root

class ViewLibraryRecommendationsPage(Page):
    """ Page to pull together all the view """
    views = (ViewLibraryRecommendationsViewFragment,
             ViewLibraryRecommendationsFragment, ) + COMMON_VIEWS

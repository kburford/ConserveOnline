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

from string import join
from urllib import urlencode
from xml.parsers.expat import ExpatError
from zExceptions import Redirect
from Acquisition import aq_inner, aq_chain

from Products.COL3.etree import Element, SubElement, fromstring

from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite
#XXX Things that will probably go away
from zExceptions.unauthorized import Unauthorized
#XXX Things that will probably go away

from Products.CMFCore import utils as cmfutils
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.config import MIMETYPES, titleWithoutStopword
from Products.COL3.interfaces.workspace import IWorkspace
from Products.CMFCore.utils import getToolByName
from Products.COL3.config import DOCUMENT_TYPES, WS_DOCTOOL_INTERFACES
from Products.COL3.browser.common import BaseBatchFragment, BatchFragmentFactory
from Products.COL3.content.label import Labeller, sortable_title
from Products.COL3.browser.base import Fragment
from Products.COL3.browser.base import Page
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.browser.common import WITHFOLDER_VIEWS
from Products.COL3.browser.helper import _calculateSize
from Products.COL3.permissions import MANAGE_WORKSPACE_PERMISSION

########################################################################
##                  Start WorkspaceDocBrowser Code                    ##
########################################################################

class WorkspaceDocBrowserViewFragment(Fragment):
    def asElement(self):
        """The view part so we can see the pretty transform happen"""
        return Element('view',
                       name="all.html",
                       type="documents",
                       title="Browse All Files & Pages",
                       section="workspaces")

#XXX Need to refactor menu fragment generation, too much rework XXX#
class WorkspaceDocBrowserMenuFragment(Fragment):
    """ the menus items for the doc browser page"""
    """ Menu fragment for topic list view """

    _workspace = None

    _addmenu_items = ((u'Add Page', '@@add-page.html'),
                      (u'Add File', '@@add-file.html'),)
    _utilmenu_items = ()

    def __init__(self, context, request):
        super(WorkspaceDocBrowserMenuFragment, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def asElement(self):
        context = aq_inner(self.context)
        url = self._workspace.absolute_url()
        pmem = getToolByName(context, 'portal_membership')
        authmem = pmem.getAuthenticatedMember()
        self._utilmenu_items = self._generateUtilMenu(url)
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        addmenu_tag = Element('addmenu')
        url = context.absolute_url()
        keyword_sortable_title = sortable_title(self.request.get('keyword'))
        keyword_type = self.request.get('type')
        keyword_record = None
        querystr = ''
        for keyword, relative_url in self._addmenu_items:
            if (relative_url in ['@@edit.html','@@delete.html']) and keyword_sortable_title: #it's a keyword, special casing here for expediency, not elegance Leo
                if not pmem.isAnonymousUser():
                    if (authmem and
                        authmem.getUser().has_permission(MANAGE_WORKSPACE_PERMISSION,
                                                         self._workspace)):
                        if not keyword_record:
                            keyword_record = Labeller(context).getLabelRecordBySortableTitle(keyword_sortable_title)
                        relative_url = '%s/%s' % (keyword_record.id, relative_url)
                        querystr = relative_url
            elif keyword_sortable_title or keyword_type:
                if keyword_sortable_title:
                    if not keyword_record:
                        keyword_record = Labeller(context).getLabelRecordBySortableTitle(keyword_sortable_title)
                    if not keyword_record:
                        # Try again with full keyword value, which apparently already was a sortable_title
                        keyw = self.request.get('keyword')
                        if keyw != keyword_sortable_title and keyw.startswith(keyword_sortable_title):
                            keyword_record = Labeller(context).getLabelRecordBySortableTitle(keyw)
                    querystr = '%s?%s' % (relative_url, urlencode(dict(with_keyword=keyword_record.Title)))
                elif keyword_type:
                    querystr = '%s?%s' % (relative_url, urlencode(dict(with_type=keyword_type)))
            else:
                querystr = relative_url
            try:
                context.restrictedTraverse(relative_url)
            except (Unauthorized, AttributeError):
                pass
            else:
                SubElement(addmenu_tag, 'entry',
                           href=url + "/" + querystr).text = keyword
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
        return ((u'All', '%s/documents/%s' % (url, 'all.html')),
                (u'Keyword','%s/documents/%s' % (url, 'bykeyword.html')),
                (u'Purpose', '%s/documents/%s' % (url, 'bypurpose.html')),
                (u'Person', '%s/documents/%s' % (url, 'byauthor.html')),)

    def _isSelected(self, label, request):
        pages = {'documents':'Keyword',
                 'bykeyword.html':'Keyword',
                 'withkeyword-documents.html':'Keyword',
                 'byauthor.html':'Person',
                 'withauthor-documents.html':'Person',
                 'bypurpose.html':'Purpose',
                 'withtype-documents.html':'Purpose',
                 'all.html':'All',}
        url = request.get('URL').split('/')
        url.reverse()
        return pages.has_key(url[0]) and pages[url[0]] == label

class WorkspaceMatchingItemMenuFragment(WorkspaceDocBrowserMenuFragment):
    """This is for all the withXXXX views so the utility menu doesn't get added"""
    _utilmenu_items = ()

    def _generateUtilMenu(self, url):
        return self._utilmenu_items

class WorkspaceDocBrowserBatchProvider(BatchProvider):

    _workspace = None

    def __init__(self, context, request):
        super(WorkspaceDocBrowserBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    """ Batch provider to provide workspace document batch for front end"""
    def query(self, params):
        items = list()
        sortable_values = {'title':'sortable_title',
                           'date':'created',
                           'size':'getDocumentSize',
                           'mimetype':'getContentType'}
        pcat = self._workspace.portal_catalog
        path = join(self._workspace.getPhysicalPath(), '/')
        sort_on='sortable_title'
        sort_order=''
        filename_startswith = ''
        if params.get('sort_on'):
            sort_on = sortable_values.get(params.get('sort_on'), sort_on)
        if params.get('sort_order') == 'desc':
            sort_order = 'reverse'
        if params.get('startswith'):
            filename_startswith = params.get('startswith').lower()+'*'

        results = pcat.searchResults(path = {'query': path, 'level':0},
                                     object_provides=WS_DOCTOOL_INTERFACES,
                                     sort_on=sort_on,
                                     sort_order=sort_order)

        for item in results:
            if filename_startswith:
                try:
                    localTitle = titleWithoutStopword(item.Title)
                except AttributeError:
                    item = item[2](item[1][2])
                    localTitle = titleWithoutStopword(item.Title)
                if not localTitle.lower().startswith(filename_startswith[:1]):
                    continue
            mimetype = MIMETYPES.get(item.getContentType, 'No Mapping')
            is_private = item.getIs_private() and 'Yes' or 'No'
            if item.is_folderish:
                mimetype = 'folder'
                href = item.getURL()
            else:
                href = '%s/view.html' % item.getURL()
            items.append({'href':href,
                          'is_private':is_private,
                          'mimetype':mimetype,
                          'title':item.Title and item.Title or item.id,
                          'size':item.getDocumentSize,
                          'date':item.created.ISO8601()})
        return items

#class WorkspaceDocBrowserBatchFragment(BaseBatchFragment):
#    """ Image batch fragment which is fed by the workspace document batch provider"""
#    batch_provider = WorkspaceDocBrowserBatchProvider

class WorkspaceDocBrowserBatchFragment(Fragment):
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
                            'label': 'Date Authored'}),)
        batchfragment = BatchFragmentFactory(WorkspaceDocBrowserBatchProvider,
                                             columns = columns,
                                             letters_param='startswith')
        if request.get('sort_on', None) is None:
            request['sort_on'] = 'title'
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class WorkspaceDocBrowserPage(Page):
    """ Page that pulls together all the document browser fragments """
    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse All Files & Pages',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WorkspaceDocBrowserPage, self).__init__(context, request)

    views = (WorkspaceDocBrowserViewFragment,
             WorkspaceDocBrowserMenuFragment,
             WorkspaceDocBrowserBatchFragment, ) + COMMON_VIEWS

########################################################################
##                  End WorkspaceDocBrowser Code                      ##
########################################################################

########################################################################
##                  Start WorkspaceDocsByAuth Code                    ##
########################################################################

class WorkspaceDocsByAuthViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="byauthor.html",
                       title="Browse Files & Pages by Person",
                       type="documents",
                       section="workspaces"
                       )

class WorkspaceDocsByAuthBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    _workspace = None

    def __init__(self, context, request):
        super(WorkspaceDocsByAuthBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        items = []
        pcat = self._workspace.portal_catalog
        wsurl = self._workspace.absolute_url()
        path = join(self._workspace.getPhysicalPath(), '/')
        wm = IWorkspaceMemberManagement(self._workspace)
        workspacemembers = wm.listAllMembers()
        for member in workspacemembers:
            results = pcat.searchResults(path = {'query': path,'level':0},
                                         Creator=member.id,
                                         object_provides=WS_DOCTOOL_INTERFACES)
            if len(results) > 0:
                href = '%s/documents/%s%s' % (wsurl, 'withauthor-documents.html?userid=', member.id,)
                items.append({'href': href,
                              'firstname':member.getProperty('firstname'),
                              'lastname':member.getProperty('lastname'),
                              'count':len(results)})
        sort_on='lastname'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WorkspaceDocsByAuthBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on = 'lastname'
    columns = (('lastname', {'default_order':'asc',
                             'label': 'Last Name'}),
               ('firstname', {'default_order':'asc',
                              'label': 'First Name'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    batch_provider = WorkspaceDocsByAuthBatchProvider

class WorkspaceDocsByAuthPage(Page):
    """ The one class to rule them all and in the xslt bind them """

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Files & Pages By Person',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WorkspaceDocsByAuthPage, self).__init__(context, request)

    views = (WorkspaceDocsByAuthViewFragment,
             WorkspaceDocsByAuthBatchFragment,
             WorkspaceDocBrowserMenuFragment) + COMMON_VIEWS

########################################################################
##                  End WorkspaceDocsByAuth Code                    ##
########################################################################

########################################################################
##                  Start WorkspaceDocsByPurpose Code                    ##
########################################################################

class WorkspaceDocsByPurposeViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process
    """
    def asElement(self):
        return Element('view',
                       name="bypurpose.html",
                       title="Browse Files & Pages By Purpose",
                       type="documents",
                       section="workspaces"
                       )

class WorkspaceDocsByPurposeBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    _workspace = None

    def __init__(self, context, request):
        super(WorkspaceDocsByPurposeBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        items = []
        path = join(self._workspace.getPhysicalPath(), '/')
        pcat = cmfutils.getToolByName(self._workspace, 'portal_catalog')
        wsurl = self._workspace.absolute_url()
        for purpose in DOCUMENT_TYPES.keys():
            results = pcat.searchResults(path = {'query': path,'level':0},
                                         getDocument_type=purpose)
            href = '%s/documents/%s%s' % (wsurl, 'withtype-documents.html?purpose=', purpose)
            if len(results) > 0:
                items.append({'href': href,
                              'purpose':DOCUMENT_TYPES[purpose],
                              'count':len(results)})
        sort_on='purpose'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WorkspaceDocsByPurposeBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    sort_on= 'purpose'
    columns = (('purpose', {'default_order':'asc',
                         'label': 'Purpose'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    batch_provider = WorkspaceDocsByPurposeBatchProvider

class WorkspaceDocsByPurposePage(Page):
    """ The one class to rule them all and in the xslt bind them """

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Files & Pages By Purpose',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WorkspaceDocsByPurposePage, self).__init__(context, request)

    views = (WorkspaceDocsByPurposeViewFragment,
             WorkspaceDocsByPurposeBatchFragment,
             WorkspaceDocBrowserMenuFragment) + COMMON_VIEWS

########################################################################
##                  End WorkspaceDocsByPurpose Code                      ##
########################################################################

########################################################################
##                  Start WSDocsMatchingType Code                     ##
########################################################################

class WSDocsMatchingPurposeViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element("view",
                       name="withtype.html",
                       title="Files & Pages by Purpose - "+DOCUMENT_TYPES.get(self.request.get('purpose'),''),
                       type="documents",
                       section="workspaces",
                       )

class WSDocsMatchingPurposeBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    _workspace = None

    def __init__(self, context, request):
        super(WSDocsMatchingPurposeBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        items = []
        type = self.request.get('purpose', '')
        path = join(self._workspace.getPhysicalPath(), '/')
        pcat = cmfutils.getToolByName(self._workspace, 'portal_catalog')
        if type:
            results = pcat.searchResults(path = {'query': path,'level':0},
                                         getDocument_type=type)
            for result in results:
                mimetype = MIMETYPES.get(result.getContentType, 'No Mapping')
                is_private = result.getIs_private() and 'Yes' or 'No'
                if result.is_folderish:
                    mimetype = 'folder'
                    href = result.getURL()
                else:
                    href = '%s/view.html' % result.getURL()
                items.append({'href':href,
                              'is_private':is_private,
                              'title':result.Title,
                              'mimetype':mimetype,
                              'size':result.getDocumentSize,
                              'date':result.created.ISO8601()})
            sort_on='title'
            if params.get('sort_on'):
                sort_on = params.get('sort_on')
            if sort_on == 'size':
                items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
            else:
                items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
            #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
            if params.get('sort_order') == 'desc':
                items.reverse()
        return items


class WSDocsMatchingPurposeBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    columns = (('title', {'default_order':'asc',
                          'label': 'Title'}),
               ('mimetype', {'default_order':'asc',
                           'label': 'Format'}),
               ('size', {'default_order':'asc',
                         'label': 'Size'}),
               ('date', {'default_order':'asc',
                         'label': 'Date'}),)
    batch_provider = WSDocsMatchingPurposeBatchProvider
    sort_on = 'title'

class WSDocsMatchingPurposePage(Page):
    """ The one class to rule them all and in the xslt bind them """

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Files & Pages by Type - '+DOCUMENT_TYPES.get(request.get('type'),''),
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WSDocsMatchingPurposePage, self).__init__(context, request)

    views = (WSDocsMatchingPurposeViewFragment,
             WSDocsMatchingPurposeBatchFragment,
             WorkspaceMatchingItemMenuFragment) + COMMON_VIEWS

########################################################################
##                  End WSDocsMatchingType Code                       ##
########################################################################

########################################################################
##                  Start WSDocsByFolder Code                         ##
########################################################################

class WSDocsByFolderViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="byfolder.html",
                       title="Browse Files & Pages by Folder",
                       type="documents",
                       section="workspaces"
                       )

class WSDocsByFolderBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    _workspace = None

    def __init__(self, context, request):
        super(WSDocsByFolderBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        items = []
        provides = 'Products.COL3.interfaces.workspace.IWorkspaceImportedDocsFolder'
        path = join(self._workspace.getPhysicalPath(), '/')
        pcat = cmfutils.getToolByName(self._workspace, 'portal_catalog')
        results = pcat.searchResults(path = {'query': path,'level':0},
                                     object_provides=provides)
        if len(results) > 0:
            for result in results:
                count = 'N/A'
                if result.is_folderish:
                    children = pcat.searchResults(path = {'query': result.getPath(),'depth':1})
                    count = len(children)
                items.append({'href': '%s%s' % (result.getURL(),'/'),
                              'title':result.Title,
                              'count':count})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WSDocsByFolderBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    columns = (('title', {'default_order':'asc',
                          'label': 'Title'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)

    batch_provider = WSDocsByFolderBatchProvider
    sort_on = 'title'

class WSDocsByFolderPage(Page):
    """ The one class to rule them all and in the xslt bind them """

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Files & Pages By Folder',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WSDocsByFolderPage, self).__init__(context, request)

    views = (WSDocsByFolderViewFragment,
             WSDocsByFolderBatchFragment,
             WorkspaceDocBrowserMenuFragment) + COMMON_VIEWS

########################################################################
##                  End WorkspaceDocsByFolder Code                    ##
########################################################################

########################################################################
##                  Start WSImportedFolderPage Code                  ##
########################################################################

class WSImportedFolderViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        return Element('view',
                       name="withfolder-documents.html",
                       title="Files & Pages by Folder - "+self.context.Title(),
                       type="documents",
                       section="workspaces"
                       )

class WSImportedFolderBatchProvider(BatchProvider):
    """ Provides a batch of folders in a workspace """
    def query(self, params):
        items = []
        context = self.context
        path = join(context.getPhysicalPath(), '/')
        pcat = cmfutils.getToolByName(context, 'portal_catalog')
        results = pcat.searchResults(path = {'query': path,'depth':1})
        if len(results) > 0:
            for result in results:
                mimetype = MIMETYPES.get(result.getContentType, 'No Mapping')
                is_private = result.getIs_private() and 'Yes' or 'No'
                if result.is_folderish:
                    mimetype = 'folder'
                    href = result.getURL()
                else:
                    href = '%s/view.html' % result.getURL()
                items.append({'href':href,
                              'is_private':is_private,
                              'title':result.Title,
                              'mimetype':mimetype,
                              'size':result.getDocumentSize and result.getDocumentSize or 0,
                              'date':result.created.ISO8601()})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'size':
                items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WSImportedFolderBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    batch_provider = WSImportedFolderBatchProvider

class WSImpFolderBreadcrumbsFragment(Fragment):
    """ Fragment to return the bredcrumbs for a given context"""

    def getContext(self):
        """ override this to parameterize the breadcrumb context """
        return aq_inner(self.context)

    def asElement(self, xtra_breadcrumb_ids=None):
        """Added the xtra_breadcrumb_ids to this asElement method so that
           we don't have to wire up traversable views and go through zcml
           hoops to get view titles added to the breadcrumbs, the ids should
           be passed in as a sequence of dictionaries like so (if href is blank,
           no href attribute will be added to the element):
           ({'title':'breadcrumb_one_title', 'href':'http://url'},
            {'title':'breadcrumb_two_title', ''})"""
        context = self.getContext()
        request = self.request
        portal = getSite()
        # no portal, no game
        if portal is None:
            return None
        root = Element('breadcrumbs')
        elem = SubElement(root,'entry')
        elem.text = 'Home'
        elem.attrib['href'] = portal.absolute_url()
        view = getMultiAdapter((context, request), name='breadcrumbs_view')
        context_url = getattr(context, 'absolute_url', lambda: None)()
        for i in range(len(view.breadcrumbs())-1):
            elem = SubElement(root, 'entry')
            elem.text = view.breadcrumbs()[i].get('Title','')
            entry_url = view.breadcrumbs()[i].get('absolute_url', None)
            if context_url != entry_url:
                elem.attrib['href'] = entry_url+'/'
            elif context_url == entry_url and xtra_breadcrumb_ids:
                elem.attrib['href'] = entry_url+'/'
        if xtra_breadcrumb_ids:
            for crumb in xtra_breadcrumb_ids:
                elem = SubElement(root, 'entry')
                elem.text = crumb['title']
                href = crumb.get('href', None)
                if href != '' and href is not None:
                    elem.attrib['href'] = crumb.get('href', '')
        return root

class WSImportedFolderPage(Page):
    """ The one class to rule them all and in the xslt bind them """

    views = (WSImportedFolderViewFragment,
             WSImportedFolderBatchFragment,
             WorkspaceMatchingItemMenuFragment) + WITHFOLDER_VIEWS + (WSImpFolderBreadcrumbsFragment, )
             
    def getResponse(self):
        """ Overriding to set some variables"""
        context = self.context
        self.xtra_breadcrumb_ids = ({'title':'Files & Pages by Folder - '+context.Title(),
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        if context.isPrincipiaFolderish:
            if 'index_html' in [r.id for r in context.listFolderContents()]:
                raise Redirect(context.absolute_url()+'/index_html')
        return super(WSImportedFolderPage, self).getResponse()

########################################################################
##                  End WSImportedFolderPage Code                     ##
########################################################################

########################################################################
##                     Start WSDocsByKeyword Code                       ##
########################################################################

class WSDocsByKeywordViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process
    NOTE - this used to be called WSDocsByLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def asElement(self):
        return Element('view',
                       name="bykeyword.html",
                       title="Browse Files & Pages by Keyword",
                       type="documents",
                       section="workspaces"
                       )

class WSDocsByKeywordBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system
    NOTE - this used to be called WSDocsByLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """

    _workspace = None

    def __init__(self, context, request):
        super(WSDocsByKeywordBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        context = aq_inner(self.context)
        items = []
        labeller = Labeller(self._workspace)
        keywords = labeller.listLabelObjects()
        for keyword in keywords:
            count = len(keyword['label'].getTraversableBRefs(context))
            if count > 0:
                querystr = 'withkeyword-documents.html?keyword='
                wsurl = self._workspace.absolute_url()
                items.append({'href': '%s/documents/%s%s' % (wsurl, querystr, keyword['sortable_title']),
                              'keyword':keyword['label'].Title(),
                              'count':count,})
        sort_on='keyword'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp((a.get(sort_on)), (b.get(sort_on))))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WSDocsByKeywordBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above
    NOTE - this used to be called WSDocsByLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    sort_on = 'keyword'
    columns = (('keyword', {'default_order':'asc',
                             'label': 'Keyword'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    batch_provider = WSDocsByKeywordBatchProvider

class WSDocsByKeywordPage(Page):
    """ The one class to rule them all and in the xslt bind them
    NOTE - this used to be called WSDocsByLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Browse Files & Pages By Keyword',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WSDocsByKeywordPage, self).__init__(context, request)

    views = (WSDocsByKeywordViewFragment,
             WSDocsByKeywordBatchFragment,
             WorkspaceDocBrowserMenuFragment) + COMMON_VIEWS

########################################################################
##                      End WSDocsByKeyword Code                        ##
########################################################################

########################################################################
##               Start WSDocsMatchingKeyword Code                       ##
########################################################################

class WSDocsMatchingKeywordViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process
    NOTE - this used to be called WSDocsMatchingLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def asElement(self):
        keyword_instance = Labeller(self.context).getLabelInstance(self.request.get('keyword'))
        try:
            title = keyword_instance.Title() and keyword_instance.Title() or 'No Title'
        except:
            title = "Keyword Not Found"
        return Element('view',
                       name="withkeyword.html",
                       title="Files & Pages by Keyword - "+title,
                       type="documents",
                       section="workspaces"
                       )

class WSDocsMatchingKeywordBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system
    NOTE - this used to be called WSDocsMatchingLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """

    _workspace = None

    def __init__(self, context, request):
        super(WSDocsMatchingKeywordBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        context = aq_inner(self.context)
        items = []
        keyword = self.request.get('keyword', '')
        #At the beginning of the project, what are now referred to as keywords were called labels
        #because the term "labels" was found to be confusing to end users.  The underlying machinery
        #retains the name Label however
        labeller = Labeller(self._workspace)
        keyword = labeller.getLabelRecordBySortableTitle(keyword)
        keywordRefs = (aq_inner(keyword.getObject())).getTraversableBRefs(context)
        for reference in keywordRefs:
            mimetype = MIMETYPES.get(reference.getContentType(), 'No Mapping')
            is_private = reference.getIs_private() and 'Yes' or 'No'
            if reference.isPrincipiaFolderish:
                mimetype = 'folder'
                href = reference.absolute_url()
            else:
                href = '%s/view.html' % reference.absolute_url()
            items.append({'href':href,
                          'is_private':is_private,
                          'title':reference.Title(),
                          'mimetype':mimetype,
                          'size':_calculateSize(reference.getObjSize()),
                          'date':reference.created().ISO8601()})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WSDocsMatchingKeywordBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above
    NOTE - this used to be called WSDocsMatchingLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    batch_provider = WSDocsMatchingKeywordBatchProvider

class WSDocsMatchingKeywordMenuFragment(WorkspaceMatchingItemMenuFragment):
    _addmenu_items = ((u'Add Page', '@@add-page.html'),
                      (u'Add File', '@@add-file.html'),
                      (u'Edit Keyword', '@@edit.html'),
                      (u'Delete Keyword', '@@delete.html'),)


class WSDocsMatchingKeywordPage(Page):
    """ The one class to rule them all and in the xslt bind them
    NOTE - this used to be called WSDocsMatchingLabelXXX.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """

    def getResponse(self):
        """ Overriding to set some variables"""
        context = self.context
        request = self.request
        keyword_instance = Labeller(context).getLabelInstance(request.get('keyword'))
        try:
            title = keyword_instance.Title() and keyword_instance.Title() or 'No Title'
        except:
            title = "No Title"
        self.xtra_breadcrumb_ids = ({'title':'Files & Pages by Keyword - ' +title,
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(WSDocsMatchingKeywordPage, self).getResponse()

    class GetCurrentKeywordInfoFragment(Fragment):
        """ NOTE - this used to be called GetCurrentLabelInfoFragment.  At the beginning of the project
        what are now called "keywords" were referred to as "labels".  End users didn't like
        "labels" so the decision was made to change to "labels" to "keywords".  Any reference
        to labels is due to not wanting to change the underlying machinery that handles labelling
        """
        def asElement(self):
            keyword = self.request['keyword']
            keyword_instance = Labeller(self.context).getLabelInstance(keyword)
            elem = Element('currentlabel')
            text = keyword_instance.getRawText()
            try:
                textelem = fromstring(text)
            except ExpatError:
                textelem = Element('{http://www.w3.org/1999/xhtml}div')
                textelem.text = text
            SubElement(elem, 'text').append(textelem)
            text = keyword_instance.getRawFooter()
            try:
                textelem = fromstring(text)
            except ExpatError:
                textelem = Element('{http://www.w3.org/1999/xhtml}div')
                textelem.text = text
            SubElement(elem, 'footer').append(textelem)
            return elem

    views = (WSDocsMatchingKeywordViewFragment,
             WSDocsMatchingKeywordBatchFragment,
             WSDocsMatchingKeywordMenuFragment,
             GetCurrentKeywordInfoFragment) + COMMON_VIEWS

########################################################################
##                     End WSDocsMatching Code                        ##
########################################################################

########################################################################
##                  Start WSDocsMatchingAuth Code                     ##
########################################################################

class WSDocsMatchingAuthViewFragment(Fragment):
    """ View portion for the front end to match on in the transformation process """
    def asElement(self):
        userid = self.request.get('userid')
        member = self.context.portal_membership.getMemberById(userid)
        title = '%s %s' % (member.getProperty('firstname', '',),
                           member.getProperty('lastname', '',) )
        return Element('view',
                       name="withauthor.html",
                       title='Files & Pages by Author - '+title,
                       type="documents",
                       section="workspaces"
                       )

class WSDocsMatchingAuthBatchProvider(BatchProvider):
    """ Provides a batch of workspaces in the system """

    _workspace = None

    def __init__(self, context, request):
        super(WSDocsMatchingAuthBatchProvider, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def query(self, params):
        items = []
        request = self.request
        path = join(self._workspace.getPhysicalPath(), '/')
        pmem = cmfutils.getToolByName(self._workspace, 'portal_membership')
        pcat = cmfutils.getToolByName(self._workspace, 'portal_catalog')
        memberid = request.get('userid', '')
        member = pmem.getMemberById(memberid)
        documents = pcat.searchResults(path = {'query': path,'level':0},
                                       Creator=member.id,
                                       object_provides=WS_DOCTOOL_INTERFACES)
        for document in documents:
            mimetype = MIMETYPES.get(document.getContentType, 'No Mapping')
            is_private = document.getIs_private() and 'Yes' or 'No'
            if document.is_folderish:
                mimetype = 'folder'
                href = document.getURL()
            else:
                href = '%s/view.html' % document.getURL()
            items.append({'href':href,
                          'is_private':is_private,
                          'title':document.Title,
                          'mimetype':mimetype,
                          'size':document.getDocumentSize,
                          'date':document.created.ISO8601()})
        sort_on='title'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'size':
                items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        else:
            items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        #items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items


class WSDocsMatchingAuthBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch provider above """
    columns = (('title', {'default_order':'asc',
                          'label': 'Title'}),
               ('mimetype', {'default_order':'asc',
                           'label': 'Format'}),
               ('size', {'default_order':'asc',
                         'label': 'Size'}),
               ('date', {'default_order':'asc',
                         'label': 'Date'}),)

    batch_provider = WSDocsMatchingAuthBatchProvider
    sort_on = 'title'

class WSDocsMatchingAuthPage(Page):
    """ The one class to rule them all and in the xslt bind them """

    def __init__(self, context, request):
        pmem = cmfutils.getToolByName(context, 'portal_membership')
        memberid = request.get('userid', '')
        member = pmem.getMemberById(memberid)
        fname = member.getProperty('firstname')
        lname = member.getProperty('lastname')
        self.xtra_breadcrumb_ids = ({'title':'Files & Pages by Author - '+fname+' '+lname,
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(WSDocsMatchingAuthPage, self).__init__(context, request)

    views = (WSDocsMatchingAuthViewFragment,
             WSDocsMatchingAuthBatchFragment,
             WorkspaceMatchingItemMenuFragment) + COMMON_VIEWS

########################################################################
##                  End WSDocsMatchingAuth Code                       ##
########################################################################

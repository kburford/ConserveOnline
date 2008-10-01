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
from Products.COL3.etree import Element, SubElement

from zope.formlib import form
from Acquisition import aq_parent, aq_inner
from zExceptions.unauthorized import Unauthorized
from ZODB.POSException import ConflictError

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note

from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.common import COMMON_VIEWS, KeywordsFragment
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.batch import BatchFragmentFactory

from Products.COL3.formlib.xmlform import AddFormFragment, EditFormFragment
from Products.COL3.interfaces.page import IPageSchema
from Products.COL3.content.page import COLPage

from Products.COL3.content.indexer import index as gsa_index
from Products.COL3.content.indexer import reindex as gsa_reindex
from Products.COL3.content.indexer import unindex as gsa_unindex

from Products.COL3.browser.batch import BatchFragment
from Products.COL3.browser.base import AjaxPage
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.content.base import idFromTitle
from Products.COL3 import config
from Products.COL3.browser.common import CurrentKeywordsFragment, getWorkspace
from Products.COL3.content.file import COLFile

# Page add and edit forms

class PageAddForm(AddFormFragment):

    form_fields = form.FormFields(IPageSchema)

    def provideInitialDefaults(self):
        """ Provide initial suggestion for Keywords(a.k.a. Labels) based on the keyword(or label) that
        was being browsed"""
        defaults = {}
        with_label = self.request.get('with_label', None)
        with_type = self.request.get('with_type', None)
        if with_label is not None:
            with_label = unicode(with_label, config.CHARSET)
            defaults.update(labels=[with_label,])
        if with_type is not None:
            with_type = unicode(with_type, config.CHARSET)
            defaults.update(with_type=[with_type,])
        return defaults

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)

        unique_id=idFromTitle(title=data['title'], container=context)

        # code taken from plone_scripts/createObject:
        new_id = context.invokeFactory(id=unique_id,
                                       type_name=COLPage.portal_type)
        if not new_id:
           new_id = unique_id
        obj = context[new_id]
        transaction_note('Created %s with id %s in %s' % (obj.getTypeInfo().getId(),
                                                          new_id,
                                                          context.absolute_url()))
        obj.update(**data)

        # Do not index if 'is private'
        if not obj.getIs_private():
            gsa_index(obj)

        return obj.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class PageAddView(Fragment):
    """ View fragment for page add views
    """

    def asElement(self):
        #<view name="add.html" type="page" title="Add Page" section="workspaces"/>
        return Element('view',
                       name="add.html",
                       type="page",
                       title="Add Page",
                       section="workspaces")

class PageAddPage(Page):

    views = (PageAddView, PageAddForm, KeywordsFragment) + COMMON_VIEWS

class PageEditForm(EditFormFragment):

    form_fields = form.FormFields(IPageSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        # the topic body is actually the text of the first comment
        return dict(title=context.Title(),
                    text=context.getRawText(),
                    labels=context.getLabels(),
                    document_type=context.getDocument_type(),
                    is_private=context.getIs_private())

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        context.update(**data)
        if not context.getIs_private():
            gsa_reindex(context)
        return context.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class PageEditView(Fragment):
    """ View class for editing pages
    """

    def asElement(self):
        #<view name="edit.html"
        #      type="page"
        #      title="Edit Page: The Current Page Title" section="workspaces"/>
        return Element('view',
                       name="edit.html",
                       type="page",
                       title="Edit Page: " + self.context.Title(),
                       section="workspaces")

class PageEditPage(Page):

    views = (PageEditView, PageEditForm, KeywordsFragment, ) + COMMON_VIEWS

class PageViewView(Fragment):
    """ View class for viewing pages
    """

    def asElement(self):
        #<view name="view.html" type="page" title="Condors United"
        #      section="workspaces"/>
        return Element('view',
                       name="view.html",
                       type="page",
                       title=self.context.Title(),
                       section="workspaces")

class PageViewActionMenu(Fragment):
    # there should be a way to automatically eliminate this view if the user
    # doesn't have permissions

    _actionmenu_entries = (# title, relative-url
                           (u'Edit', "@@edit.html"),
                           (u'Delete', "@@delete.html"),
                           )

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('actionmenu')
        for label, relative_url in self._actionmenu_entries:
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

class PageViewPage(Page):

    views = (PageViewView, PageViewActionMenu, CurrentKeywordsFragment,) + COMMON_VIEWS

class AboutPageViewView(Fragment):
    """<view name="view.html" type="about" title="ConserveOnline About Folder" section="about"/>"""
    def asElement(self):
        return Element('view',
                       name='view.html',
                       type='page',
                       title=self.context.Title(),
                       section=self.context.getPhysicalPath()[-1])

class AboutPageViewPage(Page):
    views = (AboutPageViewView, ) + COMMON_VIEWS

#class AboutPageViewPage(Page):
#    views = (PageViewView, ) + COMMON_VIEWS

class PageDeleteViewFragment(Fragment):
    def asElement(self):
        context = aq_inner(self.context)
        if self.request.get('confirm', None) is not None:
            # user has confirmed deletion
            # so delete the event
            docfolder = aq_parent(context)
            docfolder.manage_delObjects([context.id])
            gsa_unindex(context)
            # XXX status message
            raise SafeRedirect(docfolder.absolute_url())
        # user hasen't confirmed yet, show confirmation view
        #<view name="delete.html" type="page" title="Delete Page" section="workspaces"/>
        return Element('view',
                       name="delete.html",
                       type="page",
                       title="Delete: " + context.Title(),
                       section="workspaces")

class PageDeleteViewPage(Page):
    views = (PageDeleteViewFragment, ) + COMMON_VIEWS

class ImageUploadForm(BrowserView):
    """This simply provides a form for one of front end ajaxy views"""
    def __call__(self):

        request = self.request

        formStringStart = "<html><body><form ENCTYPE=\"multipart/form-data\" METHOD=\"post\" ACTION=\'\'>" + \
        "<p style=\'font-size:11pt\'>%s  When you\'re ready, click the \"upload\" button to send the file." + \
        "</p><input id=\'uploadName\' name=\'fileName\' type=\'file\'/><br/><input type=\'hidden\' " + \
        "name=\'submitted\' value=\'submitted\'/><input type=\'submit\' onmouseup=\'this.style.visibility=\"hidden\"; this.value=\"uploading\"\' name=\'submit\' value=\'upload\'/></form> "

        formStringEnd = "</body></html>"
        errorString = "<strong>*Error* (%s) ... please resubmit.</strong><br/>"
        messageString = "Enter the path and filename of the file you would like " + \
                        "to upload or click browse to search for the file."
        scriptString = '<script>parent.useFile(\'%s\',\'%s\');</script>'
        if request.form.get('submitted', None) is not None:
            try:
                workspace = getWorkspace(self.context)
                documents = workspace['documents']
                imageFile = request.get('fileName')
                fname = imageFile.filename.split("\\")
                fname = fname[len(fname)-1]
                imageFile.seek(0)
                imageId = (documents.invokeFactory(COLFile.portal_type,
                                                   fname) or
                           fname)
                image = documents[imageId]
                image.update(file=imageFile,
                             labels=['image'],
                             title=fname,
                             biogeographic_realm=workspace.getBiogeographic_realm(),
                             language=workspace.getLanguage(),
                             country=workspace.getCountry(),
                             license=workspace.getLicense())
                desc = image.Description() or fname
                formStringStart = '%s%s' % ((formStringStart % messageString),
                                            (scriptString % (image._getURL(), desc)))
            except ConflictError:
                raise
            except Exception, e:
                error = '%s%s%s' % (e.__class__.__name__, ":", str(e))
                errorString = errorString % error
                formStringStart = formStringStart % '%s%s' % (errorString, messageString)
        else:
            formStringStart = formStringStart % messageString

        return '%s%s' % (formStringStart, formStringEnd)

class ImageBatchProvider(BatchProvider):
    """ Batch provider to provide image batch for front end"""
    def query(self, params):
        workspace = getWorkspace(self.context)
        pcat = getToolByName(workspace, 'portal_catalog')
        path = join(workspace.getPhysicalPath(), '/')
        results = pcat.searchResults(path = {'query': path},
                                     portal_type=COLFile.portal_type,
                                     getContentType=config.THUMBNAIL_TYPES,
                                     sort_on='created',
                                     sort_order='reverse')
        items = [dict(imgthumb='%s/%s' % (item.getURL(), 'image_thumb'),
                      imglink=item.getURL(),
                      description=item.Description)
                 for item in results
                 # add the query results if they have proper thumbnails
                 if workspace.restrictedTraverse(item.getPath() +
                                                 '/image_thumb',
                                                 None) is not None]
        return items

class ImageBrowserBatchFragment(BatchFragment):
    """ Image batch fragment which is fed by the image batch provider"""
    def asElement(self):
        context = self.context
        request = self.request
        batchfragment = BatchFragmentFactory(ImageBatchProvider,
                                             letters_param='REMOVE',
                                             columns={}, )
        batch = batchfragment(context, request)
        return batch.asElement()

class ImageBrowserPage(AjaxPage):
    """ This is an *AjaxPage*, only returns a fragment, but keeps pattern alive"""
    views = (ImageBrowserBatchFragment, )

class LinkBrowserFragment(Fragment):
    """ This provides a chunk of xml for the front end to display links in a workspace"""
    def asElement(self):
        context = self.context
        pcat = context.portal_catalog
        workspace = aq_parent(aq_inner(context))
        root = Element('results')
        elem = SubElement(root, 'links')
        path = join(workspace['calendar'].getPhysicalPath(), '/')
        results = pcat.searchResults(path = {'query': path,'depth':1},
                                     sort_on='id')
        for item in results:
            desc = item.Description and item.Description or item.Title
            linkelem = SubElement(elem, 'linkRec')
            SubElement(linkelem, 'httpLink').text = item.getURL()
            SubElement(linkelem, 'descr').text = desc

        path = join(workspace['documents'].getPhysicalPath(), '/')
        results = pcat.searchResults(path = {'query': path,'depth':1},
                                     sort_on='id')
        for item in results:
            desc = item.Description and item.Description or item.Title
            linkelem = SubElement(elem, 'linkRec')
            SubElement(linkelem, 'httpLink').text = item.getURL()
            SubElement(linkelem, 'descr').text = desc
        return root

class LinkBrowserPage(AjaxPage):
    """ This is an *AjaxPage*, only returns a fragment, but keeps the page pattern alive"""
    views = (LinkBrowserFragment, )

class ScientificJournalsViewFragment(Fragment):
    """ View Fragment for Sceintific Journals Page"""
    def asElement(self):
        return Element('view',
                       name="scientificjournals.html",
                       type="site",
                       title="Available Scientific Journals",
                       section="site")

class ScientificJournalsPage(Page):
    """ A Simple Page for the front end """
    views = (ScientificJournalsViewFragment, ) + COMMON_VIEWS

class FAQsViewFragment(Fragment):
    """ View Fragment for FAQs Page"""
    def asElement(self):
        return Element('view',
                       name="help.html",
                       type="site",
                       title="Help and Frequently Asked Questions",
                       section="site")

class FAQsPage(Page):
    """ A Simple Page for the front end """
    views = (FAQsViewFragment, ) + COMMON_VIEWS

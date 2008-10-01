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
from Products.COL3.etree import Element, SubElement

from zope.formlib import form
from Acquisition import aq_parent, aq_inner, aq_chain
from zExceptions.unauthorized import Unauthorized

from Products.Five import BrowserView
from Products.Archetypes.utils import contentDispositionHeader
from Products.CMFPlone.utils import transaction_note

from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.common import COMMON_VIEWS, KeywordsFragment

from Products.COL3.formlib.xmlform import AddFormFragment, EditFormFragment
from Products.COL3.interfaces.file import IFileSchema, IFileEditSchema
from Products.COL3.interfaces.file import IGISDataFile

from Products.COL3.content.indexer import index as gsa_index
from Products.COL3.content.indexer import reindex as gsa_reindex
from Products.COL3.content.indexer import unindex as gsa_unindex

from Products.COL3.browser.base import SafeRedirect
from Products.COL3.content.base import idFromTitle
from Products.COL3 import config
from Products.COL3.browser.common import CurrentKeywordsFragment, getWorkspace
from Products.COL3.content.label import Labeller
from Products.COL3.interfaces.workspace import IWorkspace

try:
    from plone.i18n.normalizer.interfaces import IUserPreferredFileNameNormalizer
    FILE_NORMALIZER = True
except ImportError:
    FILE_NORMALIZER = False

# File add and edit forms
class FileAddForm(AddFormFragment):

    form_fields = form.FormFields(IFileSchema)

    def provideInitialDefaults(self):
        """ Provide initial suggestion for Keywords(a.k.a. Labels) based on the keyword that
        was being browsed"""
        defaults = {}
        workspace = getWorkspace(self.context)
        with_label = self.request.get('with_label', None)
        with_type = self.request.get('with_type', None)
        if with_label is not None:
            try:
                with_label = unicode(with_label, config.CHARSET)
            except TypeError, e:
                logger = logging.getLogger('Products.COL3.browser')
                logger.error('('+e.__class__.__name__+'[file.py(61) - provideInitialDefaults] : '+str(e)+')')
            defaults.update(labels=(with_label,))
        elif with_type is not None:
            try:
                with_type = unicode(with_type, config.CHARSET)
            except TypeError, e:
                logger = logging.getLogger('Products.COL3.browser')
                logger.error('('+e.__class__.__name__+'[file.py(68) - provideInitialDefaults] : '+str(e)+')')
            defaults.update(document_type=(with_type,))
        if workspace:
            defaults['license'] = workspace.getLicense()
        return defaults

    def createAddAndReturnURL(self, data):

        label_fields = set('''language country biogeographic_realm habitat
                              conservation directthreat organization monitoring
                              keywords'''.split())
        context = aq_inner(self.context)
        labeller = Labeller(context)
        unique_id=idFromTitle(title=data['title'], container=context)

        # code taken from plone_scripts/createObject:
        new_id = context.invokeFactory(id=unique_id, type_name='COLFile')
        if not new_id:
            new_id = unique_id
        obj = context[new_id]
        transaction_note('Created %s with id %s in %s' %
                         (obj.getTypeInfo().getId(), new_id,
                          context.absolute_url()))
        # end code take from plone_scripts/createObject
        labels = data.get('labels')
        workspace = getWorkspace(context)
        if labels:
            primarylabel = labels[0]
            workspace = getWorkspace(self.context)
            try:
                label = labeller.getLabelRecordBySortableTitle(primarylabel)
            except UnicodeDecodeError:
                # this is a hack.  Certain assigned labels, e.g., 'private', caused this exception.
                label = labeller.getLabelRecordBySortableTitle(primarylabel.encode('ascii'))
            if label:
                label = label.getObject()
                label_schema = label.Schema()
                for name in label_fields:
                    try:
                        accessor = label_schema[name].getAccessor(label)
                        value = accessor()
                        if value:
                            data[name] = value
                        else:
                            accessor = workspace.Schema()[name].getAccessor(workspace)
                            value = accessor()
                            if value:
                                data[name] = value
                    except KeyError, AttributeError:
                        pass
        if data.get('gisdata'):
            gisdata = data.get('gisdata')
            del data['gisdata']
            obj.setGisdata(gisdata, mimetype='application/octet-stream')
            interface.directlyProvides(obj.getGisdata(), IGISDataFile)
        obj.update(**data)
        # Do not index if 'is private'
        if not obj.getIs_private():
            gsa_index(obj)

        return obj.absolute_url() + "/@@view.html"

    def cancelURL(self):
        return self.context.absolute_url()

class FileAddView(Fragment):
    """ View fragment for file add views
    """

    def asElement(self):
        #<view name="add.html" type="file" title="Add a File"
        #      section="workspaces"/>
        return Element('view',
                       name="add.html",
                       type="file",
                       title="Add a File",
                       section="workspaces")

class FileAddPage(Page):
    """Page to tie together all the fragments for the file add view"""

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':'Add a File',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(FileAddPage, self).__init__(context, request)

    views = (FileAddView, FileAddForm, KeywordsFragment) + COMMON_VIEWS

class FileEditForm(EditFormFragment):

    form_fields = form.FormFields(IFileEditSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        # the topic body is actually the text of the first comment
        return dict(title=context.Title(),
                    file=None,
                    labels=context.getLabels(),
                    description=context.Description(),
                    document_type=context.getDocument_type(),
                    is_private=context.getIs_private(),
                    license=context.getLicense(),
                    gisdata=None)

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        if data['file'] is None:
            # if no file upload, don't change anything
            del data['file']
        if data['gisdata'] is None:
            del data['gisdata']
        else:
            gisdata = data.get('gisdata')
            del data['gisdata']
            obj.setGisdata(gisdata, mimetype='application/octet-stream')
            interface.directlyProvides(obj.getGisdata(), IGISDataFile)
        context.update(**data)
        if not context.getIs_private():
            gsa_reindex(context)
        return context.absolute_url() + "/view.html"

    def cancelURL(self):
        return self.context.absolute_url() + "/view.html"

class FileEditView(Fragment):
    """ View class for editing files
    """

    def asElement(self):
        #<view name="edit.html"
        #      type="file"
        #      title="Edit: California Condors brochure"
        #      section="workspaces"/>
        return Element('view',
                       name="edit.html",
                       type="file",
                       title="Edit File: " + self.context.Title(),
                       section="workspaces")

class FileEditPage(Page):

    views = (FileEditView, FileEditForm,
             KeywordsFragment, CurrentKeywordsFragment,) + COMMON_VIEWS

class FileViewView(Fragment):
    """ View class for viewing files
    """

    def asElement(self):
        #<view name="view.html" type="file" title="Condors United"
        #      section="workspaces"/>
        return Element('view',
                       name="view.html",
                       type="file",
                       title=self.context.Title(),
                       section="workspaces")

class FileViewMenu(Fragment):
    # there should be a way to automatically eliminate this view if the user
    # doesn't have permissions

    _actionmenu_entries = (# title, relative-url
                           (u'Edit', "@@edit.html"),
                           (u'Add to Library', '@@add.html'),
                           (u'Update Library File', '@@update.html'),
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
                # ugly special case:
                if (relative_url == "@@add.html" and
                    context.getLibraryreference()):
                    # file has already been sent to the library, skip it.
                    continue
                elif (relative_url == "@@update.html" and
                      not context.getLibraryreference()):
                    # file is not yet in the library, skip it.
                    continue
                SubElement(actionmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label

        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        if menu_tag:
            # do not return empty elements
            return menu_tag

class FileViewPage(Page):

    views = (FileViewView, FileViewMenu,
             CurrentKeywordsFragment,) + COMMON_VIEWS

class FileDeleteViewFragment(Fragment):
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
        #<view name="delete.html" type="file" title="Delete File"
        #      section="workspaces"/>
        return Element('view',
                       name="delete.html",
                       type="file",
                       title="Delete File",
                       section="workspaces")

class FileDeleteViewPage(Page):
    views = (FileDeleteViewFragment, ) + COMMON_VIEWS

class GISFileDataView(BrowserView):
    """ Default view for gis data files...
        *Download the file (use default index_html)*, code copied from
        download method in FileField (Archetypes/Field.py), I had to make a
        couple of minor changes to get the proper values from the current
        context
    """
    def __call__(self, REQUEST=None, RESPONSE=None,):
        file = self.context
        if not REQUEST:
            REQUEST = aq_get(instance, 'REQUEST')
        if not RESPONSE:
            RESPONSE = REQUEST.RESPONSE
        filename = self.context.filename
        if filename is not None:
            if FILE_NORMALIZER:
                filename = IUserPreferredFileNameNormalizer(REQUEST).normalize(
                    unicode(filename, 'UTF8'))
            else:
                filename = unicode(filename, 'UTF8')
            header_value = contentDispositionHeader(
                disposition='attachment',
                filename=filename)
            RESPONSE.setHeader("Content-disposition", header_value)
            RESPONSE.setHeader("base", self.context.absolute_url()+'/')
        return file.index_html(REQUEST, RESPONSE)


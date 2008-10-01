from zope.formlib import form
from Acquisition import aq_inner, aq_parent
from urllib import urlencode


from Products.COL3.etree import Element

from Products.COL3.formlib.xmlform import EditFormFragment
from Products.COL3.interfaces.label import ILabelEditSchema
from Products.COL3.content.label import sortable_title
from Products.COL3.browser.base import Fragment
from Products.COL3.browser.base import Page
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.common import COMMON_VIEWS

class KeywordEditForm(EditFormFragment):
    form_fields = form.FormFields(ILabelEditSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        schema = context.Schema()
        return dict((field.__name__, schema[field.__name__].getEditAccessor(context)())
                    for field in self.form_fields
                    if 'r' in schema[field.__name__].mode)

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        context.update(**data)
        return (context.aq_parent.absolute_url() +
                "/withkeyword-documents.html?" +
                urlencode(dict(keyword=sortable_title(context.Title()))))

    def cancelURL(self):
        context = aq_inner(self.context)
        return (context.aq_parent.absolute_url() +
                "/withkeyword-documents.html?" +
                urlencode(dict(keyword=sortable_title(context.Title()))))

class KeywordEditView(Fragment):
    """ View class for editing keywords
    """

    def asElement(self):
        return Element('view',
                       name="edit.html",
                       type="page",
                       title="Edit Keyword: " + self.context.Title(),
                       section="workspaces")

class KeywordEditPage(Page):

    views = (KeywordEditView, KeywordEditForm, ) + COMMON_VIEWS


class KeywordDeleteFragment(Fragment):
    def asElement(self):
        context = aq_inner(self.context)
        if self.request.get('confirm', None) is not None:
            # user has confirmed deletion
            # so delete the keyword 
            docfolder = aq_parent(context)
            docfolder.manage_delObjects([context.id])
            #gsa_unindex(context)
            # XXX status message
            raise SafeRedirect(context.aq_parent.absolute_url() + 
                               "/bykeyword.html")

        # user hasen't confirmed yet, show confirmation view
        #<view name="delete.html" type="file" title="Delete File"
        #      section="workspaces"/>
        return Element('view',
                       name="delete.html",
                       type="page",
                       title="Delete Keyword: " + self.context.Title(),
                       section="workspaces")
        return (context.aq_parent.absolute_url() +
                "/withkeyword-documents.html?" +
                urlencode(dict(keyword=sortable_title(context.Title()))))

class KeywordDeletePage(Page):
    views = (KeywordDeleteFragment, ) + COMMON_VIEWS

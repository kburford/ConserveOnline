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

from DateTime import DateTime

from Products.COL3.etree import Element

from zope.formlib import form
from Acquisition import aq_inner, aq_parent

from Products.CMFPlone.utils import normalizeString

from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.content.indexer import index as gsa_index
from Products.COL3.content.indexer import reindex as gsa_reindex
from Products.COL3.content.indexer import unindex as gsa_unindex

from Products.COL3 import config

from Products.COL3.formlib.xmlform import AddFormFragment, EditFormFragment
from Products.COL3.interfaces.calendar import IEventSchema
from Products.COL3.browser.base import SafeRedirect

# Event add and edit forms

class EventAddForm(AddFormFragment):

    form_fields = form.FormFields(IEventSchema)

    def provideInitialDefaults(self):
        defaults = {}
        request = self.request
        if request.get('ymd'):
            ymd = request.get('ymd').split('-')
            date = DateTime(int(ymd[0]), int(ymd[1]), int(ymd[2]))
            defaults['startDate'] = defaults['endDate'] = date
        return defaults

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)

        id = normalizeString(data['title'], encoding=config.CHARSET)
        context.invokeFactory("Event", id)
        event = context[id]
        event.update(**data)
        gsa_index(event)
        return event.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class EventAddView(Fragment):
    """ View class for event add view
    """

    def asElement(self):
        #<view name="add.html" type="event" title="Add Event" section="workspaces"/>
        return Element('view',
                       name="add.html",
                       type="event",
                       title="Add Event",
                       section="workspaces")

class EventAddPage(Page):

    views = (EventAddView, EventAddForm) + COMMON_VIEWS


class EventEditForm(EditFormFragment):

    form_fields = form.FormFields(IEventSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        schema = context.Schema()
        return dict((field.__name__, schema[field.__name__].getEditAccessor(context)())
                    for field in self.form_fields
                    if 'r' in schema[field.__name__].mode)

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        context.update(**data)
        # title and text of the first comment also need to be updated
        # XXX status message?
        gsa_reindex(context)
        return context.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class EventEditView(Fragment):
    """ Edit class for event add view
    """

    def asElement(self):
        #<view name="edit.html" type="event" title="Edit Upcoming Meeting" section="workspaces"/>
        return Element('view',
                       name="edit.html",
                       type="event",
                       title="Edit Event",
                       section="workspaces")

class EventEditPage(Page):

    views = (EventEditView, EventEditForm) + COMMON_VIEWS

class EventDeleteView(Fragment):
    """ View class for event delete views
    """

    def asElement(self):
        context = aq_inner(self.context)
        if self.request.get('confirm', None) is not None:
            # user has confirmed deletion
            # so delete the event
            calendar = aq_parent(context)
            calendar.manage_delObjects([context.id])
            gsa_unindex(context)
            # XXX status message
            raise SafeRedirect(calendar.absolute_url())
        # user hasen't confirmed yet, show confirmation view
        #<view name="delete.html" type="topic" title="Delete" section="workspaces"/>
        return Element('view',
                       name="delete.html",
                       type="event",
                       title="Delete Event",
                       section="workspaces")

class EventDeletePage(Page):

    views = (EventDeleteView,) + COMMON_VIEWS

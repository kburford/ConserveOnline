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

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.COL3.Extensions.process_subscriptions import build_query


class Base(BrowserView):
    """Base RSS feed class."""
    size = 20
    types = None
    sort_on = 'created'
    sort_order = 'reverse'

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        context = aq_inner(context)
        self.path = '/'.join(self.context.getPhysicalPath())
        self.catalog = getToolByName(context, 'portal_catalog')

    def query(self):
        query = {
            'path': self.path,
            'sort_limit': self.size,
            'sort_order': self.sort_order,
            'sort_on': self.sort_on,
        }
        if self.types:
            query['portal_type'] = self.types
        return query

    def results(self):
        return self.catalog(**self.query())[:self.size]


class FilesPages(Base):
    """Returns file and page items."""
    types = ('COLPage', 'COLFile')


class Events(Base):
    """Returns calendar event items."""
    types = ('Event',)


class Discussions(Base):
    """Returns discussion board post items."""
    types = ('PloneboardComment', 'PloneboardConversation')


class All(Base):
    """Returns all the content item items."""
    types = FilesPages.types + Events.types + Discussions.types


class UserSubscription(Base):
    """Returns the items that matches the user subscription criteria"""
    def results(self):
        pm = getToolByName(self.context, 'portal_membership')
        member = pm.getAuthenticatedMember()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        subscriptions = portal.subscriptions
        try:
            subscription = subscriptions['subscription_'+member.id]
        except KeyError:
            return []
        query = build_query(subscription, self.size)
        return portal.notification_catalog(**query)[:self.size]

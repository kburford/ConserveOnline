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

import sys, traceback, StringIO
from Products.COL3.etree import Element
from urllib import urlencode
from cgi import parse_qs

from zExceptions import Redirect
from zExceptions import Unauthorized, NotFound
from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite
from Products.Five.browser import BrowserView

from Acquisition import aq_inner, aq_acquire

from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs

from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.common import UserFragment
from Products.COL3.browser.common import BreadcrumbsFragment

# here we use the UserFragment that returns None if the user is not logged in
# instead of rendering the loginbox
COMMON_EXCEPTION_VIEWS = (BreadcrumbsFragment, UserFragment)

class ExceptionBreadcrumbs(PhysicalNavigationBreadcrumbs):
    """ Breadcrumbs view for Exceptions"""

    def breadcrumbs(self):
        request = self.request
        container = getSite()

        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())

        # our Exception pages have a .exception_label attribute
        # and this breadcrumb is supposed to be only called from our views...
        exception_label = getMultiAdapter((self.context, request),
                                          name='index.html').exception_label
        # XXX is this kosher? our views know how to handle having
        # absolute_url == None...
        base += ({'absolute_url': None,
                  'Title': exception_label,
                 },)

        return base

def registerException(context=None, msg=None):
    """ Register an exception currently being handled into the error_log
        object for the current site (or the closest one on acquisition).
    """
    site = getSite()
    try:
        log = aq_acquire(site, '__error_log__', containment=1)
    except AttributeError:
        import logging
        logger = logging.getLogger('COL3.browser.exceptions')
        logger.error('could not register exception into error_log for site: %r' % site)
    else:
        if context and not isinstance(context, Redirect) and not isinstance(context, NotFound):
            smt = simple_mail_tool()
            smt.sendAdminErrorEmail(msg) 
        return log.raising(sys.exc_info())

class UnauthorizedRedirect(BrowserView):
    def __call__(self):
        registerException()
        # where we came from...
        request = self.request
        qstring = request.get("QUERY_STRING", '')
        if qstring:
            qstring = '?' + qstring
        from_url = request['URL'] + qstring
        came_from = urlencode(dict(came_from=from_url))
        # where we are going...
        portal = getSite()
        unauth_url = portal.absolute_url() + "/unauthorized?" + came_from
        raise Redirect(unauth_url)


class UnauthorizedViewFragment(Fragment):
    """ Unauthorized view fragment

    used for both unauthenticated accesses and accesses from authenticated
    users with not enough privileges.
    """

    def fromURL(self):
        """ find out where we were triggered, with query string and all """
        qstring = self.request.get('QUERY_STRING', '')
        qparams = parse_qs(qstring)
        came_from, = qparams.get('came_from', (None,))
        return came_from or self.context.absolute_url()

    def asElement(self):
        """
        <view name="unauthorized-error.html" type="site" title="Unauthorized"
              section="home"/>
        """
        portal = aq_inner(self.context)
        pm = cmfutils.getToolByName(portal, 'portal_membership')
        # Different actions when we're authenticated or not
        if pm.isAnonymousUser():
            # anonymous users get redirected to the login screen, with a
            # came_from parameter pointing to the URL that raised the unauth
            came_from = urlencode(dict(came_from=self.fromURL()))
            login_url = portal.absolute_url() + "/login.html?" + came_from
            raise Redirect(login_url)
        # Non anonymous users get a pretty "You are not authorized" screen
        #self.request.response.setStatus(Unauthorized)
        return Element('view',
                       name="unauthorized-error.html",
                       type="site",
                       title="Unauthorized",
                       section="home")

class UnauthorizedPage(Page):

    views = (UnauthorizedViewFragment, ) + COMMON_EXCEPTION_VIEWS

class ExceptionViewFragment(Fragment):
    """ Fragment view for a generic exception """

    def asElement(self):
        """
        <view name="generic-error.html" type="site" title="Whoops!"
              section="site"/>
        """
        #import pdb; pdb.set_trace()
        et, ev, tb = sys.exc_info()
        msg = "Whoops! Error for: " + self.request.getURL()
        msg = msg + "\nRequest forwarded for: " + self.request['HTTP_X_FORWARDED_FOR']
        msg = msg + "\nException info: \n" + str(et) + ":" + str(ev)
        msg = msg + "\n" + " ".join(traceback.format_tb(tb))
        registerException(context=self.context, msg=msg)
        # re-raise redirect, since we are called to handle it as well
        if et is Redirect:
            raise et, ev, tb
        self.request.response.setStatus(200, lock=True)
        currenturl = self.request['URL']
        return Element('view',
                       name="generic-error.html",
                       currenturl=currenturl,
                       type="site",
                       title="Whoops!",
                       section="site")

class ExceptionPage(Page):
    """Page for rendering a generic exception"""
    exception_label = u"Error"

    views = (ExceptionViewFragment, ) + COMMON_EXCEPTION_VIEWS

    def __call__(self):
        # for some reason, the rendering of generic exceptions was being
        # repr()'d
        # now we force the output directly to the browser
        result = Page.__call__(self)
        self.request.response.write(result)
        return ''

class NotFoundViewFragment(Fragment):
    """ Fragment view for a NotFound exception """

    def asElement(self):
        """
        <view name="notfound-error.html" type="site" title="Not Found"
              section="site"/>
        """
        msg = "Not Found Error for: " + self.request.getURL()
        msg = msg +  "\nRequest forwarded for: " + self.request['HTTP_X_FORWARDED_FOR']
        registerException(context=self.context, msg=msg)
        self.request.response.setStatus(200, lock=True)
        return Element('view',
                       name="notfound-error.html",
                       type="site",
                       title="Not Found",
                       section="site")

class NotFoundPage(Page):
    """Page for rendering a NotFound exception """
    exception_label = u"Not Found"

    views = (NotFoundViewFragment, ) + COMMON_EXCEPTION_VIEWS

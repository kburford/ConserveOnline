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
from itertools import islice
from urlparse import urlsplit
from Products.COL3.etree import Element

from zope.app.component.hooks import getSite
from zope.formlib.form import FormBase

from Acquisition import aq_chain, aq_inner, aq_parent
from Products.Five import BrowserView
from Products.COL3 import config
from Products.COL3.content.workspace import Workspace
from Products.COL3.browser.utils import toStringWithPreamble
#from Products.COL3.browser.pageelements import ResourceView, UserView

def createViewNode(attributes):
    """ Creates a view node with attribs """
    return Element('view', attributes.copy())

class ResultSet(object):

    def __init__(self, iterable, total):
        self.iterable = iterable
        self.total = total

    def __len__(self):
        return self.total

    def __iter__(self):
        return iter(self.iterable)

    def __getitem__(self, s):
        single = False
        start = stop = step = None
        if isinstance(s, slice):
            start = s.start
            end = s.stop
            step = s.step
        elif isinstance(s, int):
            start = s
            end = s + 1
        else:
            raise TypeError('Expecting slice')
        if step is None:
            step = 1
        result = islice(self, start, end, step)
        if single:
            return list(result)[0]
        return result

class SafeRedirect(Exception):
    """ Redirect exception raised by fragments that want to cause a redirect
    but still commit the transaction.

    It purposefully does not extend zExceptions.Redirect since it could silently lose
    uncommited data """

    def __init__(self, *args):
        self.url = args[0]
        Exception.__init__(self, *args)

class Page(BrowserView):

    views = () # Subclasses should override this.
    xtra_breadcrumb_ids = None
    _stylesheet = "/shared/renderer.xsl"

    @property
    def stylesheet(self):
        portal = getSite()
        url = portal.absolute_url()
        # If we're on https, assume it's the default port and there's a server
        # on the default http port serving the same thing.
        # This is needed because something on the enfold.lxml apache stack
        # can't handle https urls
        return (url + self._stylesheet).replace("https://", "http://")

    def disableXSLT(self):
        request = self.request
        # current url has a xslt_disable=1
        query = request.get('QUERY_STRING','')
        if "xslt_disable=1" in query.split("&"):
            return True

        # last page before a post had an xslt_disable_on_post
        referer = request.get('HTTP_REFERER')
        if not referer:
            return False
        dummy, dummy, dummy, query, dummy = urlsplit(referer)
        if "xslt_disable_on_post=1" in query.split("&"):
            return True

    def getResponse(self):
        context = self.context
        request = self.request
        tree = Element('response')
        for view in self.views:
            __traceback_info__ = (self.__class__, "rendering fragment", view)
            if self.xtra_breadcrumb_ids and view.__name__.endswith('BreadcrumbsFragment'):
                element = view(context, request).asElement(xtra_breadcrumb_ids=self.xtra_breadcrumb_ids)
            else:
                element = view(context, request).asElement()
            if element is not None:
                tree.append(element)
        return tree

    def __call__(self):
        assert self.stylesheet is not None, 'no stylesheet set for this view'
        request = self.request
        response = request.response
        try:
            tree = self.getResponse()
        except (SafeRedirect,), r:
            return response.redirect(r.url)

        response.setHeader('Content-Type',
                           'text/xml; charset=' + config.CHARSET)
        response.setHeader('X-Col-Qstring', request.get('QUERY_STRING',''))
        response.setHeader('X-Col-Url', request['ACTUAL_URL'])
        if not self.disableXSLT():
            response.setHeader('Xsltstylesheet', self.stylesheet)
        return toStringWithPreamble(tree)

class AjaxPage(Page):
    """This is for a page that just returns a chunk of xml to the frontend"""
    def __call__(self):
        context = self.context
        request = self.request
        response = request.response
        element = self.views[0](context, request).asElement()

        response.setHeader('Content-Type',
                           'text/xml; charset=' + config.CHARSET)
        if not element:
            element = Element('batch')
        return toStringWithPreamble(element)

class Fragment(BrowserView):

    def asElement(self):
        raise NotImplementedError, 'asElement'

    def __call__(self):
        raise ValueError('XML Fragments are not supposed to be called '
                         'directly, but included in other views ')

class XMLViewBase(BrowserView): # XXX Remove
    """ View class for XML based content """

    def __init__(self, context, request):
        result = super(XMLViewBase, self).__init__(context, request)
        #pp = cmfutils.getToolByName(context, 'portal_properties')
        #charset = pp.site_properties.default_charset
        request.response.setHeader('Content-Type',
                                   'text/xml; charset=' + config.CHARSET)
        request.response.setHeader('X-Col-Qstring', request.get('QUERY_STRING',''))
        request.response.setHeader('X-Col-Url', request['ACTUAL_URL'])
        return result

class XMLView(XMLViewBase): # XXX Remove
    """ View class for xml based content, including an 'update' method
    That is called immediately before rendering """

    def update(self):
        """ Update method, like grok views. Override in subclasses to do stuff
        before the actual call """
        pass

    def __call__(self):
        self.update()
        # call ZPT based template:
        return super(XMLView, self).__call__()

    def renderXML(self):
        from Products.COL3.browser.common import COMMON_VIEWS
        context = self.context
        request = self.request
        tree = Element('response')
        for view in COMMON_VIEWS:
            element = view(context, request).asElement()
            if element is not None:
                tree.append(view(context, request).asElement())
        return tree

    def _isInAWorkspace(self, context):
        chain = aq_chain(aq_inner(context))
        return Workspace in [f.__class__ for f in chain]


class XSLTView(XMLView): # XXX Remove
    _stylesheet = "/shared/renderer.xsl"

    @property
    def stylesheet(self):
        portal = self.context.portal_url.getPortalObject()
        url = aq_parent(aq_inner(portal)).absolute_url()
        # If we're on https, assume it's the default port and there's a server
        # on the default http port serving the same thing.
        # This is needed because something on the enfold.lxml apache stack
        # can't handle https urls
        return (url + self._stylesheet).replace("https://", "http://")

    def maybeDisableXSLTOnPost(self):
        referer =  self.request.get('HTTP_REFERER')
        if not referer:
            return
        dummy, dummy, dummy, query, dummy = urlsplit(referer)
        if "xslt_disable_on_post=1" in query.split("&"):
            self.request.response.setHeader('Xslt-Disable', '1')

    def __init__(self, context, request):
        result = super(XSLTView, self).__init__(context, request)
        self.maybeDisableXSLTOnPost()
        assert self.stylesheet is not None, 'no stylesheet set for this view'
        self.request.response.setHeader('Xsltstylesheet', self.stylesheet)
        return result


class XMLFormBase(FormBase): # XXX Remove
    """ Formlib base class for XML-based content
    """

    def __init__(self, context, request):
        result = super(XMLFormBase, self).__init__(context, request)
        resp = request.response

        resp.setHeader('Content-Type', 'text/xml; charset=utf-8')
        resp.setHeader('X-Col-Qstring', request.get('QUERY_STRING',''))
        resp.setHeader('X-Col-Url', request['ACTUAL_URL'])

        return result


class XMLFormView(XMLFormBase): # XXX Remove
    pass

class XSLTFormView(XMLFormBase): # XXX Remove

    #stylesheet = "/shared/renderer.xsl"

    @property
    def stylesheet(self):
        portal = self.context.portal_url.getPortalObject()
        url = aq_parent(aq_inner(portal)).absolute_url()
        # If we're on https, assume it's the default port and there's a server
        # on the default http port serving the same thing.
        # This is needed because something on the enfold.lxml apache stack
        # can't handle https urls
        return ('%s/shared/renderer.xsl' % url).replace("https://", "http://")

    def __init__(self, context, request):
        result = super(XSLTFormView, self).__init__(context, request)
        self.maybeDisableXSLTOnPost()
        assert self.stylesheet is not None, 'no stylesheet set for this view'
        self.request.response.setHeader('Xsltstylesheet', self.stylesheet)
        return result

    def maybeDisableXSLTOnPost(self):
        referer = self.request.get('HTTP_REFERER')
        if not referer:
            return

        dummy, dummy, dummy, query, dummy = urlsplit(referer)
        if 'xslt_disable_on_post=1' in query:
            self.request.response.setHeader('Xslt-Disable', '1')


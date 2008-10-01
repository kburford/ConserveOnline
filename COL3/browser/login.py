from urlparse import urlsplit, urlunsplit
from urllib import urlencode

from Acquisition import aq_inner
from Products.CMFCore import utils as cmfutils
from Products.Five import BrowserView

from Products.COL3.config import FAILED_LOGIN_PARAMETER
from Products.COL3.browser.utils import getBaseUrl
from Products.COL3.browser.base import Page, Fragment
from Products.COL3.browser.common import BreadcrumbsFragment
from Products.COL3.browser.common import UserOrLoginboxFragment
from Products.COL3.etree import Element
from cgi import parse_qs
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.etree import SubElement
from Products.CMFCore.utils import getToolByName

class XMLAuthenticatedView(BrowserView):

    regularLogin = failedLogin = authenticatedUserURL = None
    loginURL = "/login"

    def __call__(self):
        purl = cmfutils.getToolByName(self.context, 'portal_url')()
        self.loginURL = purl + "/login"
        # set variables that help decide whether to show the "welcome" message
        # or the loginbox, and if the loginbox, whether we need to display an
        # authentication error.
        mt = cmfutils.getToolByName(self.context, 'portal_membership')
        if mt.isAnonymousUser():
            self.failedLogin = self.request.form.get(FAILED_LOGIN_PARAMETER,
                                                     None)
            if self.failedLogin is None:
                self.regularLogin = True
        else:
            # self.authenticatedUserURL = mt.getAuthenticatedMember().absolute_url()
            self.authenticatedUserURL = purl

        return super(XMLAuthenticatedView, self).__call__()

def _remove_login_failure(query_string):
    """ _remove_login_failure(query_string) -> query_string

    Extracts the failed login parameter (and value) from the query string if
    there is one:

      >>> _remove_login_failure('foo=bar&login_failed=myusername&spam=eggs')
      'foo=bar&spam=eggs'
      >>> _remove_login_failure('login_failed=myusername')
      ''

    If the query string doesn't contain the failed paramter, it should be
    returned as it was:

      >>> _remove_login_failure('')
      ''
      >>> _remove_login_failure('foo=bar&spam=eggs')
      'foo=bar&spam=eggs'
    """
    match = FAILED_LOGIN_PARAMETER + "="
    return "&".join([parameter for parameter in query_string.split("&")
                     if not parameter.startswith(match)])

def _add_login_failure(query_string, username):
    sufix = urlencode([(FAILED_LOGIN_PARAMETER, username)])
    if query_string:
        return query_string + "&" + sufix
    else:
        return sufix


class LoginView(BrowserView):
    def __call__(self):
        mt = cmfutils.getToolByName(self.context, 'portal_membership')
        from_url = self.request.get('HTTP_REFERER', '')
        if (not from_url or
            from_url == 'localhost'): # stupid testbrowser bug workaround
            from_url = self.context.absolute_url()
        elif from_url and from_url.endswith('logout.html'):
            ptool = getToolByName(self.context, 'portal_url')
            from_url = ptool.getPortalObject().absolute_url()
        proto, server, path, query, fragment = urlsplit(from_url)
        query = _remove_login_failure(query)

        # logins are preprocessed during traversal by PAS extractors
        # so, by now, the membership tool already knows if we're
        # logged in or not
        if mt.isAnonymousUser():
            # add the failed login notification to the URL query string
            username = self.request.form['__ac_name']
            query = _add_login_failure(query, username)
        else:
            # we're logged in, just set the cookie
            acl_users = cmfutils.getToolByName(self.context, 'acl_users')
            acl_users.credentials_cookie_auth.login()
            mt.setLoginTimes()

        # redirect to where we came from
        from_url = urlunsplit((proto, server, path, query, fragment))
        self.request.response.redirect(from_url)

class Logout(BrowserView):
    def logout(self):
        # code lifted from CMFPlone/skins/plone_login/logout.cpy
        # delegate to PAS reset-credentials code
        acl_users = cmfutils.getToolByName(self.context, 'acl_users')
        acl_users.logout(self.request)
        # kill user session
        sdm = cmfutils.getToolByName(self.context, 'session_data_manager', None)
        if sdm is not None:
            session = sdm.getSessionData(create=0)
            if session is not None:
                session.invalidate()
        url = '%s%s' % (getBaseUrl(self.context, self.request), 'logout.html')
        self.request.response.redirect(url)

class LogoutViewFragment(Fragment):
    """ <view name="logout.html" type="site" title="Signed Out" section="people"/>  """
    def asElement(self):
        return Element('view',
                       name='logout.html',
                       type='site',
                       title='Signed Out',
                       section='people',)

class LogoutViewPage(Page):
    views = (LogoutViewFragment, UserOrLoginboxFragment, BreadcrumbsFragment)

class CreateOrUpdateProfileView(BrowserView):
    """ View for the 'Create/Update your profile' link """

    def __call__(self):
        request = self.request
        context = self.context
        mship = cmfutils.getToolByName(context, 'portal_membership')
        if mship.isAnonymousUser():
            # create!
            return request.response.redirect(context.absolute_url() + '/register.html')
        # update!
        url = mship.getAuthenticatedMember().absolute_url() + '/edit.html'
        return request.response.redirect(url)

class LoginViewFragment(Fragment):
    """ <view name="login.html" type="site" title="Sign In" section="people"/>  """

    def currentURL(self):
        request = self.request
        qstring = request.get("QUERY_STRING", '')
        if qstring:
            qstring = '?' + qstring
        return request['URL'] + qstring

    def getDestination(self):
        qstring = self.request.get('QUERY_STRING', '')
        qparams = parse_qs(qstring)
        came_from, = qparams.get('came_from', (None,))
        return came_from

    def asElement(self):
        request = self.request
        context = aq_inner(self.context)
        mt = cmfutils.getToolByName(context, 'portal_membership')
        came_from = self.getDestination() or context.absolute_url()
        # force redirection into http if in https
        came_from = came_from.replace('https://', 'http://')
        if not mt.isAnonymousUser():
            # user successfully logged in
            if request.form.get('loginsubmitted'):
                acl_users = cmfutils.getToolByName(self.context, 'acl_users')
                acl_users.credentials_cookie_auth.login()
                mt.setLoginTimes()
            raise SafeRedirect(came_from)

        view_tag = Element('view',
                           name='login.html',
                           type='site',
                           title='Sign In',
                           section='people',
                           href=self.currentURL())
        if request.form.get('loginsubmitted'):
            # form submitted but we're still anonymous,
            # render the <failed> tag
            SubElement(view_tag, 'failed',
                       username=request.form['__ac_name'])
        return view_tag

class LoginViewPage(Page):
    views = (LoginViewFragment, UserOrLoginboxFragment, BreadcrumbsFragment)

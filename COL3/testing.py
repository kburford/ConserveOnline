# COL3
# Copyright(C), 2007, Enfold Systems, Inc. - ALL RIGHTS RESERVED
#
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied
# this software.  Any inquiries concerning the scope or
# enforceability of the license should be addressed to:
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# Prepare ZopeTestCase ZODB for blob
from plone.app.blob import db
del db

from AccessControl.SecurityManagement import newSecurityManager
from Testing import ZopeTestCase
import transaction


from zope.component import getSiteManager

from Products.MailHost.interfaces import IMailHost
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.setup import portal_owner
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.SecureMailHost.SecureMailHost import SecureMailHost

ZopeTestCase.installProduct('PlonePAS')
ZopeTestCase.installProduct('PluggableAuthService')
ZopeTestCase.installProduct('Sessions')
ZopeTestCase.installProduct('validation')
ZopeTestCase.installProduct('qPloneCaptchas')
ZopeTestCase.installProduct('Ploneboard')
ZopeTestCase.installProduct('CachedGSAIndexer')
ZopeTestCase.installProduct('COL3')

setupPloneSite()

class DummyMailHost(SecureMailHost):
    """ No mail allowed!
    """
    def __init__(self, *args, **kw):
        super(DummyMailHost, self).__init__(*args, **kw)
        self.sent = []

    def send(self, *args, **kw):
        """ Append messages for later perusal """
        self.sent.append((args, kw))

    _send = send

class COL3FunctionalLayer(PloneSite):

    @classmethod
    def setUp(cls):
        """ Apply the COL3 profile to the site
        """
        app = ZopeTestCase.app()
        qi_tool = app.plone.portal_quickinstaller

        # Need to log in as the portal owner
        user = app.acl_users.getUserById(portal_owner)
        newSecurityManager(None, user)

        # Install COL3
        qi_tool.installProduct('COL3')

        # replace the MailHost so tests will not send email
        sm = getSiteManager(context=app.plone)
        sm.unregisterUtility(app.plone.MailHost, IMailHost)
        app.plone.MailHost = DummyMailHost(id='MailHost')
        sm.registerUtility(app.plone.MailHost, IMailHost)

        transaction.commit()
        ZopeTestCase.close(app)

    @classmethod
    def tearDown(cls):
        pass

class COL3FunctionalTestCase(FunctionalTestCase):
    """ Functional COL3 test case class for subclassing

    Provides a fully-formed COL3 portal
    """
    layer = COL3FunctionalLayer


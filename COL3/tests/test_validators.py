# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED
from Products.COL3.exceptions import InvariantError

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: test_validators.py 23095 2007-09-28 20:15:15Z leo $

import unittest

from Products.COL3.testing import COL3FunctionalTestCase
from Products.COL3.tests.dummy import DummyMembershipTool
from Products.COL3.tests.dummy import DummyRegistrationTool
from Products.COL3.tests.dummy import SimpleObject


class ValidatorTests(unittest.TestCase):

    def test_validate_email(self):
        # Email must conform to a usable format as described in 
        # the relevant RFCs. 
        from Products.COL3.validators import validateEmail
        from Products.COL3.exceptions import InvalidEmailError

        self.assertRaises(InvalidEmailError, validateEmail, '')
        self.assertRaises(InvalidEmailError, validateEmail, 'john@doe')
        self.assertRaises(InvalidEmailError, validateEmail, '@doe.com')

        self.failUnless(validateEmail('john.doe@example.com'))

    def test_validate_agreement(self):
        # This validator uses a simple truth test.
        from Products.COL3.validators import validateAgreement
        from Products.COL3.exceptions import InvalidAgreementError

        self.assertRaises(InvalidAgreementError, validateAgreement, '')
        self.assertRaises(InvalidAgreementError, validateAgreement, None)
        self.assertRaises(InvalidAgreementError, validateAgreement, 0)
        
        self.failUnless(validateAgreement(True))
        self.failUnless(validateAgreement(1))

    def test_validate_password(self):
        # Passwords must be 8 characters or longer.
        from Products.COL3.validators import validatePassword
        from Products.COL3.exceptions import PasswordTooShortError

        self.assertRaises(PasswordTooShortError, validatePassword, '')
        self.assertRaises(PasswordTooShortError, validatePassword, 'secret1')

        self.failUnless(validatePassword('secret12'))

    def test_validate_password_confirmation_login(self):
        # The password and confirmation must be the same, but the
        # password may not be the same as the login.
        from Products.COL3.validators import validatePasswordConfirmationLogin

        # password and confirmation don't match
        obj = SimpleObject( password = '5ecret'
                          , confirm = 'secret'
                          , id = 'humptydumpty'
                          )
        self.assertRaises( InvariantError
                         , validatePasswordConfirmationLogin
                         , obj
                         )

        # password and login are the same
        obj = SimpleObject( password = 'humptydumpty'
                          , confirm = 'humptydumpty'
                          , username = 'humptydumpty'
                          )
        self.assertRaises( InvariantError
                         , validatePasswordConfirmationLogin
                         , obj
                         )

        # this one shold work.
        obj = SimpleObject( password = 'humptydumpty123'
                          , confirm = 'humptydumpty123'
                          , username = 'humptydumpty'
                          )
        self.failUnless(validatePasswordConfirmationLogin(obj))


class FunctionalValidatorTests(COL3FunctionalTestCase):
    """ Validator tests that require a fully-formed COL3 portal
    """

    def test_validate_password_confirmation_login_loggedin(self):
        # The password and confirmation must be the same, but the
        # password may not be the same as the login. This validator
        # is used for password changing as opposed to password resetting.
        from Products.COL3.validators import \
            validatePasswordConfirmationLoginLoggedin
        from Products.COL3.exceptions import PasswordConfirmationMatchError
        from Products.COL3.exceptions import PasswordLoginMatchError

        # We need a membership tool for this test
        self.portal.portal_membership = DummyMembershipTool()

        # password and confirmation don't match
        obj = SimpleObject( password = '5ecret'
                          , confirm_password = 'secret'
                          , id = 'humptydumpty'
                          )
        self.assertRaises( PasswordConfirmationMatchError
                         , validatePasswordConfirmationLoginLoggedin
                         , obj
                         )

        # The DummyMembershipTool acts as if a user named "dummy" is logged in
        # password and login match
        obj = SimpleObject( password = 'dummy'
                          , confirm_password = 'dummy'
                          , id = 'dummy'
                          )
        self.assertRaises( PasswordLoginMatchError
                         , validatePasswordConfirmationLoginLoggedin
                         , obj
                         )

        # this should go through OK
        obj = SimpleObject( password = 'humptydumpty123'
                          , confirm_password = 'humptydumpty123'
                          , id = 'humptydumpty'
                          )
        self.failUnless(validatePasswordConfirmationLoginLoggedin(obj))

    def test_validate_login_exists(self):
        # For the password reset screen, we need to validate that the login
        # the user provides actually exists in the system.
        from Products.COL3.validators import \
            validateLoginExists
        from Products.COL3.exceptions import LoginDoesNotExistError

        # We need a membership tool for this test
        # This tool only has one member: "dummy"
        self.portal.portal_membership = DummyMembershipTool()

        self.assertRaises( LoginDoesNotExistError
                         , validateLoginExists
                         , 'notexisting'
                         )
        self.failUnless(validateLoginExists('dummy'))

    def test_validate_login(self):
        # This validator ensures there is no login of the same name in the
        # system, it is used for the member registration view.
        from Products.COL3.validators import \
            validateLogin
        from Products.COL3.exceptions import LoginExistsError

        # We need a registration tool for this test
        # This tool only knowsn about one member: "dummy"
        self.portal.portal_registration = DummyRegistrationTool()

        self.assertRaises(LoginExistsError, validateLogin, 'dummy')
        self.failUnless(validateLogin('notexisting'))

    def test_validate_captcha(self):
        from Products.COL3.exceptions import CaptchaError
        from Products.COL3.validators import validateCaptcha
        from Products.qPloneCaptchas.utils import decrypt
        from Products.qPloneCaptchas.utils import getWord
        from Products.qPloneCaptchas.utils import parseKey

        captcha_key = self.portal.captcha_key

        # First, submit a wrong key
        hash = self.portal.portal_skins.plone_captchas.dynamic.getCaptcha()
        key = 'wrongkey'
        obj = SimpleObject(key=key, keyhash=hash)
        self.assertRaises(CaptchaError, validateCaptcha, obj)

        # Now submit a correct captcha
        hash = self.portal.portal_skins.plone_captchas.dynamic.getCaptcha()
        key = getWord(int(parseKey(decrypt(captcha_key, hash))['key']))
        obj = SimpleObject(key=key, keyhash=hash)
        self.failUnless(validateCaptcha(obj))

        # Trying to submit the correct key again should raise the error
        self.assertRaises(CaptchaError, validateCaptcha, obj)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ValidatorTests),
        unittest.makeSuite(FunctionalValidatorTests),
        ))


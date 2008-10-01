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
from Products.COL3.exceptions import InvariantError
from Products.COL3.exceptions import InvalidWorkspaceTitleError
from Products.COL3.exceptions import InvalidImageFile
from Products.COL3.exceptions import UseridDoesNotExistError

import re
import time

from zope.app.component.hooks import getSite


from Products.CMFCore.utils import getToolByName
from Products.qPloneCaptchas.utils import decrypt
from Products.qPloneCaptchas.utils import getWord
from Products.qPloneCaptchas.utils import parseKey

from Products.COL3.config import CHARSET
from Products.COL3.exceptions import BadPasswordError
from Products.COL3.exceptions import CaptchaError
from Products.COL3.exceptions import InvalidAgreementError
from Products.COL3.exceptions import InvalidEmailError
from Products.COL3.exceptions import LoginDoesNotExistError
from Products.COL3.exceptions import LoginExistsError
from Products.COL3.exceptions import PasswordConfirmationMatchError
from Products.COL3.exceptions import PasswordLoginMatchError
from Products.COL3.exceptions import PasswordTooShortError
from Products.COL3.exceptions import LoginEmailMismatchError
from Products.COL3.exceptions import InvalidFiletypeError
from Products.COL3.exceptions import InvalidFileSizeError

captcha_divider = ':::'
email_regex = r"^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$"
check_email = re.compile(email_regex, re.IGNORECASE).match

def _validateCaptchaValues(key, keyhash):
    """ Make sure the typed-in value for the captcha is valid

    - the typed-in key must match the key stored with the keyhash
    - the keyhash/key has not been used before
    - the keyhash/key was generated less than 1 hour ago
    """
    portal = getSite()
    captcha_tool = getToolByName(portal, 'portal_captchas')

    if not keyhash:
        raise RuntimeError("Keyhash is empty")
    decrypted_key = decrypt(portal.captcha_key, keyhash)
    if not decrypted_key:
        raise RuntimeError("Invalid Keyhash")
    parsed_key = parseKey(decrypted_key)

    index = parsed_key['key']
    date = parsed_key['date']
    solution = getWord(int(index))

    if ( key != solution or
         captcha_tool.has_key(decrypted_key) or
         time.time() - float(date) > 3600 ):
        raise CaptchaError
    else:
        captcha_tool.addExpiredKey(decrypted_key)
        return True

def validateCaptcha(obj):
    """ Captcha validation from a web page
    """
    return _validateCaptchaValues(obj.key, obj.keyhash)

def validateXMLCaptcha(value):
    """ Captcha validation from COl3 XML
    """
    key, keyhash = value.split(captcha_divider)
    return _validateCaptchaValues(key, keyhash)

def validateCurrentPassword(value):
    """ Validate the currently logged-in user's password against the given value
    """
    pwd = value.encode(CHARSET)
    portal = getSite()
    membership_tool = getToolByName(portal, 'portal_membership')
    member = membership_tool.getAuthenticatedMember()
    user_manager = membership_tool.acl_users.source_users
    credentials = {'login' : member.getId(), 'password' : pwd}

    if not user_manager.authenticateCredentials(credentials):
        raise BadPasswordError(value)

    return True

def validateWorkspaceTitle(value):
    """ Validate that the workspace title doesn't exist in the system
    """
    portal = getSite()
    pcat = getToolByName(portal, 'portal_catalog')
    workspaces = pcat.searchResults(portal_type='Workspace')
    
    if value in [unicode(r.Title,'utf-8') for r in workspaces]:
        raise InvalidWorkspaceTitleError(value)

    return True

def validateImageFile(value):
    """ Validates that the uploaded "portrait" is a valid image file """
    try:
        content_type = value.headers.get('content-type', '')
        if not content_type.startswith('image'):
            raise InvalidImageFile(value)
    except AttributeError, e:
        import logging
        logger = logging.getLogger('Products.COL3.validators')
        logger.error('During testing \"value\" is a stringIO object... ('+e.__class__.__name__, ":", str(e)+')')
    return True

def validateLogin(value):
    """ Use the registration tool to check for duplicate login
    """
    portal = getSite()
    registration_tool = getToolByName(portal, 'portal_registration')

    if not registration_tool.isMemberIdAllowed(value):
        raise LoginExistsError

    return True

def validateUserID(value):
    """ Use the registration tool to check for duplicate login
    """
    portal = getSite()
    pmem = getToolByName(portal, 'portal_membership')
    member = pmem.getMemberById(value)
    if not member:
        raise UseridDoesNotExistError
    return True

def validateLoginExists(value):
    """ Use the membership tool to check for a login
    """
    portal = getSite()
    membership_tool = getToolByName(portal, 'portal_membership')

    if membership_tool.getMemberById(value) is None:
        raise LoginDoesNotExistError(value)

    return True

def validateLoginMatchesEmail(obj):
    """ Use the membership tool to check for a login
    """
    portal = getSite()
    membership_tool = getToolByName(portal, 'portal_membership')

    member = membership_tool.getMemberById(obj.login)
    if member is None:
        raise LoginEmailMismatchError()

    if member.getProperty('email') != obj.email:
        raise LoginEmailMismatchError()
    return True

def validateEmail(value):
    """ Validate an email address
    """
    if not check_email(value):
        raise InvalidEmailError(value)

    return True

def validateAgreement(value):
    """ The user must click on the agreement
    """
    if not value:
        raise InvalidAgreementError(value)

    return True

def validatePassword(value):
    """ The password must be 8 characters or more
    """
    if len(value) < 8:
        raise PasswordTooShortError(value)

    return True

def validateFileSize(obj):
    """ File uploads cannot exceed 2 gigs """
    if obj:
        two_gigs = 2*(1024*1024*1024)
        obj.seek(0)
        if len(obj.read()) > two_gigs:
            raise InvalidFileSizeError(obj.filename)
    return True

def validateGISFileMimetype(obj):
    if obj.headers['content-type'] != 'text/xml':
        raise InvalidFiletypeError(obj.filename)
    return True

def validatePasswordConfirmationLogin(obj):
    """ Ensure that password and confirmation match, and login != password
    """
    if obj.password != obj.confirm:
        raise InvariantError(u'Password and password confirmation do not match.',
                             fields=('password', 'confirm'))

    if obj.password == obj.username:
        raise InvariantError(u'Login and password may not be the same.',
                             fields=('password', 'username'))

    return True

def validatePasswordReset(obj):
    """ Make sure that the userid entered is valid and that the passwords entered
        match
    """
    pwd = obj.password
    pwdcon = obj.confirm
    if (not pwd or not pwdcon or (pwd != pwdcon)):
        message = u'Password and password confirmation must be the same.'
        raise InvariantError(message, fields=('password', 'confirm', ))
    return True
        
        
def validatePasswordChangePreferences(obj):
    """ Ensure that password and confirmation match, and login != password
    """
    currentpwd = ''
    portal = getSite()
    membership_tool = getToolByName(portal, 'portal_membership')
    member = membership_tool.getAuthenticatedMember()
    name = member.getId()
    if obj.old_password:
        currentpwd = (obj.old_password).encode('ascii')
    newpwd = obj.password
    newpwdconfirm = obj.confirm_password
    request = portal.REQUEST
    if not (not currentpwd and not newpwd and not newpwdconfirm):
        if getToolByName(portal, 'acl_users').authenticate(name, currentpwd, request) is None:
            message = u'Current password entered does not match the actual current password.'
            raise InvariantError(message, fields=('old_password', ))
        if newpwd != newpwdconfirm:
            message = u'Password and password confirmation must be the same.'
            raise InvariantError(message, fields=('password', 'confirm_password'))
    return True

def validatePasswordConfirmationLoginLoggedin(obj):
    """ Ensure that password and confirmation match, and login != password

    This version is for changing a password as a logged-in user, and we
    do not have or accept login information in the form
    """
    if obj.password != obj.confirm_password:
        raise PasswordConfirmationMatchError

    portal = getSite()
    membership_tool = getToolByName(portal, 'portal_membership')
    member = membership_tool.getAuthenticatedMember()
    
    if obj.password == member.getId():
        raise PasswordLoginMatchError

    return True


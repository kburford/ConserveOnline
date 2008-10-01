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

from zope.app.form.interfaces import IWidgetInputError
from zope.interface import implements
from zope.schema.interfaces import ValidationError
from zope.exceptions.interfaces import UserError
from zope.interface.exceptions import Invalid

class BadPasswordError(ValidationError):
    __doc__ = u'Current password invalid.'

class CaptchaError(ValidationError):
    __doc__ = u'Please re-enter verification code.'

class InvalidAgreementError(ValidationError):
    __doc__ = u'You must agree to the ConserveOnline notices and disclaimers.'

class InvalidEmailError(ValidationError):
    __doc__ = u'Invalid email address.'

class LoginDoesNotExistError(ValidationError):
    __doc__ = u'This login does not exist.'

class UseridDoesNotExistError(ValidationError):
    __doc__ = u'No user exists for the id entered.'

class LoginExistsError(ValidationError):
    __doc__ = u'This login already exists, please choose another.'

class PasswordConfirmationMatchError(ValidationError):
    __doc__ = u'Password and password confirmation do not match.'

class InvalidFiletypeError(ValidationError):
    __doc__ = u'The file (%s) supplied is not an xml file (of type text/xml).'
    def doc(self):
        return self.__class__.__doc__ % self

class InvalidFileSizeError(ValidationError):
    __doc__ = u'The file (%s) supplied exceeds the allowed size of 2 gigabytes.'
    def doc(self):
        return self.__class__.__doc__ % self

class PasswordLoginMatchError(ValidationError):
    __doc__ = u'Login and password may not be the same.'

    # Needed to show the error on the form when doing invariant checking
    implements(IWidgetInputError)

class LoginEmailMismatchError(ValidationError):
    __doc__ = u'Login does not exist or does not match provided e-mail.'

    # Needed to show the error on the form when doing invariant checking
    implements(IWidgetInputError)

class PasswordTooShortError(ValidationError):
    __doc__ = u'Please use a password that is at least 8 characters long.'

class InvalidWorkspaceTitleError(ValidationError):
    __doc__ = u'Workspace title already exists, please enter another title.'

class InvalidImageFile(ValidationError):
    __doc__ = u'The uploaded image is not a valid image file, please choose another file.'

class AlreadyWorkspaceMember(Exception):
    u""" Member already belongs to workspace """

class JoinRequestAlreadySubmited(Exception):
    u""" Member already requested to join """

class InvariantError(Invalid, UserError):
    u"""Exception class for invariants
    
    Used for signalling multiple widgets at the same time."""
    implements(IWidgetInputError)

    def __init__(self, msg, fields):
        self.msg = msg
        self.fields = set(fields)
        UserError.__init__(self, msg)

    def doc(self):
        return self.msg

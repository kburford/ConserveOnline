# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.interface import invariant
from zope.schema import ASCIILine
from zope.schema import Password
from zope.schema import TextLine
from zope.schema import Text
from zope.schema import Datetime

from Products.COL3.formlib.schema import RichText
from Products.COL3.formlib.schema import EmailField
from Products.COL3.formlib.schema import VocabularyChoice
from Products.COL3.formlib.schema import File
from Products.COL3.formlib.schema import CaptchaCondition
from Products.COL3.validators import validateLogin
from Products.COL3.validators import validatePassword
from Products.COL3.validators import validatePasswordConfirmationLogin
from Products.COL3.validators import validatePasswordChangePreferences
from Products.COL3 import config
from Products.COL3.formlib.schema import LicenseAgreementCondition
from Products.COL3.validators import validateImageFile
from Products.COL3.validators import validatePasswordReset
from Products.COL3.validators import validateUserID

class IUserBasePropertiesSchema(Interface):
    """ Base schema with fields common to other user schemas
    """
    fullname = TextLine(title=u'Full Name',
                        required=False,
                        readonly=True)
    
    firstname = TextLine( title=u'First name'
                        , required=True
                        )

    lastname = TextLine( title=u'Last name'
                       , required=True
                       )

    country = VocabularyChoice( title=u'Region/Country'
                              , default=config.NATIONS_DEFAULT
                              , required=True
                              , vocabulary=config.NATIONS
                              )

    organization = TextLine( title=u'Organization'
                           , required=False
                           )

    organizationtype = VocabularyChoice( title=u'Type of Organization'
                                       , description=u'Select your organization type.'
                                       , required=False
                                       , vocabulary=config.ORGANIZATIONS_TYPES
                                       , default=config.ORGANIZATIONS_TYPES_DEFAULT
                                       )

    background = VocabularyChoice( title=u'Your background'
                                 , required=False
                                 , vocabulary=config.PROFILE_BACKGROUNDS
                                 , default=config.PROFILE_BACKGROUNDS_DEFAULT
                                 )

    email = EmailField( title=u'Email address'
                      , description=u'Email address is required for login. We do not spam your email address.'
                      , required=True
                      )

class ISubscriptions(Interface):
    """ Interface to mark subscriptions folder """ 
    #XXX May not need this... XXX

class IUserExtraSchema(Interface):
    """Schema to use for hidden fields
    """
    join_date = Datetime( title=u'Join Date',
                              description=u'The date that the user became a member.',
                              required=False)

class IUserBiographySchema(Interface):
    """ Schema used for the biography form
    """

    description = Text( title=u'Biography'
                      , description=u'A short overview of who you are and what you do. Will be displayed on the your author page, linked from the items you create.'
                      , required=False
                      )

class IUserPropertiesSchema(IUserBasePropertiesSchema, 
                            IUserBiographySchema,
                            IUserExtraSchema):
    """ Schema used for the internal storage of the properties of a user
    """

class IUserPasswordChangeSchema(Interface):
    """ schema for changing the user password """

    old_password = Password( title=u'Password'
                           , description=u'To change your password, type your old password here..'
                           , required=True
                           , constraint=validatePassword
                           )

    password = Password( title=u'New Password'
                       , description=u'To change your password, type your new password here (letters and numbers only). Leave blank if you do not want to change your password.'
                       , required=True
                       , constraint=validatePassword
                       )

    confirmation = Password( title=u'Retype new password'
                           , required=True
                           , constraint=validatePassword
                           )

class IUserPasswordPrefChangeSchema(Interface):
    """ schema for changing the user password """

    old_password = Password( title=u'Password'
                           , description=u'To change your password, type your old password here..'
                           , required=False
                           , constraint=validatePassword
                           )

    password = Password( title=u'New Password'
                       , description=u'To change your password, type your new password here (letters and numbers only). Leave blank if you do not want to change your password.'
                       , required=False
                       , constraint=validatePassword
                       )

    confirm_password = Password( title=u'Retype new password'
                                 , required=False
                                 , constraint=validatePassword
                            )
    validatePasswordChangePreferences = invariant(validatePasswordChangePreferences)

class IUserPortraitSchema(Interface):
    """ Portrait for the user """
    portrait = File( title=u'Portrait'
                   , description=u'To add or change the portrait: click the "Browse" button; select a picture of yourself. Recommended image size is 75 pixels wide by 100 pixels tall.'
                   , required=False
                   , constraint=validateImageFile
                   )

class IEditBioSchema(Interface):
    """ Form schema for user to edit their biography"""
    description = RichText(title=u'Biography',
                           description=u'Enter the full text of your biography above.',
                           required=False,
                           )

class IUserPreferencesSchema(IUserBasePropertiesSchema,
                             IUserPasswordPrefChangeSchema,
                             IUserPortraitSchema,
                             IEditBioSchema):
    """ Schema for editing the user profile """
    
class IUserUsernamePasswordSchema(Interface):

    username = ASCIILine( title=u'Username'
                        , description=u'Usernames are case SENSITIVE so be careful with your choice.'
                        , required=True
                        , constraint=validateLogin
                        )

    password = Password( title=u'Password'
                       , description=u'Minimum 8 characters, needs to be different from the username.'
                       , required=True
                       , constraint=validatePassword
                       )

    confirm = Password( title=u'Re-enter the password'
                      , description=u'Make sure the passwords are identical.'
                      , required=True
                      )
    
    validatePasswordConfirmationLogin = invariant(validatePasswordConfirmationLogin)
    

class IUserRegistrationControlSchema(Interface):
    """ Fields that require ToU acceptance and captcha control """

    captcha = CaptchaCondition(title=u'Enter the verification code',
                               description=u'This prevents automated spam programs from completing the form.',
                               required=True)

    termsandconditions = LicenseAgreementCondition(title=u"Terms of Use",
                                                   description=u"Do you agree with the ConserveOnline Terms of Use?",
                                                   required=True)

class IUserRegistrationSchema(IUserBasePropertiesSchema,
                              IUserUsernamePasswordSchema,
                              IUserRegistrationControlSchema):
    """ Schema used for the user registration form
    """
    
class IPasswordResetSchema(Interface):

    username = ASCIILine( title=u'Username'
                        , description=u'Usernames are case SENSITIVE.'
                        , required=True
                        ,constraint=validateUserID
                        )

    password = Password( title=u'Password'
                       , description=u'Minimum 8 characters, needs to be different from the username.'
                       , required=True
                       , constraint=validatePassword
                       )

    confirm = Password( title=u'Re-enter the password'
                      , description=u'Make sure the passwords are identical.'
                      , required=True
                      , constraint=validatePassword
                      )
    
    validatePasswordReset = invariant(validatePasswordReset)

class IResetPasswordSchema(Interface):
    username = TextLine(title=u'Username',
                        required=True,
                        description=u'Usernames are case SENSITIVE.',)


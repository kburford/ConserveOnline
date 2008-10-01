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
from Products.COL3.interfaces.fields import IFile
"""Custom fields for COL3"""

import re

from zope import interface, schema
from zope.app.form.interfaces import IWidgetInputError
from DateTime.DateTime import DateTime
from Products.CMFDefault.formlib.schema import EmailLine

from Products.COL3.interfaces.formlib import IMappingSchemaField
from Products.COL3 import config

class ConditionNotSatisfiedError(schema.ValidationError):
    """The desired condition was not met"""

    def doc(self):
        return self.args[0]

    interface.implements(IWidgetInputError)

class SubdomainError(schema.ValidationError):
    """The domain must be all lowercase, start with a letter or digit and may contain dots or dashes."""

    interface.implements(IWidgetInputError)

class AlreadyExistsError(schema.ValidationError):
    """This domain already exists."""

    interface.implements(IWidgetInputError)

class SubdomainField(schema.BytesLine):

    # all letters should be lowercase
    # must start with a letter or digit
    # can contain hiphens and dots
    subdomain_re = re.compile(r'[a-z0-9]'
                              r'[a-z0-9.-]*'
                              r'$') # match EOS

    _marker = object()
    def _validate(self, value, _marker=_marker):
        super(SubdomainField, self)._validate(value)
        if not self.subdomain_re.match(value):
            raise SubdomainError()
        if self.context._getOb(value, _marker) is not _marker:
            raise AlreadyExistsError()

    def __init__(self, **kw):
        max_length = 25
        return super(SubdomainField, self).__init__(max_length=max_length,
                                                    **kw)

class VocabularyChoice(schema.Choice):
    """Choice variant for vocabularies shared between frontend and backend """

    def __init__(self, **kw):
        super(VocabularyChoice, self).__init__(**kw)
        assert isinstance(self.vocabulary.id, str)

class ChoiceSet(schema.Set):
    """ List of Choices, for automatic association with the XMLMultiCheckBox widget """

    def __init__(self, vocabulary=None, **kw):
        value_type = schema.Choice(__name__="choice", title=u"Choice",
                                   vocabulary=vocabulary)
        self.vocabulary = value_type.vocabulary
        max_length = len(self.vocabulary)
        super(ChoiceSet, self).__init__(value_type=value_type,
                                        max_length=max_length, **kw)

    def bind(self, context):
        """Rebind subfields"""
        clone = super(ChoiceSet, self).bind(context)
        clone.value_type = clone.value_type.bind(context)
        clone.vocabulary = clone.value_type.vocabulary
        return clone


class SelectionAndDescription(schema.Dict):
    """Dict field with keys from a Choice and the values are TextLines

    'values', 'vocabulary' and 'source' are fed to the Choice field to
    get a vocabulary, and 'min/max_length' to the TextLine field for the
    descriptions """

    def __init__(self, values=None, vocabulary=None, source=None,
                 min_length=0, max_length=None, **kw):
        key_type = schema.Choice(__name__="selection", title=u"Selection",
                                 values=values, vocabulary=vocabulary,
                                 source=source)
        value_type = schema.TextLine(__name__="description",
                                     title=u"Description",
                                     min_length=min_length,
                                     max_length=max_length)
        self.vocabulary = key_type.vocabulary
        selection_max_length = len(self.vocabulary)
        super(SelectionAndDescription,
              self).__init__(key_type=key_type, value_type=value_type,
                             max_length=selection_max_length, **kw)

    def bind(self, context):
        """Rebind subfields"""
        clone = super(SelectionAndDescription, self).bind(context)
        clone.key_type, clone.value_type = [field.bind(context) for field in
                                            (clone.key_type, clone.value_type)
                                           ]
        clone.vocabulary = clone.key_type.vocabulary
        return clone

EmailField = EmailLine 

class MemberSchema(interface.Interface):

    lastname = schema.TextLine(title=u"Last Name")

    firstname = schema.TextLine(title=u"First Name")

    email = EmailField(title=u"email", required=True)

class MemberRoster(schema.List):
    """Specialized field for listing members when creating a workgroup"""

    def __init__(self, **kw):
        value_type = MappingSchemaField(__name__='member',
                                        default=None,
                                        mapschema=MemberSchema)
        super(MemberRoster, self).__init__(value_type=value_type, default=[],
                                           **kw)

class Condition(schema.Bool):
    """Boolean field where the value must always be True"""

    def __init__(self, failure=u"Condition not satisfied", **kw):
        super(Condition, self).__init__(**kw)
        self.failure = failure

    def _validate(self, value):
        super(Condition, self)._validate(value)
        if not value:
            # condition must be true
            raise ConditionNotSatisfiedError(self.failure)

class LicenseAgreementCondition(Condition):
    """ Condition field for the license agreement widget """

    def __init__(self, **kw):
        __init__ = super(LicenseAgreementCondition, self).__init__
        __init__(failure=u'You must agree to the ConserveOnline notices and disclaimers.',
                 **kw)

class CaptchaCondition(Condition):
    """ Condition field for the captcha widget """

    def __init__(self, **kw):
        __init__ = super(CaptchaCondition, self).__init__
        __init__(failure=u'Incorrect verification code. Please re-enter.',
                 **kw)

class TextLinesTuple(schema.Tuple):
    """ Simple Tuple variant to be matched against the XMLLinesTuple widget """

    value_type = schema.TextLine

class TextLinesTupleRequiresOne(TextLinesTuple):
    """ Tuple of TextLines variant that requires at least one entry if the
    field is required"""

    _one_required_msg = u'Please, add at least one entry'

    def validate(self, value):
        super(TextLinesTuple, self).validate(value)
        if self.required and not value:
            raise ConditionNotSatisfiedError(self._one_required_msg)

class Labels(TextLinesTupleRequiresOne):
    """ Tuple of TextLines variant to be matched against the
    Labels widget """

    _one_required_msg = u'Please, enter at least one label'

class Authors(TextLinesTupleRequiresOne):
    """ Tuple of TextLines variant to be matched against the
    Authors widget """

    _one_required_msg = u'Please, enter at least one author'

class Keywords(TextLinesTupleRequiresOne):
    """ Tuple of TextLines variant to be matched against the
    Keywords widget """

    _one_required_msg = u'Please, enter at least one keyword'

class RichText(schema.Text):
    """ Simple text field variant to be matched by the Editor widget """

class ZDateTime(schema.Orderable, schema.Field):
    """field for Zope DateTime values. Useful for Archetype handling forms"""
    _type = DateTime

    def __init__(self, *args, **kw):
        super(ZDateTime, self).__init__(*args, **kw)

class ZDate(ZDateTime):
    """field for Zope DateTime values. Useful for Archetype handling forms
    This version is supposed to handle only Y-M-D, not hours and minutes"""

    def __init__(self, *args, **kw):
        super(ZDate, self).__init__(*args, **kw)

class File(schema.Field):
    """ Field for handling file(-like) objects """
    interface.implements(IFile)

    def constraint(self, value):
        return hasattr(value, 'read') and hasattr(value, 'seek')

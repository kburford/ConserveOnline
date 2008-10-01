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

from xml.parsers.expat import ExpatError
from Products.COL3.etree import Element, SubElement
from Products.COL3.etree import tostring, fromstring

from zope.interface import implements
from zope.app.form import browser as zwidgets
from zope.app.component.hooks import getSite
from zope.app.form.interfaces import ConversionError

from Products.COL3.interfaces.formlib import IXMLWidget
from Products.COL3.browser.common import cleanup
from Products.COL3.validators import _validateCaptchaValues
from Products.COL3.exceptions import CaptchaError
from Products.COL3 import config
import DateTime
from DateTime.DateTime import TimeError, DateError, DateTimeError

class XMLSimpleWidget(object):
    """ Mixin for simple XML widgets.

    With helper code for rendering ElemenTree nodes.
    """

    implements(IXMLWidget)

    hide = False

    def hidden(self):
        value_node = self.asElement()
        value_node.attrib['hidden'] = '1'
        return tostring(value_node)

    ##overriding a superclass call method to return my xml
    def __call__(self):
        elem = self.asElement()
        if elem is not None:
            return tostring(self.asElement())
        return ''

    def asElement(self):
        raise NotImplementedError('asElement')

class XMLFileUploadWidget(XMLSimpleWidget, zwidgets.widget.SimpleInputWidget):
    """ XML widget for file upload """

    xmltype = "file"

    def _toFieldValue(self, input):
        filename = getattr(input, 'filename', getattr(input, 'name', None))
        if not filename:
            # file was not uploaded
            return self.context.missing_value
        firstchar = input.read(1)
        input.seek(0)
        if not firstchar:
            return self.context.missing_value
        # it behaves like a file and has content,
        # that's all we need to know
        return input

    def asElement(self):
        return None

class XMLLabelsWidget(XMLSimpleWidget, zwidgets.widget.SimpleInputWidget):
    """ XML widget for file upload """

    xmltype = "labels"

    def cleanUpValues(self, input):
        return [u' '.join(entry.strip().split()) for entry in input
                if entry.strip()]

    def _toFieldValue(self, input):
        """See SimpleInputWidget"""
        if input is None:
            input = []
        elif not isinstance(input, list):
            input = [input]
        values = self.cleanUpValues(input)

        # All AbstractCollection fields have a `_type` attribute specifying
        # the type of collection. Use it to generate the correct type,
        # otherwise return a list.  TODO: this breaks encapsulation.
        if hasattr(self.context, '_type'):
            _type = self.context._type
            if isinstance(_type, tuple):
                _type = _type[0]
            return _type(values)
        else:
            return values

    def asElement(self):
        values = self._getFormValue()
        if not values:
            # don't return empty <value> tag
            return

        attrib = {'xml:space':'preserve'}
        value_node = Element('value', attrib=attrib)
        for value in values:
            SubElement(value_node, 'option').text = value
        return value_node

class XMLAuthorsWidget(XMLLabelsWidget):
    """Tuple of TextLines widget exactly like the Labels one. The difference
    is all in the frontend"""

    xmltype = "authors"

class XMLTextWidget(XMLSimpleWidget, zwidgets.TextWidget):
    """ XML version of TextWidget """

    xmltype = 'text'

    ##this produces the xml for a text widget
    def asElement(self):
        # next 3 lines taken from zope.app.form.browser.TextWidget.__call__
        value = self._getFormValue()
        if not value or value == self.context.missing_value:
            return None

        attrib = {'xml:space':'preserve'}
        value_node = Element('value', attrib=attrib)
        value_node.text = value
        return value_node

class XMLPasswordWidget(XMLTextWidget):
    """ XML version of TextWidget """

    xmltype = 'password'

    ##this produces the xml for a password widget
    def asElement(self):
        # the password widget is always empty
        return None

class XMLZDateTimeWidget(XMLTextWidget):
    """ XML widget for ZDateTime """

    xmltype = 'calendar'

    def _toFormValue(self, value):
        """Converts a field value to a string used as an HTML form value.

        returns something like '2007-03-20 00:00'
        """
        if value == self.context.missing_value:
            return self._missing
        else:
            return "%02d-%02d-%02d %02d:%02d" % value.parts()[:5]

    def _toFieldValue(self, input):
        # shamelessly stolen and adapted from zope.app.form.browser.DatetimeWidget
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                return DateTime.DateTime(input + ' ' + config.TIMEZONE)
            except (DateError, TimeError,
                    DateTimeError, DateTime.SyntaxError), v:
                raise ConversionError("Invalid datetime data", v)

class XMLZDateWidget(XMLZDateTimeWidget):
    """ XML Widget for ZDate, mostly like XMLZDateTimeWidget but only for
    Year/Month/Day """
    
    xmltype = 'ymdentry'

    def _toFormValue(self, value):
        """Converts a field value to a string used as an HTML form value.

        returns something like '2007-03-20'
        """
        if value == self.context.missing_value:
            return self._missing
        else:
            return "%02d-%02d-%02d %02d:%02d" % value.parts()[:5]


class XMLASCIIWidget(XMLSimpleWidget, zwidgets.ASCIIWidget):
    """ XML version of TextWidget """

    xmltype = 'text'

    # reuse the xmltextwidget implementation directly so as not to annoy Alan
    # with too much multiple inheritance :-)
    asElement = XMLTextWidget.asElement.im_func

class XMLCheckBoxWidget(XMLSimpleWidget, zwidgets.CheckBoxWidget):
    """ XML version of CheckboxWidget """

    xmltype = 'checkbox'

    # reuse the xmltextwidget implementation directly so as not to annoy Alan
    # with too much multiple inheritance :-)
    def asElement(self):
        value = self._getFormValue()
        if value != 'on':
            return None
        value_node = Element('value')
        value_node.text = value
        return value_node

class XMLCaptchaWidget(XMLSimpleWidget, zwidgets.widget.SimpleInputWidget):
    """A Captcha Widget
    """
    xmltype = 'captcha'
    _missing = None

    def asElement(self):
        """
        <value>
          <captcha href="getCaptchaImage/07080f0000040d07000a190a0c6f0c0206660f0000010e03"
                   hashkey="07080f0000040d07000a190a0c6f0c0206660f0000010e03" />
        </value>
        """
        portal = getSite()
        hashkey = portal.getCaptcha()
        href = portal.absolute_url() + '/getCaptchaImage/' + hashkey
        value_node = Element('value')
        SubElement(value_node, 'captcha',
                   hashkey=hashkey,
                   href=href)
        return value_node

    def hasInput(self):
        """Check whether the field is represented in the form."""
        return (self.name + ".hashkey" in self.request.form and
                self.name in self.request.form)

    def _getFormInput(self):
        """Returns Whether the captcha input entered is valid or not

        Return values:

          ``True``  Captcha key is valid
          ``False`` Captcha key is invalid
          ``None``  Captcha value was not provided

        """
        if not self.hasInput():
            return None
        key = self.request.form[self.name]
        hashkey = self.request.form[self.name + ".hashkey"]
        try:
            _validateCaptchaValues(key, hashkey)
        except CaptchaError:
            return False
        return True

class XMLTextAreaWidget(XMLSimpleWidget, zwidgets.TextAreaWidget):
    """ XML version of TextAreaWidget """

    xmltype = 'textarea'

    def asElement(self):
        # next 3 lines taken from zope.app.form.browser.TextWidget.__call__
        value = self._getFormValue()
        if not value or value == self.context.missing_value:
            return None

        attrib = {'xml:space':'preserve'}
        value_node = Element('value', attrib=attrib)
        value_node.text = self._getFormValue()
        return value_node

class XMLLinesTupleWidget(XMLTextAreaWidget):
    """Simple TextArea widget for getting input as collection in lines """
    # code shamelessly stolen from
    # Products.CMFDefault.formlib.widgets.TupleTextAreaWidget
    # cannot inherit from TupleTextAreaWidget because it has a stupid __init__
    # that doesn't match it's adapter signature
    # would rather inherit from XMLSimpleWidget and TupleTextAreaWidget
    # and copy XMLTextAreaWidget.asElement.im_func here
    def _toFieldValue(self, input):
        input = super(XMLLinesTupleWidget, self)._toFieldValue(input)
        if isinstance(input, basestring):
            input = tuple([ l.strip()
                            for l in input.splitlines() if l.strip() ])

        if input == ():
            return self.context.missing_value

        return input

    def _toFormValue(self, value):
        if value is not None:
            value = u'\n'.join(value)
        return super(XMLLinesTupleWidget, self)._toFormValue(value)

class XMLKeywordsWidget(XMLTextWidget):
    """Simple TextLine widget for getting input as comma separated list of
    words """
    def _toFieldValue(self, input):
        input = super(XMLKeywordsWidget, self)._toFieldValue(input)
        if isinstance(input, basestring):
            input = tuple([ ' '.join(word.strip().split())
                            for word in input.split(',') if word.strip() ])

        if input == ():
            return self.context.missing_value

        return input

    def _toFormValue(self, value):
        if value is not None:
            value = u', '.join(value)
        return super(XMLKeywordsWidget, self)._toFormValue(value)

class XMLEditorWidget(XMLSimpleWidget, zwidgets.TextAreaWidget):
    """ RichText Widget that triggers the rendering of a Rich Text editor """
    # otherwise identical to XMLTextWidget
    xmltype = 'editor'

    def _toFieldValue(self, value):
        value = super(XMLEditorWidget, self)._toFieldValue(value)
        clean_value = cleanup([value.strip()])
        if (clean_value.tag == '{http://www.w3.org/1999/xhtml}div' and
            len(clean_value) == 0 and
            not clean_value.text.strip()):
            # Rich-Editor sends at least an epty div, always
            return self.context.missing_value
        else:
            return unicode(tostring(clean_value, 'utf-8'), 'utf-8')

    def asElement(self):
        __traceback_info__ = (self.__class__,)
        attrib = {'xml:space':'preserve'}
        value_node = Element('value', attrib=attrib)
        formValue = self._getFormValue().strip()
        __traceback_info__ = (self.__class__, formValue)
        if formValue:
            if isinstance(formValue, unicode):
                formValue = formValue.encode(config.CHARSET)
            try:
                value_node.append(fromstring(formValue))
            except ExpatError:
                value_node.append(cleanup(formValue))
            return value_node
        # don't return empty node

class XMLSelectWidget(XMLSimpleWidget, zwidgets.SelectWidget):
    """ XML version of SelectWidget, with named vocabulary

    Assumes fields have a vocabulary attribute that has an 'id' attribute,
    for sharing the vocabulary between FE and BE """

    xmltype = 'selection'

    def __init__(self, field, request):
        zwidgets.SelectWidget.__init__(self, field, field.vocabulary, request)

    def asElement(self):
        value = self._getFormValue()
        vocabulary = self.context.vocabulary

        attrib = {'xml:space':'preserve',
                  'vocabulary':vocabulary.id}
        value_node = Element('value', attrib=attrib)
        # the code below was adapted from
        # ItemsEditWidget.renderItemsWithValues
        if value != self._missing:
            value_node.text = value

        return value_node


class XMLRadioWidget(XMLSimpleWidget, zwidgets.RadioWidget):
    """ XML version of RadioWidget.

    Assumes fields have a vocabulary attribute """

    xmltype = 'radiogroup'

    _displayItemForMissingValue = False

    def __init__(self, field, request):
        zwidgets.RadioWidget.__init__(self, field, field.vocabulary, request)

    def asElement(self):
        value = self._getFormValue()
        missing = self._toFormValue(self.context.missing_value)

        value_node = Element('value')
        # the code below was adapted from
        # ItemsEditWidget.renderItemsWithValues
        if self._displayItemForMissingValue and not self.context.required:
            missing_option_node = SubElement(value_node, 'option', value=missing)
            missing_option_node.text = self.translate(self._messageNoValue)
            if missing == value:
                missing_option_node.attrib['selected']='selected'

        # Render normal values
        for term in self.vocabulary:
            option_node = SubElement(value_node, 'option', value = term.token)
            option_node.text = self.textForValue(term)
            if term.value == value:
                option_node.attrib['selected'] = 'selected'

        return value_node

class XMLMultiCheckBoxWidget(XMLSimpleWidget, zwidgets.MultiCheckBoxWidget):
    """ XML version of MultiCheckBoxWidget.

    Assumes fields have a vocabulary attribute, usually taken from its
    value_type
    """

    xmltype = 'checkboxgroup'

    def __init__(self, field, request):
        super(XMLMultiCheckBoxWidget, self).__init__(field, field.vocabulary,
                                                     request)

    def asElement(self):
        vocabulary = self.context.vocabulary
        values = self._getFormValue()
        tokens = sorted(vocabulary.getTerm(entry).token for entry in values)

        # we expect the vocabulary to have an "id" attribute that comes from
        # the xml tag it came from

        value_node = Element('value', vocabulary=vocabulary.id)
        for token in tokens:
            SubElement(value_node, 'selected', id=token)
        return value_node

class XMLSubdomainWidget(XMLSimpleWidget, zwidgets.ASCIIWidget):
    """ Widget for the domain input in WG creation wizard, step 1
    Mostly an ASCIIWidget, but registered to adapt the subdomain field """

    xmltype = "text"
    # reuse the xmltextwidget implementation directly so as not to annoy Alan
    # with too much multiple inheritance :-)
    asElement = XMLTextWidget.asElement.im_func

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

import zope.i18n

from Products.COL3.etree import Element, SubElement, tostring
from zope.formlib.form import FormBase, action, setUpWidgets

from Acquisition import aq_inner
from Products.Five.browser.decode import processInputs
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.base import Fragment
from Products.COL3.exceptions import InvariantError

# action validator that does no validation
def NO_VALIDATION(form, action, data): #@UnusedVariable
    return ()

class FormFragment(Fragment, FormBase):
    """ Base class for XML forms
    Action handlers MUST return ElementTrees or raise exceptions """

    # actionURL = '.'
    def actionURL(self):
        request = self.request
        qstring = request.get("QUERY_STRING", '')
        if qstring:
            qstring = '?' + qstring
        return request['URL'] + qstring

    # template = pagetemplatefile.ViewPageTemplateFile('form.xml')
    #_template_as_element = None
    form_result_as_element = None
    description = None

    def template(self):
        # FormBase calls template() and expects a string back. We
        # generate a element to be used by asElement() and store that,
        # and then return the string to please the render() method.
        # Note that the update() method is not called here. 
        # We expect that update() is called before template().
        return tostring(self.formAsElement())

    def asElement(self):
        # Call update to setup the widgets and handle
        # any form values in the request. 
        self.update()
        return self.renderAsElement()

    def update(self):
        processInputs(self.request)
        super(FormFragment, self).update()
        if (self.form_result is not None): # and 
            #self.form_result_as_element is None):
            # this result is expected to be an etree coming from the
            # handlers. Switch it with the string version for formlib
            # compatibility
            self.form_result_as_element = self.form_result
            self.form_result = tostring(self.form_result)

    def _checkMissingRequiredInput(self):
        # as a security precaution, if we're running the default validation
        # the required fields MUST contain input so their validation can kick
        # in.
        # The input can be the missing value for the widget, in which case
        # the normal validation will complain, but it must be there.
        missing = set(widget.context.__name__
                      for widget in self.widgets
                      if (widget.required and
                          widget.visible and
                          not widget.hasInput()))
        assert not missing, ("Missing required input: %s" %
                             ", ".join(missing))

    def validate(self, action, data):
        errors = super(FormFragment, self).validate(action, data)
        # plug "missing input" security error
        self._checkMissingRequiredInput()
        # wait for invariant errors and set them on each respective widget
        for error in errors:
            if isinstance(error, InvariantError):
                for fieldname in error.fields:
                    self.widgets[fieldname]._error = error
        return errors

    def renderAsElement(self):
        # NOTE: mirrors FormBase.render()
        # if the form has been updated, it will already have a result
        if self.form_result is None:
            if self.form_reset:
                # we reset, in case data has changed in a way that
                # causes the widgets to have different data
                self.resetForm()
                self.form_reset = False
            # here we fork from Formbase.render()
            self.form_result_as_element = self.formAsElement()
            # we store the string as the result to comply with formlib but
            # keep the elementtree for our own consuption
            self.form_result = tostring(self.form_result_as_element)

        return self.form_result_as_element

    def formAsElement(self):
        #if self._template_as_element is not None:
        #    return self._template_as_element
        
        fc = Element('formcontroller', action=self.actionURL())

        status = self.status
        if status:
            error = SubElement(fc, 'error')
            error.text = status

        for widget in self.widgets:
            field = SubElement(fc, 'field', name=widget.name,
                               widget=widget.xmltype)
            if widget.required:
                field.attrib['required'] = 'required'

            label = SubElement(field, 'label')
            label.text = widget.label
            
            if widget.hint:
                description = SubElement(field, 'description')
                description.text = widget.hint

            value_node = widget.asElement()
            if value_node is not None:
                field.append(value_node)
            
            err = widget.error()
            if err:
                error = SubElement(field, 'error')
                error.text = err
        
        for ai in self.availableActionsInfo():
            action = SubElement(fc, 'submit', name=ai['name'])
            action.text = ai['label']
        # XXX Leo thinks this is dangerous. It could mask errors when rendering
        # the form again on purpose after manually setting errors during an
        # action handler
        #self._template_as_element = fc
        return fc

    def availableActionsInfo(self):
        return [
            dict(name=action.__name__,
                 label=zope.i18n.translate(action.label, context=self.request))
            for action in self.actions
            if action.available()
        ]

class AddFormFragment(FormFragment):

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        # create an empty object for validation purposes
        form_context = self.createEmptyObject()
        initial_defaults = self.provideInitialDefaults()
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, form_context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request,
            data=initial_defaults)

    def createEmptyObject(self):
        """Create an empty instance of the object for validation purposes.
        For Zope2 objects, these should probably be in the context of the
        container (i.e., you should return the result of calling .__of__ on 
        them passing the container (self.context).

        If you're lazy, just return self.context and pray the validators work
        anyway
        """
        return

    def provideInitialDefaults(self):
        """ Provide initial values for the form. Return a dictionary
        with the values you want to provide a default for. Don't bother
        with the other values """
        return {}

    def createAddAndReturnURL(self, data):
        """Create an instance of the object with the provided data and add it
        to the current container (self.context). Returns the URL to redirect to
        after creating the object.""" 
        raise NotImplementedError()

    def cancelURL(self):
        """Returns the URL to redirect to in case the user has given up
        creating the object."""
        raise NotImplementedError()

    @action("Save", name="add")
    def handle_add(self, action, data): #@UnusedVariable
        url = self.createAddAndReturnURL(data)
        raise SafeRedirect(url)

    @action("Cancel", name="cancel", validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())

class ResetPasswordFormFragment(AddFormFragment):
    @action("Reset", name="add")
    def handle_add(self, action, data):
        url = self.createAddAndReturnURL(data)
        raise SafeRedirect(url)
    
    @action("Cancel", name="cancel", validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())

class EditFormFragment(FormFragment):

    def setUpWidgets(self, ignore_request=False):
        """ override of form.FormBase.setUpWidgets()

        so that we can restore info from the context """
        data = self.getDataFromContext()
        context = aq_inner(self.context)
        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, context, self.request,
            data=data,
            form=self, adapters=self.adapters, ignore_request=ignore_request)

    def getDataFromContext(self):
        """Return a dictionary with data for this form. Keys are the form fields
        and values are the context values"""
        raise NotImplementedError()

    def applyChangesAndReturnURL(self, data):
        """Create an instance of the object with the provided data and add it
        to the current container (self.context). Returns the URL to redirect to
        after creating the object.""" 
        raise NotImplementedError()

    def cancelURL(self):
        """Returns the URL to redirect to in case the user has given up
        editing the object."""
        raise NotImplementedError()

    @action("Save", name="save")
    def handle_apply(self, action, data): #@UnusedVariable
        url = self.applyChangesAndReturnURL(data)
        raise SafeRedirect(url)

    @action("Cancel", name="cancel", validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())


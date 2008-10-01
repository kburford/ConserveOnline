# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id$

from zope.app.form.browser.interfaces import IWidget
from zope.interface import Attribute

from Products.COL3.interfaces.user import IUserPasswordChangeSchema
from Products.COL3.interfaces.user import IUserPreferencesSchema
from Products.COL3.interfaces.user import IUserRegistrationSchema
from Products.COL3.interfaces.tools import IInvitationManager
from Products.COL3.interfaces.tools import IJoinRequestsManager
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement

class IXMLWidgetType(IWidget):
    """ Mixin interface for XML widgets providing an xml widget type """

    widget_type = Attribute("Type of the XML widget, sent to the front-end")

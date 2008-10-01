# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id$

from zope.app.form.browser.interfaces import IInputWidget, IBrowserWidget
from zope import schema, interface

class IXMLWidget(IInputWidget, IBrowserWidget):
    """  """

    xmltype = schema.BytesLine(title=u"XML widget type",
                               description=u"type of this xml widget, to be matched to the proper field template by XSLT",
                               required=True)

class IMappingSchemaField(schema.interfaces.IField):
    u"""Field containing a mapping from schema field names to their values."""

    _type = interface.Attribute("_type",
        u'The type of the mapping, usually dict.')

    mapschema = interface.Attribute("mapschema",
        u"The Interface that defines the Fields comprising the mapping.")

    fields = schema.List(title=u"list of tuples: (field name, schema field)",
                         value_type=schema.Tuple(min_length=2, max_length=2))

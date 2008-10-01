# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.schema import TextLine, Choice

from Products.COL3.formlib.schema import RichText
from Products.COL3.formlib.schema import ChoiceSet
from Products.COL3.formlib.schema import Labels
from Products.COL3 import config

class IPageSchema(Interface):
    """ Schema for the Add/Edit views of a page """

    title = TextLine(title=u'Title',
                     required=True)

    text = RichText(title=u'Content',
                    required=True)

    labels = Labels(title=u'Keywords',
                    required=True)

    document_type = ChoiceSet(title=u'Purpose',
                              vocabulary=config.DOCUMENT_TYPE_VOCABULARY,
                              required=False,
                              description=u'Describes the purpose of the document, if applicable.')

    is_private = Choice(title=u'Private?',
                        vocabulary=config.CONTENT_ISPRIVATE_OPTIONS,
                        default=config.CONTENT_ISPRIVATE_DEFAULT)

class IPage(Interface):
    """Marker interface for page objects, to hang views off of"""

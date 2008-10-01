# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.schema import TextLine
from Products.COL3.formlib.schema import RichText

class ITopicSchema(Interface):
    """ Form schema for creating and editing discussion board topics """

    title = TextLine(title=u'Title',
                     required=True)

    description = RichText(title=u'Content',
                           description=u'Enter the full text of your entry above',)

class ICommentSchema(Interface):
    """ Form schema for creating and editing comments on a topic"""

    title = TextLine(title=u'Title',
                    required=True)

    text = RichText(title=u'Reply',
                    description=u'Enter the full text of your entry above',)

class IViewTopicCommentSchema(Interface):
    """ Form schema for creating and editing comments on a topic view page"""
    
    text = RichText(title=u'Reply',
                    description=u'Enter the full text of your entry above',)
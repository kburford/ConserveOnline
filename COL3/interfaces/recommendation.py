# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.schema import Text
from zope.schema import TextLine, Choice

from Products.COL3 import config
from Products.COL3.formlib.schema import RichText


class IUserRecommendationSchema(Interface):
    """ Schema for the Add/Edit views of an user recommendation """

    rating = Choice(title=u'How Do You Rate This Item?',
                    vocabulary=config.RATING_OPTIONS,
                    required=True,
                    default=0)

    title = TextLine(title=u'Title of Your Recommendation',
                     default=u'',
                     required=False)

    text = Text(title=u'Your Comments',
                default=u'',
                max_length=1000,
                required=False)

    flagged = Choice(title=u'Flagged?',
                     vocabulary=config.RATING_FLAGGED_OPTIONS,
                     default=config.RATING_FLAGGED_DEFAULT,
                     required=False)


class IRecommendationReportSchema(Interface):
    """ Schema for the report a recommendation as inappropriate """

    text = Text(title=u'Why Do You Believe These Rating Comments Are Inappropriate?',
                max_length=250,
                required=True)


class IRecommendation(Interface):
    """Marker interface for recommendable objects"""

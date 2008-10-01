from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import directlyProvides
from zope.interface.interfaces import IInterface
from zope.annotation.interfaces import IAnnotatable

from zope.schema import Bool
from zope.schema import Text
from zope.schema import ASCII
from zope.schema import Datetime
from zope.schema import TextLine

from contentratings.interfaces import IRatingType
from contentratings.interfaces import IUserRating


class IRecommendationRatable(IAnnotatable):
    """Marker interface that promises that an implementing object may be
    rated by a recommendation using the IRecommendationRating interface.
    """


class IRating(Interface):
    """An object representing a user rating, the rating attributes
    are immutable.  The object itself should be a Float, though there
    is no IFloat to be inherited from other than the schema field."""

    userid = ASCII(
        title=u"User Id",
        description=u"The id of the user who set the rating",
        required=False,
        readonly=True,
        )

    timestamp = Datetime(
        title=u"Time Stamp",
        description=u"The date and time the rating was made (UTC)",
        required=True,
        readonly=True
        )

    rating_title = TextLine(
        title=u"Rating Title",
        description=u"The title of the user recommendation.",
        default=u'',
        required=False,
        )

    rating_text = Text(
        title=u"Rating Comment",
        description=u"The text of the user recommendation.",
        default=u'',
        required=False,
        )

    flagged = Bool(
        title=u"Flagged?",
        description=u"Mark this option if this rating is inappropriate.",
        default=False,
        required=False,
        )


    badcontent = Bool(
        title=u"Bad content?",
        description=u"Mark this option if this rating has bad content.",
        default=False,
        required=False,
        )


class IRecommendationRating(IUserRating):
    """A rating class that allows users to set and adjust their ratings
    of content.
    """

    def rate(rating, username, title='', text='',
             flaggged=False, badcontent=False):
        """Rate the current object with `rating` by the `username`.

        Optionally, the rating may contain a title and/or a text.
        It may also be `flagged` by another user or contain `badcontent`.

        Returns the created IRating object.
        """

directlyProvides(IRecommendationRating, IRatingType)

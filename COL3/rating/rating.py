from datetime import datetime
from zope.interface import implements
from contentratings.rating import Rating
from Products.COL3.rating.interfaces import IRating


class RecommendationRating(Rating):
    """Behaves like a float with some extra attributes"""
    implements(IRating)

    # No security on this
    __allow_access_to_unprotected_subobjects__ = True

    def __init__(self, rating, userid, rating_title='',
                 rating_text='', flagged=False, badcontent=False):
        self._rating = float(rating)
        self.userid = userid
        self.timestamp = datetime.utcnow()
        self.rating_title = rating_title
        self.rating_text = rating_text
        self.flagged = flagged
        self.badcontent = badcontent

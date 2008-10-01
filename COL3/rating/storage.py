from zope.interface import implements
from contentratings.storage import UserRatingStorage
from contentratings.interfaces import IRatingStorage
from Products.COL3.rating.rating import RecommendationRating
from Products.COL3.rating.interfaces import IRecommendationRating


class RecommendationRatingStorage(UserRatingStorage):
    """BTree-based storage for user ratings, keeps a running
    statistics tally for efficiency."""
    implements(IRecommendationRating, IRatingStorage)

    _badcontent = 0

    def rate(self, rating, username, title='', text='',
             flagged=False, badcontent=False):
        """Set a rating for a particular user."""
        # We keep a running average for efficiency, we need to
        # have the current statistics to do so
        orig_total = self._average * self.numberOfRatings
        orig_rating = self._ratings.get(username,
                                        RecommendationRating(0.0, username))
        rating = RecommendationRating(rating, username, title, text,
                                      flagged, badcontent)
        self._ratings[username] = rating
        if orig_rating.badcontent and not badcontent:
            self._badcontent -= 1
            self._average = (orig_total + rating)/self.numberOfRatings
        if not orig_rating.badcontent and badcontent:
            self._badcontent += 1
            self._average = float(self.numberOfRatings and
                                  (orig_total - orig_rating)/self.numberOfRatings)
        if not orig_rating.badcontent and not badcontent:
            self._average = (orig_total + rating - orig_rating)/self.numberOfRatings
        # Mark this new rating as the most recent
        self._most_recent = rating
        return rating

    @property
    def numberOfRatings(self):
        return len(self._ratings) - self._badcontent

    def remove_rating(self, username):
        """Remove the rating for a given user"""
        orig_total = self._average * self.numberOfRatings
        rating = self._ratings[username]
        del self._ratings[username]
        # Since we want to keep track of the most recent rating, we
        # need to replace it with the second most recent if the most
        # recent was deleted
        if rating is self.most_recent:
            ordered = sorted(self.all_user_ratings(True),
                             key=lambda x: x.timestamp)
            if ordered:
                self._most_recent = ordered[-1]
            else:
                self._most_recent = None
        # Update the average
        if rating.badcontent:
            self._badcontent -= 1
        else:
            self._average = float(self.numberOfRatings and
                                  (orig_total - rating)/self.numberOfRatings)

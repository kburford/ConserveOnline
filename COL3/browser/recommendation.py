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

from zope.formlib import form
from zope.formlib.form import action
from Acquisition import aq_inner, aq_parent

from Products.CMFCore.utils import getToolByName

from contentratings.interfaces import IUserRating
from Products.COL3.etree import Element
from Products.COL3.browser.base import Page
from Products.COL3.browser.base import Fragment
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.formlib.xmlform import NO_VALIDATION
from Products.COL3.formlib.xmlform import AddFormFragment
from Products.COL3.formlib.xmlform import EditFormFragment
from Products.COL3.Extensions.content_filter import has_bad_word
from Products.COL3.interfaces.recommendation import IUserRecommendationSchema
from Products.COL3.interfaces.recommendation import IRecommendationReportSchema


class RecommendationViewFragment(Fragment):

    def asElement(self):
        return Element('view',
                       name='recommendation.html',
                       type='recommendation',
                       title='Add A Rating: '+self.context.Title(),
                       section='library')


class RecommendationForm(EditFormFragment):

    form_fields = form.FormFields(IUserRecommendationSchema)

    def getDataFromContext(self):
        defaults = {}
        context = aq_inner(self.context)
        tool = getToolByName(context, 'portal_membership')
        username = self.request.get('username')
        if username:
            member = tool.getMemberById(username)
        else:
            member = tool.getAuthenticatedMember()
        recommendation = IUserRating(context)
        rating = recommendation.userRating(member.getId())
        if rating is not None:
            defaults['title'] = rating.rating_title
            defaults['text'] = rating.rating_text
            defaults['rating'] = int(rating)
            defaults['flagged'] = rating.flagged
        return defaults

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        tool = getToolByName(context, 'portal_membership')
        username = self.request.get('username')
        if username:
            member = tool.getMemberById(username)
        else:
            member = tool.getAuthenticatedMember()
        if has_bad_word(data['text'] + ' ' + data['title']):
            data['badcontent'] = True
        recommendation = IUserRating(context)
        rating = recommendation.rate(username=member.getId(), **data)
        if rating.badcontent:
            info = {
                'author': rating.userid,
                'timestamp': rating.timestamp,
                'content': context.Title(),
                'title': rating.rating_title,
                'url': context.absolute_url()+'/recommendation.html?username='+rating.userid,
                'comment': rating.rating_text,
            }
            smt = simple_mail_tool()
            smt.sendRecommendationBadContentEmail(context, info)
        return context.absolute_url()+'/view.html'

    def cancelURL(self):
        return self.context.absolute_url()+'/view.html'

    @action('Submit', name='apply')
    def handle_apply(self, action, data):
        url = self.applyChangesAndReturnURL(data)
        raise SafeRedirect(url)

    @form.action('Cancel', name='cancel', validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())


class RecommendationPage(Page):
    views = (RecommendationViewFragment,
             RecommendationForm,) + COMMON_VIEWS


class RecommendationReportFragment(Fragment):

    def asElement(self):
        return Element('view',
                       name='report-recommendation.html',
                       type='recommendation',
                       title='Report: ' + self.context.Title(),
                       section='library')


class RecommendationReportForm(AddFormFragment):

    form_fields = form.FormFields(IRecommendationReportSchema)

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)
        author = self.request.get('username')
        tool = getToolByName(context, 'portal_membership')
        member = tool.getAuthenticatedMember()
        mfrom = member.getProperty('email')
        recommendation = IUserRating(context)
        rating = recommendation.userRating(author)
        info = {
            'author': author,
            'timestamp': rating.timestamp,
            'title': context.Title(),
            'url': context.absolute_url()+'/recommendation.html?username='+author,
            'username': member.getId(),
            'comment': data['text'],
        }
        rating.flagged = True
        smt = simple_mail_tool()
        smt.sendRecommendationReportEmail(context, mfrom, info)
        return self.cancelURL()

    def cancelURL(self):
        return self.context.absolute_url()+'/view-recommendations.html'

    @action('Submit', name='add')
    def handle_add(self, action, data):
        url = self.createAddAndReturnURL(data)
        raise SafeRedirect(url)

    @form.action('Cancel', name='cancel', validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())


class RecommendationReportPage(Page):
    views = (RecommendationReportFragment,
             RecommendationReportForm,) + COMMON_VIEWS


class RecommendationDeleteView(Fragment):

    def asElement(self):
        context = aq_inner(self.context)
        if self.request.get('confirm', None) is not None:
            # user has confirmed deletion
            # so delete the recommendation
            tool = getToolByName(context, 'portal_membership')
            member = tool.getAuthenticatedMember()
            recommendation = IUserRating(context)
            recommendation.remove_rating(member.getId())
            raise SafeRedirect(context.absolute_url()+'/view.html')
        # user hasen't confirmed yet, show confirmation view
        return Element('view',
                       name="delete-recommendation.html",
                       type="recommendation",
                       title="Delete Recommendation",
                       section="library")


class RecommendationDeletePage(Page):
    views = (RecommendationDeleteView,) + COMMON_VIEWS

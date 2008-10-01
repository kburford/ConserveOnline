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

from Acquisition import aq_chain
from xml.parsers.expat import ExpatError
from Products.COL3.etree import Element, SubElement

from zope.formlib import form
from Acquisition import aq_inner
from zExceptions.unauthorized import Unauthorized

from Products.CMFCore import utils as cmfutils
from Products.COL3.content.indexer import index as gsa_index
from Products.COL3.content.indexer import reindex as gsa_reindex
from Products.COL3.content.indexer import unindex as gsa_unindex

from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.base import createViewNode
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.browser.batch import BatchProvider
from Products.COL3.browser.batch import BatchFragmentFactory

from Products.COL3.formlib.xmlform import AddFormFragment, EditFormFragment
from Products.COL3.interfaces.discussion import ITopicSchema, ICommentSchema
from Products.COL3.interfaces.discussion import IViewTopicCommentSchema
from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.interfaces.workspace import IWorkspaceMemberManagement
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.common import cleanup
from Products.COL3.etree import fromstring
from Products.CMFCore.utils import getToolByName

class CommentViewFragment(Fragment):
    """ <view name="view.html" type="comment" title="View Comment" section="workspaces"/> """
    def asElement(self):
        viewattribs = {'name':'view.html',
                       'type':'comment',
                       'title':self.context.Title(),
                       'section':'workspaces'}
        return createViewNode(viewattribs)

class CommentViewMenu(Fragment):
    # there should be a way to automatically eliminate this view if the user
    # doesn't have permissions

    _actionmenu_entries = (# title, relative-url
                           (u'Edit', "@@edit-comment.html"),
                           )

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('actionmenu')
        for label, relative_url in self._actionmenu_entries:
            try:
                context.restrictedTraverse(relative_url)
            except Unauthorized:
                pass
            else:
                SubElement(actionmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label

        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        if menu_tag:
            # do not return empty elements
            return menu_tag

class CommentViewPage(Page):
    views = (CommentViewFragment, CommentViewMenu,) + COMMON_VIEWS

class ViewTopicBatchProvider(BatchProvider):
    """ Batch provider to return discussions from a workspace """
    def query(self, params):
        items = []
        context = self.context
        portal = getToolByName(aq_inner(self.context), 'portal_url').getPortalObject()
        #comments = context.getComments(limit=5000, offset=0)
        comments = context.getComments(limit=params['end']-params['start']+1,
                                       offset=params['start'])
        for comment in comments:
            try:
                commenttext = fromstring(comment.text())
            except:
                # hack: some discussion comments are stored as plain text and can't be parsed by fromstring()
                commenttext = fromstring("<div>"+comment.text()+"</div>")
            textelem = Element('text')
            textelem.append(commenttext)
            creator = comment.Creator()
            items.append({'href' : '%s/%s' % (context.absolute_url(), comment.id),
                          'title':comment.title,
                          'text': textelem,
                          'author':creator,
                          'authorhref':portal.absolute_url()+'/view-profile.html?userid='+creator,
                          'modified': comment.modified().ISO8601(),
                          })
        return items

class ViewBatchFragment(Fragment):
    def asElement(self):
        context = self.context
        request = self.request
        batchfragment = BatchFragmentFactory(ViewTopicBatchProvider,
                                             letters_param='REMOVE',
                                             columns={}, )
        batch = batchfragment(context, request)
        return batch.asElement()

class CommentAddForm(AddFormFragment):

    form_fields = form.FormFields(IViewTopicCommentSchema)

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)
        pm = cmfutils.getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            creator = 'Anonymous'
        else:
            creator = pm.getAuthenticatedMember().getUserName()

        comment = context.addComment(None,
                                     data['text'],
                                     creator=creator,
                                     files=None)
        # XXX status message
        gsa_index(comment)
        return context.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class TopicViewFragment(Fragment):
    """ <view name="view.html" type="topic" title="<topic title>" section="workspaces"/> """
    def asElement(self):
        return Element('view',
                       name='view.html',
                       type='topic',
                       title=self.context.title_or_id(),
                       section='workspaces')

class TopicQuotedText(Fragment):
    def asElement(self):
        request = self.request
        context = self.context
        quoted = request.get('quoted', '')
        if quoted:
            reply = context.getComment(quoted)
            if reply:
                root = Element('quoted_reply')
                SubElement(root, 'author').text = reply.Creator()
                replytext = reply.getText()
                try:
                    replytext = fromstring(replytext)
                except ExpatError:
                    replytext = cleanup(replytext)
                SubElement(root, 'text').append(replytext)
                return root

class TopicViewMenu(Fragment):
    # there should be a way to automatically eliminate this view if the user
    # doesn't have permissions

    _actionmenu_entries = (# title, relative-url
                           (u'Edit', "@@edit.html"),
                           (u'Delete', "@@delete.html"),
                           )

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('actionmenu')
        for label, relative_url in self._actionmenu_entries:
            try:
                context.restrictedTraverse(relative_url)
            except Unauthorized:
                pass
            else:
                SubElement(actionmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label

        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        if menu_tag:
            # do not return empty elements
            return menu_tag

class TopicViewPage(Page):
    views = (TopicViewFragment,
             TopicQuotedText,
             ViewBatchFragment,
             TopicViewMenu) + COMMON_VIEWS

    def getResponse(self):
        """ Overriding to set some variables"""
        _workspace = None
        context = self.context
        request = self.request
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getAuthenticatedMember()
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                _workspace = ob
        if not pmem.isAnonymousUser():
            self.views = self.views+(CommentAddForm,)
        return super(TopicViewPage, self).getResponse()

class ViewTopicsViewFragment(Fragment):
    """<view name="view.html" type="topics" title="Discussions" section="workspaces"/>"""
    def asElement(self):
        return Element('view',
                       name='view.html',
                       type='topics',
                       title='Discussions',
                       section='workspaces')


class DiscussionBatchProvider(BatchProvider):
    """ Batch provider to return discussions from a workspace """
    def query(self, params):
        items = []
        context = self.context
        pcat = cmfutils.getToolByName(context, 'portal_catalog')
        query = '/'.join(context.getPhysicalPath())
        topics = pcat.searchResults(path = {'query': query,'depth':1}, sort_on='sortable_title')
        for topic in topics: #[params['start']:params['end']]:
            replycreated = ''
            replyauthor = ''
            replies = pcat.searchResults(path = {'query': topic.getPath(),'depth':1},
                                         sort_on='created',
                                         sort_order='reverse')
            if len(replies) > 0:
                replycreated = replies[0].created.ISO8601()
                replyauthor = replies[0].Creator
            else:
                replycreated = context.created().ISO8601()
                replyauthor = context.Creator()
            items.append({'href':topic.getURL(),
                          'title':topic.Title,
                          'author':topic.Creator,
                          'replies':len(replies),
                          'lastcomment':{'children':{'created':replycreated,
                                                     'author':replyauthor},}
                          })
        return items

class DiscussionBatchFragment(Fragment):
    def asElement(self):
        context = self.context
        request = self.request
        batchfragment = BatchFragmentFactory(DiscussionBatchProvider,
                                             letters_param='REMOVE',
                                             columns={}, )
        batch = batchfragment(context, request)
        return batch.asElement()

class DiscussionsMostPopular(Fragment):
   """A Fragment Containing the five most popular discussions
      based on the total replies in a discussion"""
   def asElement(self):
        items = []
        context = self.context
        pcat = cmfutils.getToolByName(context, 'portal_catalog')
        query = '/'.join(context.getPhysicalPath())
        topics = pcat.searchResults(path = {'query': query,'depth':1})
        if len(topics) > 0:
            for topic in topics:
                replycreated = ''
                replyauthor = ''
                replies = pcat.searchResults(path = {'query': topic.getPath(),'depth':1},
                                             sort_on='created',
                                             sort_order='desc')
                if len(replies) > 0:
                    replycreated = replies[0].created.ISO8601()
                    replyauthor = replies[0].Creator
                else:
                    replycreated = context.created().ISO8601()
                    replyauthor = context.Creator()
                items.append({'href':topic.getURL(),
                              'title':topic.Title,
                              'author':topic.Creator,
                              'replies':len(replies),
                              'lastcomment':{'children':{'created':replycreated,
                                                         'author':replyauthor},}
                              })
                items.sort(lambda a, b: cmp(a.get('replies'), b.get('replies')))
                items.reverse()

            root = Element('mostpopular')
            for item in items[:5]:
                topicelem = SubElement(root, 'topic')
                topicelem.attrib['href'] = item['href']
                elem = SubElement(topicelem, 'title')
                elem.text = item['title']
                elem = SubElement(topicelem, 'author')
                elem.text = item['author']
                elem.attrib['href'] = '/profile/%s' % item['author']
                elem = SubElement(topicelem, 'replies')
                elem.text = str(item['replies'])
                lastcommentelem = SubElement(topicelem, 'lastcomment')
                elem = SubElement(lastcommentelem, 'created')
                lastcomment = item['lastcomment']['children']
                elem.text = lastcomment['created']
                elem = SubElement(lastcommentelem, 'author')
                elem.text = lastcomment['author']
                elem.attrib['href'] = '/profile/%s' % lastcomment['author']
            return root

class ViewTopicsDiscussionFragment(Fragment):
    """ Most Popular topics and topics batch """
    def asElement(self):
        context = self.context
        request = self.request
        root = Element('discussion')
        views = (DiscussionsMostPopular, DiscussionBatchFragment, )
        for view in views:
            element = view(context, request).asElement()
            if element is not None:
                root.append(element)
        return root

class TopicsViewMenu(Fragment):
    # there should be a way to automatically eliminate this view if the user
    # doesn't have permissions (added my simplistic way, BJS 10/17/07)

    """ Menu fragment for topic list view """
    _actionmenu_entries = ((u'Add Discussion', "@@add-topic.html"),)

    def asElement(self):
        context = aq_inner(self.context)
        url = context.absolute_url()
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        actionmenu_tag = Element('actionmenu')
        for label, relative_url in self._actionmenu_entries:
            try:
                context.restrictedTraverse(relative_url)
            except Unauthorized:
                pass
            else:
                SubElement(actionmenu_tag, 'entry',
                           href=url + "/" + relative_url).text = label

        if actionmenu_tag:
            # do not append if empty
            menu_tag.append(actionmenu_tag)
        if menu_tag:
            # do not return empty elements
            return menu_tag

class ViewTopicsViewPage(Page):
    views = (TopicsViewMenu,
             ViewTopicsViewFragment,
             ViewTopicsDiscussionFragment) + COMMON_VIEWS

# Topic add and edit forms

class TopicAddForm(AddFormFragment):

    form_fields = form.FormFields(ITopicSchema)

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)
        pm = cmfutils.getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            creator = 'Anonymous'
        else:
            creator = pm.getAuthenticatedMember().getUserName()

        topic = context.addConversation(title=data['title'],
                                        creator=creator)
        topic.update(description=data['description'])
        gsa_index(topic)
        getToolByName(context, 'plone_utils').addPortalMessage('The discussion was successfully added...')
        return topic.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class TopicAddView(Fragment):
    """ View class for topic add views
    """

    def asElement(self):
        #<view name="add.html" type="topic" title="Add Topic" section="workspaces"/>
        return Element('view',
                       name="add.html",
                       type="topic",
                       title="Add Discussion",
                       section="workspaces")

class TopicAddPage(Page):

    views = (TopicAddView, TopicAddForm) + COMMON_VIEWS

class TopicEditForm(EditFormFragment):

    form_fields = form.FormFields(ITopicSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        # the topic body is actually the text of the first comment
        return dict(title=context.Title(),
                    description=context.getRawDescription())

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        context.update(**data)
        gsa_reindex(context)
        return context.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class TopicEditView(Fragment):
    """ View class for topic add views
    """

    def asElement(self):
        #<view name="edit.html" type="topic" title="Edit Topic" section="workspaces"/>
        return Element('view',
                       name="edit.html",
                       type="topic",
                       title="Edit Discussion",
                       section="workspaces")

class TopicEditPage(Page):

    views = (TopicEditView, TopicEditForm) + COMMON_VIEWS

class TopicDeleteView(Fragment):
    """ View class for topic add views
    """

    def asElement(self):
        context = aq_inner(self.context)
        if self.request.get('confirm', None) is not None:
            # user has confirmed deletion
            # delete working around permission as this view as already
            # properly protected
            discussion_board = context.getForum()
            discussion_board.removeConversation(context.getId())
            gsa_unindex(context)
            # XXX status message
            raise SafeRedirect(discussion_board.absolute_url())
        # user hasen't confirmed yet, show confirmation view
        #<view name="delete.html" type="topic" title="Delete" section="workspaces"/>
        return Element('view',
                       name="delete.html",
                       type="topic",
                       title="Delete Discussion",
                       section="workspaces")

class TopicDeletePage(Page):

    views = (TopicDeleteView,) + COMMON_VIEWS

class CommentEditForm(EditFormFragment):

    form_fields = form.FormFields(ICommentSchema)

    def getDataFromContext(self):
        context = aq_inner(self.context)
        schema = context.Schema()
        return dict((field.__name__, schema[field.__name__].getEditAccessor(context)())
                    for field in self.form_fields
                    if 'r' in schema[field.__name__].mode)

    def applyChangesAndReturnURL(self, data):
        context = aq_inner(self.context)
        context.update(**data)
        gsa_reindex(context)
        # XXX status message?
        return context.absolute_url()

    def cancelURL(self):
        return self.context.absolute_url()

class CommentEditFragment(Fragment):
    """ View class for comment add views
    """

    def asElement(self):
        #<view name="edit.html" type="comment" title="Edit Some Discussion Topic" section="workspaces"/>
        return Element('view',
                       name="edit.html",
                       type="comment",
                       title=self.context.getConversation().Title(),
                       section="workspaces")

class CommentEditPage(Page):

    views = (CommentEditFragment, CommentEditForm) + COMMON_VIEWS


class CommentDeleteView(Fragment):
    """ View class for comment delete views
    """

    def asElement(self):
        context = aq_inner(self.context)
        if self.request.get('confirm', None) is not None:
            # user has confirmed deletion
            # delete working around permission as this view as already
            # properly protected
            context.delete()
            gsa_unindex(context)
            # XXX status message
            raise SafeRedirect(context.getConversation().absolute_url())
        # user hasen't confirmed yet, show confirmation view
        #<view name="delete.html" type="topic" title="Delete" section="workspaces"/>
        return Element('view',
                       name="delete.html",
                       type="comment",
                       title="Delete Comment",
                       section="workspaces")

class CommentDeletePage(Page):

    views = (CommentDeleteView,) + COMMON_VIEWS



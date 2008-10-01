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
from string import join
from urlparse import urlsplit, urlunsplit
from xml.parsers.expat import ExpatError

from Products.COL3.etree import tostring, fromstring
from elementtidy.TidyHTMLTreeBuilder import TreeBuilder
from Products.COL3.etree import Element, SubElement

from OFS.Traversable import Traversable
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.app.component.hooks import getSite
from Acquisition import aq_chain, aq_inner
from plone.app.blob.field import BlobField

from Products.statusmessages.interfaces import IStatusMessage
from Products.Archetypes.atapi import TextField, FileField, DateTimeField
from Products.Archetypes.atapi import IntegerField, BooleanField, StringField
from Products.Archetypes.atapi import ComputedField, ImageField, LinesField
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName

from Products.COL3.browser.base import Fragment
from Products.COL3.config import FAILED_LOGIN_PARAMETER
from Products.COL3.browser.interfaces import IUrlHelper
from Products.COL3.browser.interfaces import IContentHelper
from Products.COL3.content.label import Labeller
from Products.COL3.content.label import sortable_title
from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.permissions import MANAGE_WORKSPACE_PERMISSION
from Products.Ploneboard.content.PloneboardConversation import PloneboardConversation

def getWorkspace(context):
        for ob in aq_chain(aq_inner(context)):
            if IWorkspace.providedBy(ob):
                return ob

class WorkspaceFragment(Fragment):
    _sections = ('calendar', 'discussion', 'documents', )
    _section = 'home'
    _workspace = None
    def __init__(self, context, request):
        super(WorkspaceFragment, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            try:
                if ob.id in self._sections:
                    self._section = ob.id
            except AttributeError:
                pass #an object in the aq chain doesn't have
                     #an id attribute, ignore it...nothing to see here
            if IWorkspace.providedBy(ob):
                self._workspace = ob
        #this is admittedly ugly but members is a view on the workspace itself
        #so if we're not within one of the three workspace containers we need
        #to check to see if the user is accessing the members area via the url
        if self._section == 'home': #we didn't find a workspace container above
            urlparts = self.request.get('VIRTUAL_URL_PARTS', '')
            for urlpart in urlparts:
                if urlpart.endswith('workspace-members.html'):
                    self._section = 'members'
                if urlpart.endswith('edit-properties.html'):
                    self._section = 'setup'
        #okay (at least for now) we've exhausted all the places where we could be...
        #if we're not in the workspace root, we must be in the docs folder
        if self._section == 'home' and not IWorkspace.providedBy(context):
            self._section = 'documents'

    def _getWorkspace(self):
        return aq_inner(self._workspace)

    def asElement(self):
        workspace = self._getWorkspace()
        if workspace is None:
            return
        pw = getToolByName(workspace, 'portal_workflow')
        elem = Element('workspace')
        elem.attrib['href'] = workspace.absolute_url()
        if self._hasFolders():
            elem.attrib['hasfolders'] = 'hasfolders'
        SubElement(elem, 'title').text = workspace.Title()
        try:
            if workspace['workspacelogo'].getImage():
                logourl = workspace['workspacelogo'].absolute_url()
                SubElement(elem, 'logo',
                           {'src':logourl}).text = 'Workspace Title'
        except KeyError:
            pass #the workspace was created prior to adding the logo/icon code
        try:
            if workspace['workspaceicon'].getImage():
                iconurl = workspace['workspaceicon'].absolute_url()+'/image_icon'
                SubElement(elem, 'icon',
                           {'src':iconurl}).text = 'Workspace Icon'
        except KeyError:
            pass #the workspace was created prior to adding the logo/icon code
        SubElement(elem, 'editpropsurl').text = workspace.absolute_url()+'/edit-properties.html'
        try:
            SubElement(elem, 'logo', {'src':workspace.getLogo().absolute_url()})
        except AttributeError:
            pass #there hasn't been a file uploaded, don't add the node
        states = {'published':'false', 'private':'true'}
        is_private = states[pw.getInfoFor(workspace, 'review_state')]
        SubElement(elem, 'private').text = is_private
        SubElement(elem, 'section').text = self._section
        return elem

    def _hasFolders(self):
        wschildren = self._sections + ('news', 'wsmembers', 'front-page')
        pcat = getToolByName(self.context, 'portal_catalog')
        path = join(self._getWorkspace().getPhysicalPath(), '/')
        chillrens = pcat.searchResults(path={'query':path, 'depth':1})
        for child in chillrens:
            if child.is_folderish and child.id not in wschildren:
                return True
        return False

class UserFragment(Fragment):

    _workspace = None

    def __init__(self, context, request):
        super(UserFragment, self).__init__(context, request)
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self._workspace = ob

    def asElement(self):
        portal = getSite()
        # no portal, no game
        if portal is None:
            return None
        portal_url = portal.absolute_url()
        mtool = getToolByName(portal, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        # not authenticated, no game
        if member is None or mtool.isAnonymousUser():
            return None
        isAdmin = 'false'
        if (self._workspace is not None and
            member.getUser().has_permission(MANAGE_WORKSPACE_PERMISSION,
                                            self._workspace)):
            isAdmin = 'true'
        elem = Element('user')
        elem.attrib['href'] = ('%s/view-profile.html?userid=%s' %
                               (portal_url, member.getId()))
        SubElement(elem, 'username').text = member.getId()
        SubElement(elem, 'title').text = member.getProperty('fullname')
        email = member.getProperty('email')
        if email:
            SubElement(elem, 'email').text = email
            SubElement(elem, 'emailsuffix').text = email[email.index('@')+1:]
        lastlogin = member.getProperty('last_login_time')
        if lastlogin:
            SubElement(elem, 'lastlogin').text = lastlogin.ISO8601()
        SubElement(elem, 'isadmin').text = isAdmin
        return elem

class UserOrLoginboxFragment(UserFragment):

    def asElement(self):
        elem = super(UserOrLoginboxFragment, self).asElement()
        if elem is None:
            portal = getSite()
            portal_login_url = portal.absolute_url() + '/login'
            scheme, server, path, query, fragment = urlsplit(portal_login_url)
            if ':' not in server:
                # XXX quick workaround for port 84, which doesn't have an ssl
                # server configured. A proper fix would involve setting a
                # toggable configuration to enable SSL redirection
                portal_login_url = urlunsplit(('https', server, path, query, fragment))
            elem = Element('loginbox')
            # loginbox needs to return username/passwd using SSL

            elem.attrib['action'] = portal_login_url

            self.failedLogin = self.request.form.get(FAILED_LOGIN_PARAMETER, None)
            if self.failedLogin is None:
                elem.attrib['username'] = "Username"
            else:
                elem.attrib['username'] = self.failedLogin
                elem.attrib['failed'] = '1'
        return elem

class MessageFragment(Fragment):
    """Fragment to hold any status messages, to set messages, modules would
       need to call:
           getToolByName(context, 'plone_utils').addPortalMessage('the message')
    """
    def asElement(self):
        request = self.request
        status = IStatusMessage(request)
        messages = status.showStatusMessages()
        if messages:
            root = Element('messages')
            for message in messages:
                elem = SubElement(root, 'message')
                elem.text = message.message
            return root

class KeywordsFragment(Fragment):
    """Fragment to display all labels in the workspace. Use it inside
    workspaces only
    NOTE - this used to be called LabelsFragment.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def asElement(self):
        labeller = Labeller(self.context)
        labels_tag = Element('keywords')
        for label in labeller.listLabels():
            SubElement(labels_tag, 'item').text = label
        if len(labels_tag):
            return labels_tag

class CurrentKeywordsFragment(Fragment):
    """Fragment to display labels for the current context. Use it inside
    workspaces only.
    NOTE - this used to be called CurrentLabelsFragment.  At the beginning of the project
    what are now called "keywords" were referred to as "labels".  End users didn't like
    "labels" so the decision was made to change to "labels" to "keywords".  Any reference
    to labels is due to not wanting to change the underlying machinery that handles labelling
    """
    def asElement(self):
        labeller = Labeller(self.context)
        current_labels_tag = Element('currentkeywords')
        for label in labeller.getLabelRecordsForContent(self.context):
            querystr = '/documents/withkeyword-documents.html?keyword='
            browseurl = self._getWorkspaceUrl() + querystr + sortable_title(label.Title())
            SubElement(current_labels_tag, 'item', href=browseurl).text = label.Title()
        if len(current_labels_tag):
            return current_labels_tag

    def _getWorkspaceUrl(self):
        for link in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(link):
                return link.absolute_url()

class BreadcrumbsFragment(Fragment):
    """ Fragment to return the bredcrumbs for a given context"""

    def getContext(self):
        """ override this to parameterize the breadcrumb context """
        return aq_inner(self.context)

    def asElement(self, xtra_breadcrumb_ids=None):
        """Added the xtra_breadcrumb_ids to this asElement method so that
           we don't have to wire up traversable views and go through zcml
           hoops to get view titles added to the breadcrumbs, the ids should
           be passed in as a sequence of dictionaries like so (if href is blank,
           no href attribute will be added to the element):
           ({'title':'breadcrumb_one_title', 'href':'http://url'},
            {'title':'breadcrumb_two_title', ''})"""
        context = self.getContext()
        request = self.request
        portal = getSite()
        # no portal, no game
        if portal is None:
            return None
        root = Element('breadcrumbs')
        elem = SubElement(root,'entry')
        elem.text = 'Home'
        #portal_url = portal.absolute_url()
        elem.attrib['href'] = portal.absolute_url()
        view = getMultiAdapter((context, request), name='breadcrumbs_view')
        context_url = getattr(context, 'absolute_url', lambda: None)()
        if context_url:
            SubElement(root,'base').text = context_url+'/'
        else:
            SubElement(root,'base').text = portal.absolute_url()+'/'
        for breadcrumb in view.breadcrumbs():
            elem = SubElement(root, 'entry')
            elem.text = breadcrumb.get('Title','')
            entry_url = breadcrumb.get('absolute_url', None)
            if context_url != entry_url:
                elem.attrib['href'] = entry_url+'/'
            elif context_url == entry_url and xtra_breadcrumb_ids:
                elem.attrib['href'] = entry_url+'/'
        if xtra_breadcrumb_ids:
            for crumb in xtra_breadcrumb_ids:
                elem = SubElement(root, 'entry')
                elem.text = crumb['title']
                href = crumb.get('href', None)
                if href != '' and href is not None:
                    elem.attrib['href'] = crumb.get('href', '')
        return root

def cleanup(values, as_string=False):
    div = Element('{http://www.w3.org/1999/xhtml}div', {'class':'tinyFix'})
    div.text = ''
    b = TreeBuilder('utf-8')
    if isinstance(values, basestring):
        values = [values]
    for value in values:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        b.feed(value)
    tree = b.close()
    body = tree.find('{http://www.w3.org/1999/xhtml}body')
    children = body.getchildren()
    text = body.text
    # strip out any extra divs.
    while (len(children) == 1
            and children[0].tag == '{http://www.w3.org/1999/xhtml}div'):
        body = children[0]
        children = body.getchildren()
        text = body.text
    if children:
        for child in children:
            div.append(child)
    if text:
        div.text = text
    if as_string:
        return tostring(div)
    return div

class ResourceFragment(Fragment):
    """ Fragment to return metadata for the current context"""
    def renderXML(self, tree=None):
        return self._renderXML(tree)

    def _renderXML(self, tree):
        doc = self.asElement()
        if tree is not None:
            tree.append(doc)
            return tree
        return tostring(doc)

    def asElement(self):
        ctx = self.context
        doc = Element('resource')
        if not (shasattr(ctx, 'Schema') and shasattr(ctx, 'UID')):
            return None

        doc.attrib['uuid'] = ctx.UID()
        doc.attrib['href'] = ctx.absolute_url()

        attachments = None

        seen = []

        helper = getMultiAdapter((self.context, self.request), IContentHelper)
        urlhelper = getMultiAdapter((self.context, self.request), IUrlHelper)
        skip = ('uid', 'mode', 'date', 'description')
        info = helper.getInfo()
        itemlist = []
        for key, value in info.items():
            if key in skip:
                continue
            elif key in seen:
                continue
            elm = Element(key)
            if(key == 'author'):
                elm.text = value
                elm.attrib['href'] = urlhelper.getProfileUrl(info.get('creator', ctx.Creator()))
                itemlist.append(elm)
                seen.append(key)
                continue
            elif key == 'type':
                ti = self.context.getTypeInfo()
                if ti is None:
                    raise ValueError('Object at %s does not have a matching '
                                     'type in the portal_types tool.' % self.context.absolute_url())
                elm.attrib['title'] = ti.title_or_id()
                elm.text = ti.id
                itemlist.insert(0, elm)
                seen.append(key)
                continue
            elif key == 'mimetype':
                elm.attrib['id'] = value
                elm.text = value.upper()
                itemlist.append(elm)
                seen.append(key)
                continue
            if value in (True, False):
                value = str(value).lower()
            try:
                elm.text = unicode(value, 'utf-8')
                itemlist.append(elm)
            except TypeError:
                elm.text = value
                itemlist.append(elm)
            seen.append(key)

        for it in itemlist:
            if it.text is not None and it.text != '':
                doc.append(it)

        exclusions = ('locallyAllowedTypes',
                      'immediatelyAddableTypes',
                      'constrainTypesMode',
                      'allowDiscussion',
                      'excludeFromNav',
                      'presentation',
                      'tableContents',
                      'contributors',
                      'creators',
                      'labels',
                      'libraryreference',
                      'category',
                      'maxAttachments',
                      'maxAttachmentSize')
        for f in ctx.Schema().fields():
            if f.getName() not in exclusions and f.getName() not in seen:
                __traceback_info__ = ("rendering field", f.getName())
                if 'r' not in f.mode:
                    # skip non-readable fields
                    continue

                if 'w' not in f.mode or isinstance(f, (TextField, ComputedField)):
                    accessor = f.getAccessor(ctx)
                else:
                    accessor = f.getEditAccessor(ctx)

                # Should we do some cleanup here? What about non-HTML content?
                assert accessor is not None, "%s has no accessor?" % f.getName()
                value = accessor()
                if isinstance(value, (list, tuple)):
                    values = [str(v) for v in value]
                else:
                    values = [value]

                ct = None
                if isinstance(f, (FileField, BlobField)):
                    ct = f.getContentType(ctx)
                if (isinstance(f, (FileField, BlobField))
                    and not isinstance(f, TextField)
                    and not isinstance(f, ImageField)):
                    if f.getName() == 'gisdata':
                        if ctx.getGisdata().filename:
                            gisdataelem = Element('gisdata',
                                                  href=ctx.getGisdata().absolute_url(),
                                                  mime='text/xml',
                                                  name='xml')
                            gisdataelem.text = f.getFilename(ctx)
                            doc.append(gisdataelem)
                    else:
                        if attachments is None:
                            attachments = Element('attachments')
                        filename = ''
                        try:
                            filename = ctx.getUploadedFile().filename
                        except AttributeError:
                            filename = f.getFilename(ctx)
                        if value and filename != '':
                            attachment = Element('attachment')
                            attachments.append(attachment)
                            attachment.attrib['mime'] = ct
                            attachment.attrib['name'] = f.getName()
                            fname = f.getFilename(ctx)
                            dl = doc.attrib['href']
                            attachment.attrib['href'] =  dl
                            try:
                                fname = unicode(fname, 'utf-8')
                            except TypeError:
                                # already is unicode
                                pass
                            attachment.text = fname
                else:
                    elm = Element(f.getName())
                    seen.append(f.getName())
                    if (isinstance(f, (TextField, StringField))
                        and f.getWidgetName() in ('RichWidget',)
                        and ct in ('text/html', 'text/xml')):
                        value = f.getEditAccessor(ctx)()
                        try:
                            elm.append(fromstring(value))
                        except ExpatError:
                            elm.append(cleanup(value))
                        doc.append(elm)
                    elif (isinstance(f, TextField)
                        and f.getWidgetName() in ('TextAreaWidget', )
                        and isinstance(ctx, PloneboardConversation)
                        and f.getName() == 'description'):
                        elm.tag = 'text'
                        value = f.getEditAccessor(ctx)()
                        try:
                            elm.append(fromstring(value))
                        except ExpatError:
                            elm.append(cleanup(value))
                        doc.append(elm)
                    elif isinstance(f, LinesField):
                        for value in values:
                            SubElement(elm, 'item').text = unicode(value, 'utf-8')
                        doc.append(elm)
                    else:
                        text = []
                        for value in values:
                            if value is not None:
                                if isinstance(f, DateTimeField):
                                    text.append(value.ISO8601())
                                elif isinstance(f, BooleanField):
                                    text.append(str(value).lower())
                                elif isinstance(f, ImageField):
                                    if value is not None:
                                        try:
                                            elm.attrib['href'] = value.absolute_url()
                                        except AttributeError:
                                            pass
                                elif isinstance(f, IntegerField) and value is None:
                                    text.append('0')
                                else:
                                    if not isinstance(value, basestring):
                                        value = str(value)
                                    text.append(value)
                        utext = []
                        for t in text:
                            if isinstance(t, unicode):
                                utext.append(t)
                            else:
                                utext.append(unicode(t, 'utf-8'))
                        elm.text = u'; '.join(utext)
                        if elm.text is not None and elm.text != '':
                            doc.append(elm)

        if attachments is not None:
            doc.append(attachments)
        return doc

WITHFOLDER_VIEWS = (WorkspaceFragment , MessageFragment, UserOrLoginboxFragment,
                    ResourceFragment)

COMMON_VIEWS = WITHFOLDER_VIEWS +(BreadcrumbsFragment, )

COMMON_VIEWS_NORESOURCE = (WorkspaceFragment , MessageFragment, UserOrLoginboxFragment,
                           BreadcrumbsFragment)

class MenuFragment(Fragment):

    additems = ()
    utilitems = ()

    def asElement(self):
        root = Element('menus')
        url = self.context.absolute_url()
        show_add_menu = self._showAddMenu()
        if show_add_menu:
            addmenu = SubElement(root, 'addmenu')
            for label, href in self.additems:
                elem = SubElement(addmenu, 'entry')
                elem.text = label
                elem.attrib['href'] = '%s/%s' % (url, href)
        if self.utilitems:
            utilmenu = SubElement(root, 'utilitymenu')
            for label, href in self.utilitems:
                elem = SubElement(utilmenu, 'entry')
                elem.text = label
                elem.attrib['href'] = '%s/%s' % (url, href)
        return root

    #The default it to always show the add menu
    def _showAddMenu(self):
        return True

class BaseBatchFragment(Fragment):
    batch_provider = None
    sort_on = 'title'
    letters_param = 'REMOVE'
    columns = (('title', {'default_order':'asc',
                             'label': 'Title'}),
               ('mimetype', {'default_order':'asc',
                          'label': 'Format'}),
               ('size', {'default_order':'asc',
                          'label': 'Size'}),
               ('date', {'default_order':'asc',
                          'label': 'Date'}),)
    def asElement(self):
        if self.batch_provider is None:
            raise NotImplementedError, 'No Batch Provider Given'
        context = self.context
        request = self.request
        columns = self.columns
        letters_param = self.letters_param
        batchfragment = BatchFragmentFactory(self.batch_provider,
                                             columns=columns,
                                             letters_param=letters_param)
        if request.get('sort_on', None) is None:
            request['sort_on'] = self.sort_on
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class COLMemberMenuFragment(MenuFragment):
    """Use this fragment if someone needs to be a COL3 member
       in order to add or edit
    """
    def _showAddMenu(self):
        pm = getToolByName(self.context, 'portal_membership')
        return not pm.isAnonymousUser()

class TraversableView(BrowserView, Traversable):

    def __init__(self, context, request):
        self.context = context
        self.request = self.REQUEST = request

    def getId(self):
        return self.__name__

    def title_or_id(self):
        return self.getId()


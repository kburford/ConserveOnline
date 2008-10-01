import urllib
from xml.sax import saxutils

from Acquisition import aq_inner
from zope.interface import implements, Interface, providedBy
from zope.component import getMultiAdapter, adapts
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IBaseContent
from Products.Ploneboard.interfaces import IConversation

from Products.COL3.etree import Element, SubElement
from Products.COL3.etree import tostring

from interfaces import IUserHelper, IUrlHelper, IContentHelper

from Products.COL3.config import MIMETYPES

def _calculateSize(sizeStr):
        const = {'MB':1024,
                 'GB':1024*1024}
        sizeStr = sizeStr.split(' ')
        size = sizeStr[0]
        units = sizeStr[1]
        if units == 'kB':
            return str(int(float(size)))
        else:
            return str(int(float(size)) * const[units])

class UrlHelper(BrowserView):
    adapts(Interface, IDefaultBrowserLayer)
    implements(IUrlHelper)

    def getQuery(self):
        form = self.request.form
        parts = ['%s=%s' % (k,v) for (k,v) in form.items()]
        q = '&'.join(parts)
        return saxutils.escape(q)

    def quote(self, url):
        return urllib.quote(url)

    def getBaseUrl(self, postfix=True):
        ptool = getToolByName(aq_inner(self.context), 'portal_url')
        portal = ptool.getPortalObject()
        url = portal.absolute_url()
        if postfix and not url.endswith('/'):
            url = url + '/'
        return url

    def getProfileUrl(self, username):
        return ('%sview-profile.html?userid=%s' %
                (self.getBaseUrl(), username))


class UserHelper(BrowserView):
    adapts(Interface, IDefaultBrowserLayer)
    implements(IUserHelper)

    def getInfo(self, username=None, member=None):
        context = self.context
        root = Element('user')
        helper = getMultiAdapter((self.context, self.request), IUrlHelper)
        mtool = getToolByName(context, 'portal_membership')
        if member is None:
            if username is None and not mtool.isAnonymousUser():
                member = mtool.getAuthenticatedMember()
                username = member.getUserName()
            elif username:
                member = mtool.getMemberById(username)
        else:
            username = member.getUserName()
        if member:
            root.attrib['href'] = helper.getProfileUrl(username)
            userelem = SubElement(root, 'username')
            userelem.text = username
            userelem = SubElement(root, 'title')
            userelem.text = member.Title()
            userelem = SubElement(root, 'lastlogin')
            userelem.text = ''
            userelem = SubElement(root, 'profilepercentage')
            userelem.text = '67'
        return tostring(root)

class ContentHelper(BrowserView):
    adapts(Interface, IDefaultBrowserLayer)
    implements(IContentHelper)

    def getInfo(self):
        context = self.context
        mt = getToolByName(self.context, 'portal_membership')
        text = ''
        try:
            creator = self.context.Creator()
            if isinstance(creator, unicode):
                creator = creator.encode()
            author = mt.getMemberInfo(creator)
        except AttributeError:
            creator = author = '<Unknown>'

        mode = self.request.form.get('form.mode', 'view')
        try:
            uid = context.UID()
        except AttributeError:
            uid = None
        try:
            description = context.Description()
        except AttributeError:
            description = None
        #XXX Use reflection here instead of embedded try/except
        try:
            # XXX and stop specialcasing!
            if IConversation.providedBy(context):
                text = context.getRawDescription()
            else:
                text = context.getRawText()
        except AttributeError:
            try:
                text = context.getText()
            except AttributeError:
                pass
        size = _calculateSize(context.getObjSize())
        return dict(
            uid=uid,
            type=context.Type(),
            description = description,
            size=size,
            mimetype=MIMETYPES.get(context.getContentType(), 'None Found'),
            author=author and author.get('fullname', author.get('username', creator)) or creator,
            mode=mode)

    def getFullInfo(self):
        context = self.context
        data = self.getInfo()

        impl = providedBy(context)
        if not impl.isOrExtends(IBaseContent):
            return data

        for field in context.Schema().fields():
            name = field.__name__
            if name in data:
                continue
            value = field.get(context)
            if field.type == 'file':
                if not value:
                    value = {'id':'','url':''}
                else:
                    value = {'id':value.filename,
                             'url':value.absolute_url()}
            if field.type == 'image':
                if value:
                    value = value.absolute_url()
            data[name] = value
        return data

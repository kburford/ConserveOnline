# TEMP until we get proper indexing story this should be enough to demonstrate concept.
# do not over-engineer
import logging
import os.path

from Acquisition import aq_inner, aq_chain
from DateTime.DateTime import DateTime
from Products.CMFPlone.log import log_exc

from types import ListType, TupleType

from enfold.gsa import gsa
import BeautifulSoup
import base64

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from Products.COL3.content.interfaces import IIndexable
from Products.COL3 import config
from Products.COL3.browser.common import cleanup
from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.interfaces.library import ILibraryFile
from Products.CachedGSAIndexer.config import TOOL_NAME

MAX_UPLOAD_BYTES = 1000000000 
LARGE_CONTENT_BYTES = 100000000
EXTENSIONS_NOT_INDEXED = """jpg mov zip""".split()

INDEXABLE_MIMETYPES = """
application/msword
application/pdf
application/vnd.ms-excel
application/vnd.ms-powerpoint
application/x-dbase
text/comma-separated-values
text/css
text/html
text/plain
*meta*
""".strip().split('\n')

INDEXABLE_TEXT_PLAIN = ['DOC','PDF','PPT','css','doc','htm','html','pdf','ppt','sql','txt','xls','']


class date:

    def __init__(self, name):
        self.name = name

    def __call__(self, item):
        v = getattr(item, self.name, lambda: DateTime)()
        if not v or not isinstance(v, DateTime):
            v = DateTime()
        return v.ISO8601()

class collection:

    def __init__(self, name):
        self.name = name

    def __call__(self, item):
        v = getattr(item, self.name, lambda: tuple)()
        if isinstance(v, basestring):
           v = (v,)
        if v is None:
           v = []
        try:
           return "\n".join(v)
        except TypeError:
           return ""

class _float:
    def __init__(self, name, default=0.0):
        self.name = name
        self.default = default

    def __call__(self, item):
        if not shasattr(item, self.name):
            return float(self.default)
        value = getattr(item, self.name)()
        try:
            return float(value)
        except ValueError:
            return float(self.default)

def getValue(item, attrs):
    if type(attrs) not in (ListType, TupleType):
        attrs = (attrs,)
    default = lambda : ''
    value = ''
    for attr_name in attrs:
        if isinstance(attr_name, basestring):
            if not shasattr(item, attr_name):
                continue
            attr = getattr(item, attr_name, default)
        else:
            # It's a function.
            func = attr_name
            def call(item=item):
                return func(item)
            attr = call
        __traceback_info__ = (item, attr_name, attr)
        try:
            if callable(attr):
                value = attr()
            else:
                value = attr
        except:
            log_exc('Failure extracting info %r:%r' % (item, attr_name))
            value = ''
        if value:
            return value
    return value

def cleanText(text, format, url, limit):
    #remove this comment and next line to reenable cleanText
    #return text
    logger = logging.getLogger('COL3.content.indexer.cleanText') 
    if len(text) > limit:
        """ for now, don't attempt to index content this big:
        2008-04-08T02:47:21 ERROR Zope.SiteErrorLog http://col3dev.tnc.org/index_workspaces
        Traceback (innermost last):
          ...
          Module Products.CachedGSAIndexer.tool, line 166, in flushQueue
          Module enfold.gsa.gsa, line 847, in sendFeed
          Module enfold.gsa.gsa, line 780, in buildFile
          Module xml.dom.minidom, line 47, in toxml
          Module xml.dom.minidom, line 62, in toprettyxml
          Module StringIO, line 271, in getvalue
        MemoryError"""
        logger.warn("Content too large to index (%d bytes): %s" % (len(text),url))
        return ""

    # the GSA doesn't attempt to index media files, tarballs, and other non-textual binaries
    ext = os.path.splitext(url)[1][1:]
    if ext.find("?"):
        ext = ext[:ext.find("?")]
    if format not in INDEXABLE_MIMETYPES or (format=='text/plain' and ext not in INDEXABLE_TEXT_PLAIN):
        logger.info("GSA would not index content with '%s' mimetype and '%s' extension: %s" % (format, ext,url))
        return ""

    if format == "*meta*" or (format[:4] == "text" and ext in ['css','htm','html','sql','txt',]):
        text = unicode(text, errors='replace')
    #else:
    logger.info("mimetype=%s, ext=%s for %s" % (format, ext, url))
        #text = unicode(text, 'utf-8', error='replace')

    return text

ATTR_MAP = {
        #'id': ('getId',),
        #'uid': ('UID',),
        'Title': ('Title',),
        #'description': ('Description',),
        #'keywords': (collection('Subject'),),
        'url': ('getRemoteUrl', 'absolute_url',),
        #'credit': (collection('Contributors'),),
        #'body':('getText', 'CookedBody', 'getBody',),
        #'created': (date('created'),),
        #'modified': (date('modified'),),
        #'start_date': (date('start'),),
        #'end_date': (date('end',),),
        #'effective_date': (date('effective'),),
        #'expires_date': (date('expires'),),
        #'portal_type': ('getPortalTypeName', 'portal_type'),
        #'format': ('Format', 'getContentType',),
        }

class Indexer(object):
    tmpl = '<html><title>%s</title><body>%s</body></html>'

    def __init__(self, context):
        self.context = context
        self.data = {}

    def _getCOLMetadata(self, ob):
        if len(ob.getBiogeographic_realm()):
            self.data['biogeographic_realm'] = ob.getBiogeographic_realm()
        if len(ob.getHabitat()):
            self.data['habitat'] = " ".join(ob.getHabitat())
        if len(ob.getConservation()):
            self.data['conservation'] = " ".join(ob.getConservation())
        if len(ob.getDirectthreat()):
            self.data['directthreat'] = " ".join(ob.getDirectthreat())
        if len(ob.getMonitoring()):
            self.data['monitoring'] = " ".join(ob.getMonitoring())
        if len(ob.getKeywords()):
            self.data['keywords'] = " ".join(ob.getKeywords())
 
    def _addWorkspaceMetadata(self):
        for ob in aq_chain(aq_inner(self.context)):
            if IWorkspace.providedBy(ob):
                self.data['workspace'] = ob.Title() and ob.Title() or ob.id
                self._getCOLMetadata(ob)
                break

    def _addLibraryMetadata(self):
        context = self.context
        if ILibraryFile.providedBy(context):
            self.data['library'] = context.title_or_id()
            self._getCOLMetadata(context)

    @property
    def lastmodified(self):
        fmt = "%a, %d %b %Y %X -0400"
        modified = self.context.ModificationDate()
        return modified.strftime(fmt)

    @property
    def url(self):
        return self.context.absolute_url()

    @property
    def metadata(self):
        func = getValue
        obj = self.context
        for attr, methods in ATTR_MAP.items():
            value = func(obj, methods)
            if value:
                self.data[attr] = value
        self._addLibraryMetadata()
        self._addWorkspaceMetadata()
        logger = logging.getLogger('COL3.content.indexer.metadata') 
        logger.info(self.data)
        return self.data

    def metadataPlus(self, **kw):
        data = self.metadata
        for key in kw:
            data[key] = kw[key]
        return data
    
    @property
    def format(self):
        context = self.context
        value = getValue(context, ('Format', 'getContentType'))
        if not value:
            value = 'application/x-unknown'
        return value

    @property
    def body(self):
        context = self.context
        value = getValue(context, ('getText', 'CookedBody', 'getBody',))
        if self.format == 'text/html':
            return self.tmpl % (self.metadata['Title'], value)
        return value

class FileIndexer(Indexer):
    @property
    def format(self): 
        context = self.context
        value = getValue(context, ('getContentType'))
        if not value:
            value = 'application/x-unknown'
        return value

    @property
    def body(self):
        context = self.context
        return str(context.getFile())

class EventIndexer(Indexer):
    @property
    def format(self): 
        return 'text/html'

class PBConversationIndexer(Indexer):
    @property
    def format(self):
        return 'text/html'
    @property
    def body(self):
        context = self.context
        value = self.tmpl % (context.title_or_id(), 
                             context.Description())
        return value

class ProfileIndexer(Indexer):
    @property
    def format(self):
        return 'text/html'

    @property
    def url(self):
        context = self.context
        request = self.context.REQUEST
        serverurl = request['SERVER_URL']
        url = '%s/view-profile.html?userid=%s' % (serverurl, context.getId())
        return url

    @property
    def body(self):
        context = self.context
        pm = getToolByName(context, 'portal_membership')
        user = pm.getMemberById(context.getId())
        first = user.getProperty('firstname', '')
        last = user.getProperty('lastname', '')
        bio = user.getProperty('description', '')
        value = self.tmpl % ('%s %s' % (first, last),
                             bio)
        return value    

class WorkspaceIndexer(Indexer):
    @property
    def format(self):
        return 'text/html'

    @property
    def body(self):
        context = self.context
        logger = logging.getLogger('COL3.content.WorkspaceIndexer.body')
        logger.info('Calling body method in WorkspaceIndexer for '+context.title_or_id()+' workspace...')
        value = self.tmpl % (context.title_or_id(),
                             context.Description())
        return value

class KeywordIndexer(Indexer):
    @property
    def format(self):
        return 'text/html'

    @property
    def body(self):
        context = self.context
        value = self.tmpl % (context.title_or_id(),
                             context.Description())
        return value

def get_indexer():
    return gsa.Indexer("http://%s:%d/xmlfeed" % (config.GSA_HOST,
                                                 config.GSA_FEED_PORT),
                       config.GSA_FEED,
                       gsa.Indexer.INCREMENTAL_FEED)

#def index(content):
#    if not config.GSA_ENABLED:
#        return
#    app = get_indexer()
#    idx = IIndexable(content)
#    app.addItem(idx.url, idx.metadata, idx.format, idx.body)
#    app.sendFeed()


def index(content, limit=LARGE_CONTENT_BYTES):
    __traceback_info__ = "indexing " + "/".join(content.getPhysicalPath())

    logger = logging.getLogger('COL3.content.index') 
    gt = getToolByName(content, TOOL_NAME)
    idx = IIndexable(content)
    meta = idx.metadata
    #import pdb; pdb.set_trace()
    if meta.has_key('Title'):
        meta['Title'] = cleanText(meta['Title'], '*meta*', "Title: " + idx.url, limit)
    if meta.has_key('library'):
        meta['library'] = cleanText(meta['library'], '*meta*', "meta:library: " + idx.url, limit)
    if meta.has_key('workspace'):
        meta['workspace'] = cleanText(meta['workspace'], '*meta*', "meta:workspace: " + idx.url, limit)
    body = cleanText(idx.body, idx.format, idx.url, limit)
    if len(body) > LARGE_CONTENT_BYTES:
        # we can index large content, but make sure we have as much memory to work with as possible.
        logger.info( str(len(body)) + " bytes in " + idx.url)
        gt.flushQueue()
        gt.add(idx.url, meta, idx.format, body)
        gt.flushQueue()
    else:
        gt.add(idx.url, meta, idx.format, body)
    return len(idx.url)+len(meta)+len(idx.format)+len(body)

#def reindex(content):
#    if not config.GSA_ENABLED:
#        return
#    app = get_indexer()
#    idx = IIndexable(content)
#    app.updateItem(idx.url, idx.metadata, idx.format, idx.body)
#    app.sendFeed()

def reindex(content, limit=MAX_UPLOAD_BYTES):
    gt = getToolByName(content, TOOL_NAME)
    idx = IIndexable(content)
    meta = idx.metadata
    body = cleanText(idx.body, idx.format, idx.url, limit)
    gt.update(idx.url, meta, idx.format, body)
    return len(idx.url)+len(meta)+len(idx.format)+len(body)

#def unindex(content):
#    if not config.GSA_ENABLED:
#        return
#    app = get_indexer()
#    app.deleteItem(content.absolute_url())
#    app.sendFeed()

def unindex(content):
    gt = getToolByName(content, TOOL_NAME)
    gt.delete(content.absolute_url())

#def setup_gsa():
#    from App.config import getConfiguration
#    gsa_config = getConfiguration().product_config.get('col3_gsa')
#    if gsa_config is None:
#        # GSA is disabled
#        config.GSA_ENABLED = False
#        return
#    config.GSA_ENABLED = True
#    config.GSA_HOST = gsa_config['host']
#    config.GSA_FEED_PORT = int(gsa_config['port'])
#    config.GSA_FEED = gsa_config['feed']


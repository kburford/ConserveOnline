import logging
import sys, os
from time import sleep
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import setSite

from Products.COL3 import config
from Products.COL3.content.indexer import get_indexer, index
from Products.COL3.content.interfaces import IIndexable
from Products.CachedGSAIndexer.config import TOOL_NAME
from Products.CMFCore import permissions

"""Feeds cannot be uploaded using HTTPS.
Instead, call as external method using XPath
The XML feed must be < 1 GB in size. If your feed is
larger than 1 GB, consider breaking the feed into smaller
feeds that can be pushed more efficiently.
"""
INDEX_GSA_SETUP_FILE = "index_gsa_setup.cfg"
MAX_CONTENT_BYTES = 20000000
MAX_QUEUED_BYTES =  30000000
MAX_QUEUE_LENGTH = 50 	# need to keep this small for bulk-indexing, for now 
security.declareProtected(permissions.ManagePortal, 'index_container')
def index_container(self, path_to_container):

    catalog = getToolByName(self, 'portal_catalog')
    gt = getToolByName(self, TOOL_NAME)

    items = catalog(path=path_to_container, portal_type=config.INDEXABLE_TYPES)
    n=0
    count = 0
    logging.info("Indexing %d items in %s" % (len(items),path_to_container))
    queued_bytes = 0
    start = 0
    size_limit = MAX_CONTENT_BYTES
    try:
        cfgfile = open(os.path.join(os.getcwd(),INDEX_GSA_SETUP_FILE), 'rU')
        logging.info(INDEX_GSA_SETUP_FILE + " found")
    except:
        logging.info(INDEX_GSA_SETUP_FILE + " not found")
        cfgfile = None
    if cfgfile:
        buf = cfgfile.readlines()
        starttag = path_to_container + ":start:"
        if len(buf) and buf[0].startswith(starttag):
            start = int(buf[0][len(starttag):])
        cfgfile.close()
    gt.setQueueEnabled(True)
    skipping = (start>0)
    if skipping:
        logging.info("Starting with item %d" % start)
    for item in items:
        if skipping:
            n += 1
            if n >= start:
                skipping = False
            else:
                continue

        content = item.getObject()
        if content:
            try:
                #import pdb; pdb.set_trace()
                queued_bytes += index(content, size_limit)
                n += 1
                count += 1
                if n % 5 == 0:
                    logging.info("Processed %d items" % n)
            except (UnicodeDecodeError, UnicodeEncodeError),e:
                errstr = e.__class__.__name__ + ":" + str(e)
                logging.error("Unicode-related error when indexing %s\n%s\nObject: " % 
                        (content.absolute_url(),errstr, e.object))
                logging.info("Skipping this url, will continue with next.")
            if gt.getQueueLength() >= MAX_QUEUE_LENGTH or gt.getQueuedBytes() > MAX_QUEUED_BYTES:
                # Keep the queue small, else we get memory errors during xml feed construction
                logging.info("\t%d items indexed; queueing %d more totalling %d bytes" % (n, count, queued_bytes))
                try:
                    gt.flushQueue()
                except (UnicodeDecodeError, UnicodeEncodeError), e:
                    errstr = e.__class__.__name__ + ":" + str(e)
                    logging.error("Unicode-related error when flushing queue\n%s\nObject: %s" % 
                            (content.absolute_url(), errstr, e.object))
                except:
                    import traceback
                    logging.error("Exception caught when flushing queue")
                    traceback.print_exc()
                cfgfile = open(os.path.join(os.getcwd(),INDEX_GSA_SETUP_FILE), 'wU')
                if cfgfile:
                    starttag = path_to_container + ":start:"
                    cfgfile.write(starttag+str(n))
                    cfgfile.close()
                count = 0
                queued_bytes = 0

    logging.info("Finished: indexed %d of %d items in %s" % (n, len(items), path_to_container))
    os.remove(cfgfile)


security.declareProtected(permissions.ManagePortal, 'index_people')
def index_people(self):
    mt = getToolByName(self, 'portal_membership')
    members = mt.listMembers()
    logging.info("Indexing %d members" % len(members))
    n=0
    gt = getToolByName(self, TOOL_NAME)
    for member in members:
        if member:
            n+=1
            index(member)
    gt.flushQueue()
    logging.info("Finished: indexed %d members" % n)

security.declareProtected(permissions.ManagePortal, 'index_workspaces')
def index_workspaces(self):
    plonesite=self.id
    WSPATH = "/"+plonesite+"/workspaces"
    index_container(self, WSPATH)

security.declareProtected(permissions.ManagePortal, 'index_library')
def index_library(self):
    plonesite=self.id
    LIBPATH = "/"+plonesite+"/library"
    index_container(self, LIBPATH)

security.declareProtected(permissions.ManagePortal, 'index_all')
def index_all(self):
    plonesite=self.id
    index_people(self)
    index_library(self)
    index_workspaces(self)

if __name__=='__main__':
    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest
    app=makerequest(app)
    plonesite=sys.argv[1]
    portal = app.unrestrictedTraverse(plonesite)
    setSite(portal)
    newSecurityManager(None, portal.getWrappedOwner())
    logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',                    
                    stream=sys.stdout)

    index_all(portal)

# COL3
# Copyright(C), 2007, Enfold Systems, Inc. - ALL RIGHTS RESERVED
#
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied
# this software.  Any inquiries concerning the scope or
# enforceability of the license should be addressed to:
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

"""
This is a 'zopectl run' script that submits all or queued DOI records to crossref.org
"""

import sys, string, transaction
from logging import getLogger
from zope.app.component.hooks import setSite

from Products.CMFCore.utils import getToolByName

log = getLogger('Products.ConserveOnline.Extensions.createDOIRecords')

def logger_and_responder(response):
    def log_and_respond(msg):
        response.write(msg + '\n')
        log.info(msg)
    return log_and_respond

def setResponseCharsetAndGetLogger(self):
    response = self.REQUEST.RESPONSE
    charset = self.portal_properties.site_properties.default_charset
    response.setHeader("Content-Type", "text/plain; charset=" + charset)
    logresp = logger_and_responder(response)
    return logresp


def createDOIRecords(self, from_queue=True, area='test'):
    """ Simple method that will call the appropriate method on the
        CrossRef tool to update the CrossRef site with library DOIs
    """
    logresp = setResponseCharsetAndGetLogger(portal)
    crossref_tool = getToolByName(self, 'crossreference_tool')
    nfiles = len(crossref_tool.keys())
    result = crossref_tool.processLibraryFiles(from_queue, area)
    logresp("%d queued files processed; html returned was\n%s" % (nfiles, result))

if __name__=='__main__':
    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest
    app=makerequest(app)
    plonesite=sys.argv[1]
    portal = app.unrestrictedTraverse(plonesite)
    setSite(portal)
    newSecurityManager(None, portal.getWrappedOwner())

    from_queue = True
    area = "test"
    for i in range(2, len(sys.argv)-1):
        if sys.argv[i]=='live':
            area = 'live'
        # We will not be submitting all existing library file metadata to crossref, 
        # so always leave from_queue set to True.
        #elif sys.argv[i]=='all':
        #    from_queue = False

    createDOIRecords(portal, from_queue=from_queue, area=area)

    txn = transaction.get()
    txn.note("Completed DOI submission")
    txn.commit()


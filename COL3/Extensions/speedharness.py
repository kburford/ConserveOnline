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

"""This is a 'zopectl run' script that times and profiles the backend XML
generation of a number of URLs.

It requires _lsprof.so and cProfile.py that should be taken from a Python 2.5
compiled with the same parameters as Python 2.4

It also requires lsprofcalltree.py that should have been bundled with it."""

import time, tempfile

from zope.app.component.hooks import setSite

from Testing.makerequest import makerequest
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager, getSecurityManager
from Acquisition import aq_base

PORTAL = "/Plone"
SKIN = '/++skin++col'

USER_URLS = [
    # (userid, path)
    (None, "/"),
    ("leo1", "/"),
]

def setupAppPortalAndAuth(app, userid):
    app = makerequest(aq_base(app))
    app.REQUEST['URL1'] = app.REQUEST['URL']
    app.REQUEST['PARENTS'] = [app]

    portal = app.unrestrictedTraverse(PORTAL) 
    setSite(portal)
    portal.setupCurrentSkin(app.REQUEST)
    if userid is None:
        noSecurityManager()
    else:
        acl_users = portal.unrestrictedTraverse("acl_users")
        newSecurityManager(app.REQUEST,
                           acl_users.getUserById(userid).__of__(acl_users))
    app.REQUEST['AUTHENTICATED_USER'] = getSecurityManager().getUser()
    return app

#outdir = tempfile.mkdtemp()
#print "profiling output at:", outdir

for i, (userid, path) in enumerate(USER_URLS):
    # throw the cache out
    app._p_jar.cacheMinimize()

    app = setupAppPortalAndAuth(app, userid)
    print "\ntiming path", path, "with user", userid
    print "starting cache size:", app._p_jar._db.cacheSize()
    # on cold cache
    # - traversal
    t0 = time.time()
    method = app.REQUEST.traverse(PORTAL + SKIN + path)
    t1 = time.time()
    # - rendering
    result = method()
    t2 = time.time()
    print "on cold cache, traversal:", t1 - t0, "rendering:", t2 - t1
    print "cache size:", app._p_jar._db.cacheSize()

    # reduce cache size to target ZODB cache size (see zope.conf)
    app._p_jar.cacheGC()
    print "adjusted cache size:", app._p_jar._db.cacheSize()
    # on warm cache
    # - traversal
    t0 = time.time()
    method = app.REQUEST.traverse(PORTAL + SKIN + path)
    t1 = time.time()
    # - rendering
    result = method()
    t2 = time.time()
    print "on warm cache, traversal:", t1 - t0, "rendering:", t2 - t1
    print "cache size:", app._p_jar._db.cacheSize()


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

import os
import sys
import tempfile

import transaction
from zope.app.component.hooks import setSite
from ZODB.utils import serial_repr
from AccessControl.SecurityManagement import newSecurityManager
from DateTime.DateTime import DateTime

from Products.COL3 import config

try:
    from os import link
except ImportError:
    # appease Windows
    from shutil import copyfile as link

# name of the manifest file within the scan structure
MANIFEST = 'MANIFEST'

REPORT_HEADER = """
Report from virus scan run:
---------------------------
""".strip()

def getPortal(app, portal_path):
    portal = app.unrestrictedTraverse(portal_path, None)
    if portal is None:
        return
    portal.setupCurrentSkin(portal.REQUEST)
    newSecurityManager(None, portal.getWrappedOwner())
    setSite(portal)
    return portal

def do_prepare(portal, scandir=None):
    # we assume the temporary directory is in the same partition as the blob
    # storage, as configured by default by buildout
    d = tempfile.mkdtemp()
    manifest = open(os.path.join(d, 'MANIFEST'), 'w')
    paths = [rec.getPath()
             for rec in portal.portal_catalog(portal_type=config.SCAN_TYPES)]
    paths.sort()
    for i, path in enumerate(paths):
        # minimize the cache every now and then
        if not i % 500:
            portal._p_jar.cacheMinimize()

        fileobj = portal.unrestrictedTraverse(path)
        blobWrapper = fileobj.getFile()
        blob = blobWrapper.getBlob()
        
        path = fileobj.getPhysicalPath()[1:] # drop the initial /
        filename = blobWrapper.getFilename()
        linksource = blob.committed()
        if filename:
            filename = filename.replace(' ','-')
            # Use try-except to test whether filename need unicode conversion
            try:
                str(filename)
            except UnicodeEncodeError:
                # Yes, it does
                print "original filename contains unicode characters: ", fileobj.virtual_url_path(), filename
                try:
                    filename = filename.encode('latin1') 
                except UnicodeEncodeError:
                    # Okay...
                    filename = filename.encode('utf-8')
            relpath = os.path.join(*(path + (filename,)))
            relpath = relpath.replace(' ','-')
            linktarget = os.path.join(d, relpath)
            os.makedirs(os.path.dirname(linktarget))
            link(linksource, linktarget)
            print >> manifest, '|'.join((relpath, serial_repr(blob._p_serial)))
        else:
            print "Filename missing for ", fileobj.virtual_url_path()

    if scandir is None:
        date = DateTime()
        scandir = os.path.join(os.path.dirname(d),
                               date.ISO().replace(' ','_').replace(':','.'))
    manifest.close()
    os.rename(d, scandir)
    print "Generated scan structure at:", scandir
    return scandir

def do_report(portal, scandir):
    changes = False
    manifest = open(os.path.join(scandir, MANIFEST))
    report = open(os.path.join(scandir, 'report.txt'), 'w')
    print >> report, REPORT_HEADER
    portalpath = "/".join(portal.getPhysicalPath())
    for i, entry in enumerate(manifest):
        # minimize the cache every now and then
        if not i % 500:
            portal._p_jar.cacheMinimize()

        relpath, serial = entry.strip().rsplit('|', 1)
        dirname, _filename = os.path.split(relpath)
        contentpath = "/" + dirname.replace(os.path.sep, '/')
        # does the structure match the manifest?
        assert os.path.isdir(os.path.join(scandir, dirname))
        # is it inside the portal?
        assert contentpath.startswith(portalpath)
        content = portal.unrestrictedTraverse(contentpath,
                                              None)
        if (content is None or
            "/".join(content.getPhysicalPath()) != contentpath):
            print >> report, contentpath +': content no longer exists'
            if content is not None:
                print >> report, "/".join(content.getPhysicalPath()), contentpath
            continue
        blob = content.getFile().getBlob()
        blob.committed()
        current_serial = serial_repr(blob._p_serial)
        if (content.portal_type not in config.SCAN_TYPES or
            current_serial != serial):
            print >> report, (contentpath +
                              ': content updated since scan (%s, %s)' % (serial, 
                                                                         current_serial))
            continue
        if not os.path.exists(os.path.join(scandir, relpath)):
            # XXX: do something here to the infected content
            # set 'changes' to True if content was changed
            print >> report, contentpath + ': infected!'
            continue # kind of useless, but just to keep simmetry

    manifest.close()
    report.close()
    if changes:
        tr = transaction.get()
        tr.note('Applied changes due to detected viruses')
        tr.commit()
    return report.name

def help():
    print """
Usage:
%s prepare <path-to-portal> [scandir],
or
%s report <path-to-portal> <scandir>
e.g.,
\t%s prepare ConserveOnline /usr/local/www/col3/virusscan
    """.strip() % (sys.argv[0], sys.argv[0], sys.argv[0])

def main(app):
    from Testing.makerequest import makerequest
    app=makerequest(app)

    args = sys.argv[1:]
    if len(args) < 2 or len(args)>3:
        return help()
    scandir = None
    if len(args)==3:
        scandir = args.pop()
    elif args[0]=='report':
        print "You must include a scandir arg on which to report"
        return help()
    portal = getPortal(app, args.pop())
    if portal is None:
        return help()
    cmd = globals().get('do_' + args.pop())
    if cmd is None:
        return help()
    return cmd(portal, scandir)

if __name__ == "__main__":
    main(app) #@UndefinedVariable

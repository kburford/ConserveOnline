import logging
import sys, os
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import setSite
from Products.CachedGSAIndexer.config import TOOL_NAME

if __name__=='__main__':
    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest
    app=makerequest(app)
    plonesite="ConserveOnline"
    if len(sys.argv)>1:
        plonesite=sys.argv[1]
    portal = app.unrestrictedTraverse(plonesite)
    setSite(portal)
    newSecurityManager(None, portal.getWrappedOwner())
    gt = getToolByName(portal, TOOL_NAME)
    print "CachedGSAIndexer tool properties: "
    for p,v in gt.getToolProps().items():
      print p, ":",v

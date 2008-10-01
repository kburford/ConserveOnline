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

from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName

def install(self):
    out = StringIO()
    print >> out, "setting up Ploneboard"
    # Apply the Ploneboard and COL3 profiles
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.setImportContext('profile-Products.Ploneboard:ploneboard')
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext('profile-COL3:default')
    setup_tool.runAllImportSteps()

    return out.getvalue()

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
from Acquisition import aq_inner
from zope.component import getMultiAdapter
#from zope.app.traversing.browser.interfaces import IAbsoluteURL

from Products.COL3.etree import tostring
from Products.CMFCore.utils import getToolByName

from Products.COL3 import config

def toStringWithPreamble(xmlElement):
    xmlElementStr = tostring(xmlElement)
    return ("<?xml version='1.0' encoding='%s'?>\n" % config.CHARSET +
            xmlElementStr)

def strip(str):
    try:
        return str.strip()
    except AttributeError:
        return str

def getBaseUrl(context, request, postfix=True):
    ptool = getToolByName(context, 'portal_url')
    portal = aq_inner(ptool.getPortalObject())
#    url = str(getMultiAdapter((portal, request), IAbsoluteURL))
    url = portal.absolute_url()
    if postfix and not url.endswith('/'):
        url = url + '/'
    return url

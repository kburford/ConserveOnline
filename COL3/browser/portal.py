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

from xml.parsers.expat import ExpatError
from Products.COL3.etree import Element, SubElement, fromstring

from zExceptions import Redirect
from AccessControl.SecurityManagement import getSecurityManager
from zope.interface import Interface
from zope.app.component.hooks import getSite
from Products.CMFCore import utils as cmfutils
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.ploneview import Plone

from Products.COL3.browser.base import Page, Fragment
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.config import NATIONS
from Products.COL3.browser.common import cleanup
from Products.COL3 import config

class WorkspacesByCountryPortletFragment(Fragment):
    """ Returns a list of the countries with the most workspaces """
    def asElement(self):
        items = []
        root = Element('portlet',
                       type='mostworkspaces',
                       title='Most Workspaces')
        context = self.context
        pcat = getToolByName(context, 'portal_catalog')
        countries = pcat.uniqueValuesFor('getWorkspaceCountry')
        url = context.absolute_url() + '/workspaces/withcountry-workspaces.html?country=%s'

        # No need to merge results or recompute url outside of token 
        for country in countries:
            if not country:
                continue 
 
            count = len(pcat.searchResults(portal_type='Workspace',
                                           getWorkspaceCountry=country,
                                           _merge=False))
            items.append({'href': url % country,
                          'country':NATIONS.getTermByToken(country).title, 
                          'count':count})

        items.sort(key = lambda a: a['count'], reverse=True)
        for item in items[:7]:
            resource = SubElement(root, 'resource', href=item['href'])
            SubElement(resource, 'title').text = item['country']
            SubElement(resource, 'count').text = str(item['count'])
        return root



class PortalViewFragment(Fragment):
    """<view name="view.html" type="colhome" title="ConserveOnline Home Page" section="home"/>"""
    def asElement(self):
        return Element('view',
                       name='view.html',
                       type='colhome',
                       title='ConserveOnline Home Page',
                       section='home')

class NewDocInLibraryPortletFragment(Fragment):
    """ latest docs in lib """
    def asElement(self):
        root = Element('portlet',
                       type='recentlypublished',
                       title='Recently Published Documents')
        portalcatalog = cmfutils.getToolByName(self.context, 'portal_catalog')
        libraryfiles =  portalcatalog(object_provides='Products.COL3.interfaces.library.ILibraryFile',
                                      sort_on='created',
                                      sort_order='reverse',
                                      sort_limit=5)[:5]
        for libraryfile in libraryfiles:
            elem = Element('resource', href=libraryfile.getURL())
            SubElement(elem, 'title').text = libraryfile.Title
            root.append(elem)
        return root

class NewWorkspacesPortletFragment(Fragment):
    """ most recent workspaces portlet fragment to display in homepage right colummn"""
    def asElement(self):
        root = Element('portlet',
                       type='newworkspaces',
                       title='New Workspaces')
        context = self.context
        pcat = cmfutils.getToolByName(context, 'portal_catalog')
        workspaces = pcat.searchResults(portal_type='Workspace',
                                        sort_on='created',
                                        sort_order='reverse',
                                        sort_limit=5)[:5]
        for workspace in workspaces:
            resource_elem = SubElement(root, 'resource', href=workspace.getURL())
            SubElement(resource_elem, 'title').text = workspace.Title
            creation_date = workspace.created.ISO8601()
            SubElement(resource_elem, 'created').text = creation_date
        return root

class PortalPortletsFragment(Fragment):
    """ This is here to assemble the portlet fragments for display on the portal homepage """
    def asElement(self):
        ctx = self.context
        req = self.request
        root = Element('portlets')
        newdocportlet = NewDocInLibraryPortletFragment(ctx, req)
        newworkgroupsportlet = NewWorkspacesPortletFragment(ctx, req)
        workspacesbycountry = WorkspacesByCountryPortletFragment(ctx, req)
        root.append(newdocportlet.asElement())
        root.append(newworkgroupsportlet.asElement())
        root.append(workspacesbycountry.asElement())
        return root

class COLConfigFragment(Fragment):
    """ A Fragment with consolidated information for display on the portal home page"""
    def asElement(self):
        context = self.context
        colConfig = context.about['homepageconfig']

        root = Element('colhome')

        #sideimage section of colhome block
        image_url='#'
        if colConfig.getRefs('ReferenceToImageOne'):
            image_url = colConfig.getRefs('ReferenceToImageOne')[0].absolute_url()
        sideimageelem = SubElement(root, 'sideimage', href=colConfig.getSideimageoneurl())
        SubElement(sideimageelem, 'img', title='title', href=image_url)

        image_url='#'
        if colConfig.getRefs('ReferenceToImageTwo'):
            image_url = colConfig.getRefs('ReferenceToImageTwo')[0].absolute_url()
        sideimageelem = SubElement(root, 'sideimage', href=colConfig.getSideimagetwourl())
        SubElement(sideimageelem, 'img', title='title', href=image_url)

        image_url='#'
        if colConfig.getRefs('ReferenceToImageThree'):
            image_url = colConfig.getRefs('ReferenceToImageThree')[0].absolute_url()
        sideimageelem = SubElement(root, 'sideimage', href=colConfig.getSideimagethreeurl())
        SubElement(sideimageelem, 'img', title='title', href=image_url)

        #featured workspace section of homepage
        featured_workspace_url='#'
        featured_image_url='#'
        if colConfig.getRefs('RefersToTheFeaturedWorkspace'):
            featured_workspace_url = colConfig.getRefs('RefersToTheFeaturedWorkspace')[0].absolute_url()
        if colConfig.getRefs('RefersToTheFeaturedImage'):
            featured_image_url = colConfig.getRefs('RefersToTheFeaturedImage')[0].absolute_url()

        featureelem = SubElement(root, 'feature', href=featured_workspace_url)
        SubElement(featureelem, 'img', title='title', href=featured_image_url)
        textnode = cleanup(colConfig.getRawFeaturecontent())
        SubElement(featureelem, 'text').append(textnode)
        return root

    def _createTextNode(self, text):
        try:
            return fromstring(text)
        except ExpatError:
            div = Element('{http://www.w3.org/1999/xhtml}div')
            div.text = text
            return div

class PortalView(Page):
    """ View class for the portal itself """
    views = (PortalViewFragment,
             COLConfigFragment,
             PortalPortletsFragment,) + COMMON_VIEWS

class IAboutFolder(Interface):
    """ Simple marker interafce for the about folder """

class AboutView(BrowserView):
    """ Simple view to redirect to the about page if the about folder is clicked """
    def __call__(self):
        context = self.context
        raise Redirect(context.absolute_url()+'/aboutus')

class PloneBlocker(Plone):

    def globalize(self):
        """ Override Products.CMFPlone.browser.ploneview.Plone.globalize() to
        bail out with a NotFound error, since we do not want the Plone
        interface to be visible from the XSLT rendered URL space """
        # This commented-out block does not work due to deep stack manipulation
        # magick in the original globalize().
        #u = getSecurityManager().getUser()
        #if u.hasRole('Manager'):
        #    return super(PloneBlocker, self).globalize()
        self.request.response.notFoundError(entry=self.request['URL'])


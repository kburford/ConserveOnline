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

from Products.COL3.search.GoogleWrapper import GoogleWrapper
import logging
import urllib2
from enfold.gsa import gsa
from xml.parsers.expat import ExpatError

from Products.COL3.etree import Element, SubElement
from Products.COL3.etree import fromstring

from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.gsa_config import GSA_HOST
from Products.COL3 import config
from Products.COL3.config import GSA_SEARCH_FOLDERS as searchfolders

class SearchQueryViewFragment(Fragment):
    """ 
    This fragment encapsulates the search criteria the user submitted.
    We also need to provide the url since we need to retain the 'context'
    when you search inside a workspace.

    XXX url and locurl are same?
    <searchquery>
        <url>http://path/to/search</url>
        <terms>words searched on</terms>
        <locurl>http://host/path/to/filter/on</locurl>
        <loclabel>All Site</loclabel>
    <searchquery>
    """

    def asElement(self):
        """
           <option value="config.DEFAULT_QUERY_COLLECTION">All Site</option> <- default collection from config
           <option value="library"> Library </option>
           <option value="workspace"> All Workspaces </option>
           <option value="ConservationWebsites"> Conservation Sites </option>
           <option value="GIS"> GIS Portal Content </option>
        """
        _terms = None
        _locurl = None
        _loclabel = None
        request = self.request 
        serverurl = request['SERVER_URL']
        _url = serverurl + '/search'
        q = request.get('q')
        site = request.get('site')
        getfields = request.get('getfields')
        requiredfields = request.get('requiredfields')
        collections = set(config.GSA_COLLECTIONS)
        default_collection = config.DEFAULT_QUERY_COLLECTION
        default_collection_set = set((default_collection,))
        folders = {'workspace':'All Workspaces', 
                   'library':'Library'}
        if requiredfields:
            requiredfields =  requiredfields.split(':')
        if q:
            _terms = ' '.join([t for t in q.split() if not t.startswith('site')])
            _locurl = ''.join([t for t in q.split() if t.startswith('site')])
            if not _locurl:
                _locurl = request.get('site')
                if _locurl and _locurl.endswith('/'):  # normalize
                    _locurl=_locurl[:-1]
                    _url = _locurl + '/search'
            #basically running through all the possible query string parameters used
            #in filtered searches that are used by the backend
            if site and site in collections.difference(default_collection_set): #one of the two external collections
                _loclabel = site
            elif requiredfields and requiredfields[len(requiredfields)-1]: #in the query string this is workspace:'Name of Workspace'
                _loclabel = 'This Workspace'
            elif site and site in searchfolders: #dropdown box passed in worksacpe and library as "site"
                _loclabel = folders[site]
            elif getfields and getfields in searchfolders: #getfield is the same as name portion of the required fields param
                _loclabel = folders[getfields]
            elif site == default_collection: #exhausted all possibilties, All Site realy refers to everything in the default collection with no filters
                _loclabel = 'All Site'
            else:
                _loclabel = 'This Workspace'      
        request = self.request
        elem = Element('searchquery')
        url = SubElement(elem, 'url') 
        url.text = _url
        terms = SubElement(elem, 'terms')
        terms.text = _terms
        locurl= SubElement(elem, 'locurl')
        locurl.text = _locurl
        loclabel = SubElement(elem, 'loclabel')
        loclabel.text = _loclabel
        return elem

class SearchResultsViewFragment(Fragment):
    def _computeSection(self):
        request = self.request

        actual = request['ACTUAL_URL']
        if 'library' in actual:
            return 'library'
        if 'workspaces' in actual:
            return 'workspaces'
        return ''

    def asElement(self):
        section = self._computeSection()
        return Element('view',
                       name='gsa.html',
                       type='gsa',
                       title='ConserveOnline Search Results',
                       section=section)

class GSAResultsViewFragment(Fragment):
    """ The front end will be passing back  a value from the dropdown list on the
        search box which will either be:
        
        1) A collection name
        2) The name of a folder from which all results should come
        3) The name of a particular workspace from which all results should come
        
        The code below isn't beautiful but in order to determine how to construct the
        query we need to:
        
        1) See if the value is in the list of collections, if so, instantiate the GSA
           object with that value
        2) If it's not in collections, see if the value is one of the folders we're interested
           in, if so, add the foldername to the metadata on the query
        3) If neither 1 or 2 is true, assume this is the name of a workspace and add it
           to the metadata accordingly
    """
    def asElement(self):
        request = self.request
        user_query = request.get('q', '')
        start = int(request.get('start', 0))
        searchfilter = request.get('site')
        requiredfields = request.get('requiredfields')
        filter = (searchfilter in config.GSA_COLLECTIONS) and searchfilter or config.DEFAULT_QUERY_COLLECTION
        app = gsa.GSA(GSA_HOST, filter)
        query = app.createQuery(user_query)
        query.setDuplicateDirectoryFilter(False)
        query.setDuplicateSnippetFilter(False)
        query.setStartRecord(start)
        if searchfilter and searchfilter not in config.GSA_COLLECTIONS:
            #if the search filter is to search the workspaces or library folders
            #then we need to search on the "library" or "workspace" meta tag, which
            #translates to "inmeta:foldername" in the query string
            if searchfilter in config.GSA_SEARCH_FOLDERS:
                query.addMeta(searchfilter, '')
            #if the search filter is to search the a particular workspace
            #then we need to search on the "workspace" meta tag with the searchfilter
            #as the value which translates to "inmeta:workspace~nameofworkspace" in 
            #the query string
            else:
                query.addMeta('workspace', searchfilter)
        if requiredfields:
            namevalue = requiredfields.split(':')
            fieldname = namevalue[0]
            fieldvalue = len(namevalue)>1 and namevalue[1] or ''
            query.addMeta(fieldname, urllib2.unquote(fieldvalue)) 
        try:
            socket = app.query(query, xml=True)
            results = socket.read()
            node = fromstring(results)
        except gsa.GSAException, gsae:
            error = '%s%s%s' % (gsae.__class__.__name__, ":", str(gsae))
            logger = logging.getLogger('COL3.browser.search') 
            logger.error('***** '+error+' *****')
            node = Element('GSP')
        return node

class GoogleSearchResultsFragment(Fragment):
    """ This does a search against google and returns the top five results """
    def asElement(self):
        root = Element('portlets')
        portletelem = SubElement(root, 
                                 'portlet', 
                                 type="googlecomresults", 
                                 title="Google Search")
        user_query = self.request.get('q', '')
        googlewrapper = GoogleWrapper()
        results = googlewrapper.doQuery(user_query, numresults=5)
        try:
            resultstree = fromstring(results.xml)
            resultnodes = resultstree.findall('results/result')
            for resultnode in resultnodes:
                portletelem.append(resultnode)
        except ExpatError: #this means the results are empty
            pass
        return root
        
class SearchResultsPage(Page):
    views = (SearchResultsViewFragment, 
             GoogleSearchResultsFragment, 
             SearchQueryViewFragment, 
             GSAResultsViewFragment) + COMMON_VIEWS

    def __init__(self, context, request):
        self.xtra_breadcrumb_ids = ({'title':u'Search Results',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        super(SearchResultsPage, self).__init__(context, request)


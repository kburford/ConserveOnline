import logging
from urllib import quote_plus
from datetime import datetime

from Acquisition import aq_inner, aq_parent #@UnresolvedImport
from zope.interface import implements, Interface
from Products.COL3.etree import Element, SubElement #@UnresolvedImport

from Products.CMFCore.utils import SimpleItemWithProperties

from Products.COL3.browser.common import BaseBatchFragment, TraversableView
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.browser.batch import BatchProvider, BatchFragmentFactory
from Products.COL3.browser.base import Fragment, Page
from Products.COL3.browser.utils import strip
from Products.COL3.config import NATIONS
from Products.COL3.browser.base import ResultSet

class PersonObj(SimpleItemWithProperties):
    """ The indexed person object """
    _properties = (
                   dict(id='userid', type='string', mode='w'),
                   dict(id='firstname', type='string', mode='w'),
                   dict(id='lastname', type='string', mode='w'),
                   dict(id='country', type='string', mode='w'),
                   dict(id='organization', type='string', mode='w'),
                  )

    def __init__(self, userId, firstname, lastname, country, organization):
        self.userid = userId
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.organization = organization

    def getPhysicalPath(self):
        return ('people', 'person', self.userid,)

class IPeople(Interface):
    """ Interface for people view to register a default view against in zcml"""

class People(TraversableView):
    """ The entry point for people browsing """
    portal_type='People'
    implements(IPeople)

class BrowsePeopleMenuFragment(Fragment):
    """ the menus items for the doc browser page"""
    """ Menu fragment for topic list view """

    _utilmenu_items = ()

    def asElement(self):
        context = aq_parent(aq_inner(self.context))
        url = context.absolute_url()
        self._utilmenu_items = self._generateUtilMenu(url)
        menu_tag = Element('menus')
        # loop through all action menus, appending them if the user has
        # permission
        url = context.absolute_url()
        if self._utilmenu_items:
            utilmenu = SubElement(menu_tag, 'utilitymenu', label="By:")
            for label, url in self._utilmenu_items:
                elem = SubElement(utilmenu, 'entry', href=url)
                elem.text = label
                if self._isSelected(label, self.request):
                    elem.attrib['current'] = 'current'
        return menu_tag

    def _generateUtilMenu(self, url):
        return ((u'All',url + '/people/all.html',),
                (u'Regions/Countries', url + '/people/bycountry.html',),
                (u'Organizations', url + '/people/byorganization.html'),)

    def _isSelected(self, label, request):
        pages = {'all.html':'All',
                 '@@all.html':'All',
                 'bycountry.html':'Region/Countries',
                 'byorganization.html':'Organizations',}
        url = request.get('URL').split('/')
        url.reverse()
        return pages.has_key(url[0]) and pages[url[0]] == label

####################################################################################
##                            Begin BrowseAllPeople                               ##
####################################################################################

class BrowseAllPeopleViewFragment(Fragment):
    def asElement(self):
        return Element('view',
                       name='all-people.html',
                       type='people',
                       title='Browse All People',
                       section='people')

class BrowseAllPeopleBatchProvider(BatchProvider):
    """ Batch provider that gets all the results from the people catalog """
    def query(self, params):
        prop_dict = {}
        items = []
        member_propnames = ['lastname', 'firstname', 'organization', 'country']
        context = aq_parent(aq_inner(self.context))
        request = self.request
        startswith = ''
        sort_on='lastname'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if request.get('startswith'):
            startswith = request.get('startswith').lower()+'*'
        people = context.people_catalog.searchResults(sort_on=sort_on,
                                                      lastname_user=startswith)
        querystr = context.absolute_url()+'/view-profile.html?userid=%s'
        for person in people: #None Given here so tests will pass, test_user_1 is missing values
            for propname in member_propnames: #this is so tests would pass...default test user is missing some props
                                              #also, organization is optional so this catchall will account for that as well @IndentOk
                prop_dict[propname] = getattr(person, propname, None) or 'None Given'
            if startswith: #we need to make sure the first letter of the last name matches the letter to match on selected
                if prop_dict['lastname'].lower().startswith(startswith[:1].lower()):
                    items.append({'href': querystr % person.userid,
                                  'lastname':prop_dict['lastname'],
                                  'firstname':prop_dict['firstname'],
                                  'organization':prop_dict['organization'],
                                  'country':prop_dict['country']})
            else:
                items.append({'href': querystr % person.userid,
                              'lastname':prop_dict['lastname'],
                              'firstname':prop_dict['firstname'],
                              'organization':prop_dict['organization'],
                              'country':prop_dict['country']})
        logger = logging.getLogger('Products.COL3.browser.people')
        start = datetime.now()
        #logger.info('***** Started people sort at - '+start.strftime('%X *****'))
        items.sort(lambda a, b: cmp((a.get(sort_on)).lower(), (b.get(sort_on)).lower()))
        end = datetime.now()
        #logger.info('***** People sorting ended at '+end.strftime('%X *****')+' and took '+str((end-start).seconds)+' seconds')
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class BrowseAllPeopleBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch_provider defined below """
    def asElement(self):
        context = self.context
        request = self.request
        columns = (('lastname', {'default_order':'asc',
                                 'label': 'Last Name'}),
                  ('firstname', {'default_order':'asc',
                                 'label': 'First Name'}),
                  ('organization', {'default_order':'asc',
                                    'label': 'Organization'}),
                  ('country', {'default_order':'asc',
                               'label': 'Region/Country'}),)
        batchfragment = BatchFragmentFactory(BrowseAllPeopleBatchProvider,
                                             columns = columns,
                                             letters_param='startswith')
        if request.get('sort_on', None) is None:
            request['sort_on'] = 'lastname'
        batch = batchfragment(context, request)
        retbatch = batch.asElement()
        return retbatch

class BrowseAllPeoplePage(Page):
    """ """
    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'Browse All People',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(BrowseAllPeoplePage, self).getResponse()

    views = (BrowseAllPeopleViewFragment,
             BrowsePeopleMenuFragment,
             BrowseAllPeopleBatchFragment) + COMMON_VIEWS

####################################################################################
##                             End BrowseAllPeople                                ##
####################################################################################

####################################################################################
##                         Begin BrowsePeopleByCountry                            ##
####################################################################################

class BrowsePeopleByCountryViewFragment(Fragment):
    def asElement(self):
        return Element('view',
                       name='bycountries-people.html',
                       type='people',
                       title='Browse People By Regions/Countries',
                       section='people',)

class BrowsePeopleByCountryBatchProvider(BatchProvider):
    """ Batch provider that gets all the results from the people catalog """
    def query(self, params):
        items = []
        sort_on='country'
        context = aq_parent(aq_inner(self.context))
        people_catalog = context.people_catalog
        countries = people_catalog.uniqueValuesFor('country')
        total = len(countries)
        countries = list(countries)
        countries.sort()
        countries = countries[params['start']:params['end']]
        url = context.absolute_url() + '/people/withcountry-people.html?name='
        for country in NATIONS._terms:
            if country.value in countries:
                count = 0
                results = people_catalog.searchResults(_merge=False,
                                                                                country=country.token)
                for results in results:
                    count += 1
                items.append({'count': count,
                                         'href': url + quote_plus(country.token),
                                         'country': country.title})
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return ResultSet(items, total)

class BrowsePeopleByCountryBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch_provider defined below """
    sort_on = 'country'
    columns = (('country', {'default_order':'asc',
                            'label': 'Region/Country'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    batch_provider = BrowsePeopleByCountryBatchProvider

class BrowsePeopleByCountryPage(Page):
    """ """
    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'Browse People By Regions/Countries',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(BrowsePeopleByCountryPage, self).getResponse()

    views = (BrowsePeopleByCountryViewFragment,
             BrowsePeopleMenuFragment,
             BrowsePeopleByCountryBatchFragment) + COMMON_VIEWS

####################################################################################
##                           End BrowsePeopleByCountry                            ##
####################################################################################

####################################################################################
##                       Begin BrowsePeopleWithCountry                            ##
####################################################################################

class BrowsePeopleWithCountryViewFragment(Fragment):
    def asElement(self):
        country = self.request.get('name')
        try:
            country = NATIONS.by_token[country].title
        except Exception, e:
            error = '%s%s%s' % (e.__class__.__name__, ":", str(e))
            logger = logging.getLogger('Products.COL3.browser.people')
            logger.error('***** '+error+' *****')
        return Element('view',
                       name='withcountry.html',
                       type='people',
                       title='List People for Region/Country - '+country,
                       section='people')

class BrowsePeopleWithCountryBatchProvider(BatchProvider):
    """ Batch provider that gets all the results from the people catalog """
    def query(self, params):
        items = []
        country = strip(self.request.get('name'))
        context = aq_parent(aq_inner(self.context))
        url = context.absolute_url() + '/view-profile.html?userid='
        sort_on='lastname'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        results = context.people_catalog.searchResults(country=country,
                                                                                     sort_on=sort_on)
        for result in results:
            if len(results) > 0:
                items.append({'href':url + result.userid,
                                         'lastname':result.lastname,
                                         'firstname':result.firstname,
                              'organization':result.organization,})
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class BrowsePeopleWithCountryBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch_provider defined below """
    sort_on = 'lastname'
    columns = (('lastname',  {'default_order':'asc',
                              'label': 'Last Name'}),
               ('firstname', {'default_order':'asc',
                              'label': 'First Name'}),
               ('organization', {'default_order':'asc',
                                 'label': 'Organization'}),)
    batch_provider = BrowsePeopleWithCountryBatchProvider

class BrowsePeopleWithCountryPage(Page):
    """ """
    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'List People for Country - '+self.request.get('name'),
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(BrowsePeopleWithCountryPage, self).getResponse()

    views = (BrowsePeopleWithCountryViewFragment,
             BrowsePeopleWithCountryBatchFragment) + COMMON_VIEWS

####################################################################################
##                         End BrowsePeopleWithCountry                            ##
####################################################################################

####################################################################################
##                     Begin BrowsePeopleByOrganization                           ##
####################################################################################

class BrowsePeopleByOrganizationViewFragment(Fragment):
    def asElement(self):
        return Element('view',
                       name='byorganization-people.html',
                       type='people',
                       title='Browse People By Organization',
                       section='people',)

class BrowsePeopleByOrganizationBatchProvider(BatchProvider):
    """ Batch provider that gets all the results from the people catalog """
    def query(self, params):
        items = []
        context = aq_parent(aq_inner(self.context))
        people_catalog = context.people_catalog
        url = context.absolute_url() + '/people/withorganization-people.html?name='
        #import pdb; pdb.set_trace()
        organizations = people_catalog.uniqueValuesFor('organization')
        total = len(organizations)
        organizations = list(organizations)
        organizations.sort()
        organizations = organizations[params['start']:params['end']]
        for organization in organizations:
            results = people_catalog.searchResults(_merge = False,
                                                                            organization=organization)
            if len(results) > 0:
                #href = organization is not None and url+organization or url+'None Given'
                if organization is None:
                    organization=""
                href = organization and url+organization or url+'None Given'
                items.append({'href':href,
                                         'organization':organization,
                                        'count':len(results),})
        sort_on='organization'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        if sort_on == 'count':
            items.sort(lambda a, b: cmp(a.get(sort_on), b.get(sort_on)))
        if params.get('sort_order') == 'desc':
            items.reverse()
        return ResultSet(items, total)

class BrowsePeopleByOrganizationBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch_provider defined below """
    sort_on = 'organization'
    columns = (('organization', {'default_order':'asc',
                                 'label': 'Organization'}),
               ('count', {'default_order':'asc',
                          'label': 'Count'}),)
    batch_provider = BrowsePeopleByOrganizationBatchProvider

class BrowsePeopleByOrganizationPage(Page):
    """ """
    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'Browse People By Organizations',
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(BrowsePeopleByOrganizationPage, self).getResponse()

    views = (BrowsePeopleMenuFragment,
             BrowsePeopleByOrganizationViewFragment,
             BrowsePeopleByOrganizationBatchFragment) + COMMON_VIEWS

####################################################################################
##                      End BrowsePeopleByOrganization                            ##
####################################################################################

####################################################################################
##                    Begin BrowsePeopleWithOrganization                          ##
####################################################################################

class BrowsePeopleWithOrganizationViewFragment(Fragment):
    def asElement(self):
        return Element('view',
                       name='withorganization.html',
                       type='people',
                       title='List People for Organization - '+self.request.get('name'),
                       section='people')

class BrowsePeopleWithOrganizationBatchProvider(BatchProvider):
    """ Batch provider that gets all the results from the people catalog """
    def query(self, params):
        items = []
        context = aq_parent(aq_inner(self.context))
        request = self.request
        organization = strip(request.get('name'))
        people_catalog = context.people_catalog
        url = context.absolute_url() + '/view-profile.html?userid='
        sort_on='lastname'
        if params.get('sort_on'):
            sort_on = params.get('sort_on')
        results = people_catalog.searchResults(organization=organization,
                                               sort_on=sort_on)
        if len(results) > 0:
            for result in results:
                items.append({'href':url+result.userid,
                              'lastname':result.lastname,
                              'firstname':result.firstname,
                              'organization':result.organization,})
        if params.get('sort_order') == 'desc':
            items.reverse()
        return items

class BrowsePeopleWithOrganizationBatchFragment(BaseBatchFragment):
    """ Batch fragment that's fed by the batch_provider defined below """
    sort_on = 'lastname'
    columns = (('lastname', {'default_order':'asc',
                             'label': 'Last Name'}),
               ('firstname', {'default_order':'asc',
                              'label': 'First Name'}),
               ('organization', {'default_order':'asc',
                                 'label': 'Organization'}),)
    batch_provider = BrowsePeopleWithOrganizationBatchProvider

class BrowsePeopleWithOrganizationPage(Page):
    """ """
    def getResponse(self):
        """ Overriding to set some variables"""
        self.xtra_breadcrumb_ids = ({'title':'List People For Organization - '+self.request.get('name'),
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(BrowsePeopleWithOrganizationPage, self).getResponse()

    views = (BrowsePeopleWithOrganizationViewFragment,
             BrowsePeopleWithOrganizationBatchFragment) + COMMON_VIEWS

####################################################################################
##                      End BrowsePeopleWithOrganization                          ##
####################################################################################

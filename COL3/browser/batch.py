import string
import datetime
import operator
import Missing

from math import floor, ceil
from Products.COL3.etree import tostring #@UnusedImport
from Products.COL3.etree import Element, SubElement
from Products.COL3.etree import _ElementInterface

from ZTUtils.Zope import url_query, make_query
from ZTUtils.Batch import Batch as ZTBatch
from Products.COL3.browser.base import Fragment
from Products.COL3.browser.base import ResultSet

_marker = object()

ELEMENT_ORDERING = ['title',
                    'description',
                    'author',
                    'creator',
                    'created'
                    'modified']

PAGE_SIZES = ['10', '20', '50', '100']
DEFAULT_PAGE_SIZE = '20'

get = operator.itemgetter(0)
def order(tuple):
    try:
        return ELEMENT_ORDERING.index(get(tuple))
    except ValueError:
        return len(ELEMENT_ORDERING)

def itemAsElement(item):
    """
    We expect to receive a dictionary here, where each key is a
    top-level tag, and the value is another dictionary with possible
    attributes, were the value-dictionary 'value' key contains the
    top-level tag value.

    For example:

    >>> item = {'title': {'value': 'Living on the edge'},
    ...         'author': {'value': 'Aerosmith',
    ...                    'href': 'http://aerosmith.com'},
    ...         'created': {'value': '08/07/1992'},
    ...         }
    >>> tostring(itemAsElement(item)) #doctest:+XMLDATA
    <item>
          <title>Living on the edge</title>
          <author href="http://aerosmith.com">Aerosmith</author>
          <created>08/07/1992</created>
    </item>


    In the case where you only have simple values with no attributes
    we accept a shortcut, where you provide only the value instead of
    a dictionary.

    For example:

    >>> item = {'title': 'Living on the edge',
    ...         'author': {'value': 'Aerosmith',
    ...                    'href': 'http://aerosmith.com'},
    ...         'created': '08/07/1992',
    ...         }
    >>> tostring(itemAsElement(item)) #doctest:+XMLDATA
    <item>
          <title>Living on the edge</title>
          <author href="http://aerosmith.com">Aerosmith</author>
          <created>08/07/1992</created>
    </item>


    We also accept 'datetime' values, which will be serialized using
    the ISO8601 format.

    For example:

    >>> item = {'title': 'Living on the edge',
    ...         'author': {'value': 'Aerosmith',
    ...                    'href': 'http://aerosmith.com'},
    ...         'created': datetime.datetime(1992, 8, 7),
    ...         'modified': datetime.datetime(1992, 8, 7, 18, 5, 11),
    ...         }
    >>> tostring(itemAsElement(item)) #doctest:+XMLDATA
    <item>
          <title>Living on the edge</title>
          <author href="http://aerosmith.com">Aerosmith</author>
          <created>1992-08-07 00:00:00</created>
          <modified>1992-08-07 18:05:11</modified>
    </item>

    The following is for the case where an element contains child elements.

    For example:

    >>> item = {'title': {'value':'Living on the edge'},
    ...         'subtitles': {'children':{'subtitle':'Darkness on the Edge of Town',
    ...                                   'subtitle2':'I Love the Nightlife'}},
    ...         'author': {'value': 'Aerosmith',
    ...                    'href': 'http://aerosmith.com'},
    ...         'created': {'value':'08/07/1992'},
    ...         }
    >>> tostring(itemAsElement(item)) #doctest:+XMLDATA
    <item>
          <title>Living on the edge</title>
          <author href="http://aerosmith.com">Aerosmith</author>
          <created>08/07/1992</created>
          <subtitles>
                <subtitle>Darkness on the Edge of Town</subtitle>
                <subtitle2>I Love the Nightlife</subtitle2>
          </subtitles>
    </item>

    """
    item = item.copy() # Avoid modifying in-place.
    elm = Element('item')
    for tag, data in sorted(item.items(), key=order):
        if tag == 'href':
            elm.attrib[tag] = data
        elif isinstance(data, dict):
            if data.has_key('children'):
                assert isinstance(data['children'], dict), 'Children must be a dictionary'
                sub = SubElement(elm, tag)
                for tag in data['children'].keys():
                    childelem = SubElement(sub, tag)
                    childelem.text = data['children'][tag]
            else:
                assert data.has_key('value'), 'Must provide value'
                v = data['value']
                del data['value']
                sub = SubElement(elm, tag, **data)
                sub.text = v
        elif isinstance(data, _ElementInterface): #XXX Need this here, can't append text nodes with
            elm.append(data)                      #XXX div tags and markup
        else:
            if isinstance(data, (str, unicode)):
                pass
            elif isinstance(data, bool):
                data = str(data).lower()
            elif isinstance(data, (datetime.date, datetime.datetime,
                                   int, long, float)):
                data = str(data)
            elif data==None or data==Missing.Value:
                data = ""
            else:
                raise ValueError(
                    "Don't know how to serialize %s (%s) - tag(%s)" %
                    (repr(data), type(data), tag))
            sub = SubElement(elm, tag)
            sub.text = data
    return elm

class BatchFragment(Fragment):

    pagesize = DEFAULT_PAGE_SIZE 
    size = int(DEFAULT_PAGE_SIZE)
    provider = None
    letters_param = 'title'
    fulltext_param = 'query'
    params_to_remove = ()

    columns = (('title', {'default_order':'asc','label': 'Title'}),
               ('type', {'default_order':'asc','label': 'Type'}),
               ('author', {'default_order':'asc','label': 'Author'}),
               ('created', {'default_order':'desc','label': 'Created'}),
               ('modified', {'default_order':'desc','label': 'Date'}),)

    def cleanupParams(self, q, remove=()):
        for key in set(remove) & set(self.params_to_remove):
            if q.has_key(key):
                del q[key]
        if q.has_key('end'):
            del q['end']
        if q.has_key('size'): # and q['size'] == self.size:
            del q['size']
        for key in q.keys():
            if q[key] is None:
                del q[key]
        return q

    def computeParams(self):
        params = {}

        # Fetch basic params from the request
        for pname in ('sze', 'start', 'page', 'sort_on', 'sort_order', 'startswith'):
            value = self.request.get(pname, _marker)
            if value is not _marker:
                params[pname] = value
        # Then fetch values that match the column names, which
        # indicate filtering the batch results
        for pname in self.columns:
            value = self.request.get(pname[0], _marker)
            if value is not _marker:
                params[pname[0]] = value

        # If 'sze' has been passed in, that's the batch size.
        self.size = int(params.get('sze', self.size) == 'All' and -1 or params.get('sze', self.size))

        # If a 'page' has been passed in, then we compute the start as
        # the offset in 'batches'.
        if params.has_key('page'):
            params['start'] = self.size * (int(params['page']) - 1)
        else:
            # Otherwise, we look for a 'start' argument.
            params['start'] = int(params.get('start', 0))

        # bounds-check
        start = int(params['start'])
        params['start'] = start>=0 and start or 0

        # The end is always computed as relative to the current start,
        # no matter if we are doing pagination or not. This is the end
        # of the current batch, not the result set size.
        params['end'] = params['start'] + self.size

        # If a 'sort_on' has been passed in, that's the 'index' to
        # sort on. Defaults to no sorting.
        params['sort_on'] = params.get('sort_on', None)

        # Sort in ascending/descending order.
        params['sort_order'] = params.get('sort_order', None)

        return params

    def info(self, params, results):
        start = params['start']
        end = params['end']
        total = len(results)
        if params.has_key('sze'):
            size = params['sze']
        else:
            size = self.size 

        # bounds-check
        start = (start < 0) and 0 or start
        start = (start >= total and total != 0) and total-1 or start
        end = (end < start) and start or end
        end = (end > total) and total or end
        params['start'] = start
        params['end'] = end
        if size < 0:
            # -1 is the flag for "All'
            size = total
        pagesize = PAGE_SIZES[-1]
        for s in PAGE_SIZES:
            if s == 'All':
                continue
            if size <= int(s):
                pagesize = s
                break
        size = min(size, int(pagesize))
        self.pagesize = pagesize
        self.size = size

        next = next_first = start + size
        if next_first > total:
            next_first = total

        prev = start - 1
        if prev < 0:
            prev = 0

        prev_first = start - size
        if prev_first < 0:
            prev_first = 0


        # Compute the base url for next/previous/filter urls.
        self.request.set('URL_MARKER', '')
        omit = params.keys() + ['start', 'sort_on', 'sort_order', 'letters_param', 'sze', 'size']
        url = url_query(self.request, req_name='URL_MARKER', omit=omit)
        baseurl = self.request.get('URL', '')

        data = {'total': total,
                'start': start + 1,
                'end'  : end,
                'size' : size}

        q = params.copy()
        if next <= total:
            local_q = q.copy()
            local_q['start'] = next_first
            local_q = self.cleanupParams(local_q)
            data['next'] = {'url': self._constructUrl(baseurl,
                                                      url ,
                                                      make_query(**local_q)),
                            'label': 'Next'}

        if prev != 0:
            local_q = q.copy()
            local_q['start'] = prev_first
            local_q = self.cleanupParams(local_q)

            data['prev'] = {'url': self._constructUrl(baseurl,
                                                      url ,
                                                      make_query(**local_q)),
                            'label': 'Previous'}

        data['cols'] = cols = []
        col_defs = self.columns
        sort_order = params.get('sort_order', None)
        sort_on = params.get('sort_on', None)
        if sort_order is None:
            col_defs_dict = dict(col_defs)
            col = col_defs_dict.get(params['sort_on'], {})
            sort_order = col.get('default_order', 'asc')
        else:
            sort_order = sort_order in ('asc',) and 'asc' or 'desc'

        for col_id, col in col_defs:
            local_q = q.copy()
            local_q['start'] = params['start']
            local_q['sort_on'] = col_id
            selected = col_id == sort_on
            if selected:
                # If it's the currently-selected item, invert the
                # sort-order for the URL, so that when you click on it
                # it reverses the sorting.
                col_order = sort_order
                if col_order in ('asc',):
                    col_order = 'desc'
                else:
                    col_order = 'asc'
            else:
                col_order = col.get('default_order', 'asc')
            local_q['sort_order'] = col_order
            local_q = self.cleanupParams(local_q)
            localurl = self._constructUrl(baseurl, url, make_query(**local_q))
            cols.append(
                {'url': localurl,
                 'id': col_id.lower(),
                 'label': col['label'],
                 'selected': selected,
                 'order': col_order})

        data['pages'] = pages = []
        npages = int(ceil(len(results) / float(self.size))) + 1
        current_page = int(floor((params['end'] - 0.1) / self.size)) + 1
        for page in  xrange(1, npages):
            local_q = q.copy()
            local_q['start'] = (page - 1) * self.size
            local_q = self.cleanupParams(local_q)
            #local_q['end'] = int(local_q['start']) + self.size
            #local_q['size'] = self.size
            localurl = self._constructUrl(baseurl, url, make_query(**local_q))
            pages.append(
                {'url': localurl,
                 'label': page,
                 'current': page == current_page})

        # Add pagesize: number of items per page
        data['sizes'] = sizes = []
        for sze in PAGE_SIZES:
            local_q = q.copy()
            local_q = self.cleanupParams(local_q, ('sze'))
            local_q['sze'] = sze
            localurl = self._constructUrl(baseurl, url, make_query(**local_q))
	    sizes.append(
                {'url': localurl,
                 'label': sze,
                 'current': sze == self.pagesize })
 
        letters_param = self.letters_param
        if letters_param != 'REMOVE':
            data['letters'] = letters = []
            for letter in string.ascii_uppercase:
                local_q = q.copy()
                local_q[letters_param] = letter
                local_q = self.cleanupParams(local_q, ('start',))
                current = params.get(letters_param, '') == local_q[letters_param]
                # 'start' applies only to current letter; should be 0 for any other letters
                qtemp = local_q
                if not current:
                    qtemp['start']=0
                localurl = self._constructUrl(baseurl, url, make_query(**qtemp))
                letters.append(
                    {'url': localurl,
                     'label': letter,
                     'current': current})
        return data

    def _constructUrl(self, baseurl, url, query):
        if url == '?':
            return '%s%s%s' % (baseurl, url, query)
        else:
            return '%s%s&%s' % (baseurl, url, query)

    def asElement(self):
        params = self.computeParams()
        provider = self.provider(self.context, self.request)

        # Compute the result, based on the params informed.
        results = provider.query(params)

        # Compute some information for display, like what pages,
        # next/previous link, etc.
        info = self.info(params, results)

        batch = Element('batch')
        for attrib in ('total', 'start', 'end', 'current',
                       'query', self.fulltext_param):
            if info.has_key(attrib):
                if attrib == self.fulltext_param:
                    # Full text param if present is always stored
                    # under 'query' attribute of the batch element.
                    attrib = 'query'
                batch.attrib[attrib] = str(info[attrib])

        if info.has_key('cols') and info['cols']:
            cols = SubElement(batch, 'cols')
            for entry in info['cols']:
                col = SubElement(cols, 'col')
                col.attrib['id'] = entry['id']
                col.attrib['href'] = entry['url']
                if entry['selected']:
                    col.attrib['dir'] = entry['order']
                col.text = entry['label']

        if info.has_key('pages') and info['pages']:
            pages = SubElement(batch, 'pages')
            for entry in info['pages']:
                page = SubElement(pages, 'page')
                page.attrib['href'] = entry['url']
                if entry['current']:
                    page.attrib['current'] = 'current'
                page.text = str(entry['label'])

        if info.has_key('letters'):
            letters = SubElement(batch, 'letters')
            for entry in info['letters']:
                letter = SubElement(letters, 'letter')
                letter.attrib['href'] = entry['url']
                if entry['current']:
                    letter.attrib['current'] = 'current'
                letter.text = entry['label']

        # Add pagesize: number of items per page
        if info.has_key('sizes'):
            pagesize = SubElement(batch, 'pagesize')
            for entry in info['sizes']:
                size = SubElement(pagesize, 'size')
                size.attrib['href'] = entry['url']
                if entry['current']:
                    size.attrib['current'] = 'current'
                size.text = str(entry['label'])

        if info.has_key('prev') or info.has_key('next'):
            navigation = SubElement(batch, 'navigation')
            if info.has_key('next'):
                next = SubElement(navigation, 'next')
                next.attrib['href'] = info['next']['url']
                next.text = info['next'].get('label', 'Next')

            if info.has_key('prev'):
                next = SubElement(navigation, 'previous')
                next.attrib['href'] = info['prev']['url']
                next.text = info['prev'].get('label', 'Previous')

        # sliced is old style results
        # ResultSet is 'new style' & optimized
        sliced = results[params['start']:params['end']]
        if isinstance(results, ResultSet):
            sliced = results

        if sliced:
            items = SubElement(batch, 'items')
            for item in sliced:
                items.append(itemAsElement(item))

        #if results[params['start']:params['end']]:
        #    items = SubElement(batch, 'items')
        #    for item in results[params['start']:params['end']]:
        #        items.append(itemAsElement(item))

        if batch and len(batch.getchildren()) > 0:
            return batch
        else:
            return None

class BatchProvider(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def query(self, params=None):
        raise NotImplementedError('query')

def BatchFragmentFactory(provider, size=None,
                            params_to_remove=None,
                            columns=None,
                            letters_param=None,
                            fulltext_param=None):
    def Factory(context, request):
        batch = BatchFragment(context, request)
        batch.provider = provider
        if params_to_remove is not None:
            batch.params_to_remove = params_to_remove
        if size is not None:
            batch.size = size
        if columns is not None:
            batch.columns = columns
        if letters_param is not None:
            batch.letters_param = letters_param
        if fulltext_param is not None:
            batch.fulltext_param = fulltext_param
        return batch
    return Factory

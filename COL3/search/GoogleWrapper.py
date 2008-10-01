#!/usr/bin/python
"""
##############################################################################
#
# GoogleWrapper.py
#
# Interface to Google Web API.  Wraps google.py, Mark Pilgrim's
# Python port of the Google Web API.  Subclass of TNCSearch.
#
############################################################################## 
"""

import google
import sys
import traceback
import time
import urllib
import types

import TNCSearch as TS
import TNCResult as TR

from Products.COL3 import config

class GoogleWrapper(TS.TNCSearch):
    """
    Interface to Google API
    """
    def __init__(self, numresults=5, resultstart=0, key=''):
        """
        Create a GoogleWrapper instance.

        Arguments:
          numresults (default 5) - number of search results to capture for
            each search.
          resultstart - the number at which to start the results, first
            result is 0 (the default)
          key - optional additional Google API key to use (default '')
        """
        TS.TNCSearch.__init__(self, numresults)
        self.resultstart = resultstart
        self.keys = GoogleKeys()    # Internal keys
        if key:
            self.keys.append(key)
        self.id = "google"
        self.name = "Google Search"

    def doQuery(self, query, numresults=0, resultstart=0):
        """
        Execute a single query.  Return the results as a ResultList - a
        list of canonical search result pages (ResultPage objects).
        
        Arguments:
          query - a Query class instance (to take advantage of query syntax
            translation from another engine's syntax) or a string 
          numresults - the number of results to fetch (defaults to init setting)
          resultstart - the number at which to start the results, first
            result is 0 (the default)
        """

        # Remove comments to test without net connection.
        # __debug__ is on if -O optimizer switch is not used.
        #if __debug__:
        #    return dummyResults()

        if numresults == 0:
            numresults = self.numresults
        else:
            self.numresults = numresults

        if resultstart == 0:
            resultstart = self.resultstart
        else:
            self.resultstart = resultstart

        # Handle queries that come in as strings as well as Query instances
        import TNCQuery as TQ  # import here to prevent circular reference
        if type(query) == types.StringType:
            q = query
        elif type(query) == type(TQ.Query()):
            q = query.translate("google")
        else:
            q = ""
        
        numkeys = len(self.keys)
        
        # If exception, try the next key until none left.
        for i in range(0,numkeys):
            try:
                key = self.keys[i]
                results = google.doGoogleSearch(q, resultstart, numresults,
                                                outputencoding=config.CHARSET, 
                                                license_key=key)
            except:
                #raise #remove comment to see traceback
                if i == numkeys - 1:
                    # Tried all the keys. Give up
                    raise GoogleKeysError('No more keys')
                else:
                    # Probably maxed out key. Try the next key.
                    continue
            break   # Googled successfully. Break out of the loop.

        if results:
            results = self.__transformResults(results)
            if results:
                results.query = q
                results.engine = self.id

        return results


    def getCachedPage(self, URL):
        """
        Gets the Google cached page for the passed URL.
        """

        # Remove comments to test without net connection.
        # __debug__ is on if -O optimizer switch is not used.
        #if __debug__:
        #    return dummyText()
        
        numkeys = len(self.keys)
        for i in range(0,numkeys):
            try:
                key = self.keys[i]
                text = google.doGetCachedPage(URL, license_key=key)
            except:
                if i == numkeys - 1:
                    # Tried all the keys. Give up
                    raise GoogleKeysError('No more keys')
                else:
                    # Probably maxed out key. Try the next key.
                    continue
            break   # Googled successfully. Break out of the loop.

        # HACK: There is a bug in the Google index wherein some
        # documents can't be fetched using the Google API. This is a
        # workaround that looks for fetch failures (fetched page is
        # actually the Google "no matching docs" page) and tries a
        # conventional fetch instead. These are slower, but better
        # than no fetched doc at all.
        if text.find('- did not match any documents') > -1:
            text = None
            page = TR.ResultPage(URL)
            text = page.fetchRawPage()

	return text
         
    def spellCheck(self, phrase):
        numkeys = len(self.keys)
        answer = phrase

        # Skip check if in test mode
        #  if __debug__:
        #    return answer
        
        for i in range(0,numkeys):
            try:
                key = self.keys[i]
                answer = google.doSpellingSuggestion(phrase, license_key=key)
            except:
                if i == numkeys - 1:
                    # Tried all the keys. Give up
                    raise GoogleKeysError('No more keys')
                else:
                    # Probably maxed out key. Try the next key.
                    continue
            break   # Googled successfully. Break out of the loop.

        # Google replaces quotes with '&quot;'.
        if answer:
            answer = answer.replace('&quot;', '"')

        return answer

    def __transformResults(self, results):
        """
        Helper function to convert search result from Google format to
        TNC canonical result.  Input is a pygoogle SearchReturnValue
        instance.  This has two parts, metadata, and the list of 
        result pages.  Output is a ResultList instance.
        """
        rl = TR.ResultList()
        # Total hits
        rl.totalhits = results.meta.estimatedTotalResultsCount
        # If no hits, we're done
        if rl.totalhits < 1:
            return rl
        rl.startresult = results.meta.startIndex
        rl.endresult = results.meta.endIndex
        # Other interesting info available from Google: searchTips,
        # searchComments, list of relevant Open Directory categories
        
        # Extract ResultPage info from each google result
        i = rl.startresult
        #i = 1  # Show page rank starting at 1
        for result in results.results:
            page = TR.ResultPage()

            page.url = result.URL.replace("&","&amp;")
            page.rank = i
            page.title = testUnicode(result.title)
            page.summary = testUnicode(escapeText(result.snippet))
            if result.cachedSize:
                page.size = int(result.cachedSize[0:len(result.cachedSize)-1])
            # score, date, and type are not available from Google
            # We could figure out type if we needed it
            # Other interesting info available: Open Directory category info
            i += 1

            rl.append(page)
        
        # Now that we have our ResultList, we can transform it into XML
        rl.xml = self.__transform2xml(rl)

        return rl

    def __transform2xml(self, rl):
        """
        Helper function to convert completed ResultList to XML format.
        We are copying Searchblox XML format here.
        """
        
        start = rl[1].rank
        length = len(rl)
        end = start + length - 1
        lastpage = int(rl.totalhits / length)
        if (rl.totalhits % length) > 0:
            lastpage += 1
        curpage = int(start / length) + 1
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += '<searchdoc>'
        xml += '<results hits="%d" query="%s" sort="relevance" ' % \
                    (rl.totalhits, rl.query)
        xml += 'start="%d" end="%d" currentpage="%d" lastpage="%d">' % \
                    (start, end, curpage, lastpage)

        for page in rl:
            # Create a <result> for each ResultPage
            xml += '<result no="%d">' % page.rank
            xml += '<url>%s</url>' % page.url
            xml += '<size>%d</size>' % page.size
            xml += '<title>%s</title>' % page.title
            xml += '<context>%s</context>' % page.summary
            xml += '</result>'

        xml += '</results></searchdoc>'
        return xml

#############################################
# GoogleKeys - Manages a list of google keys #
##############################################
class GoogleKeys:
    def __init__(self):
        self.keys = ["kIJk/xOC3hqHUs82cKP1ZGal37g9hB3L",      # sally's
                     "Byew8HNQFHLLimZKQmaFCiydv5o+foSe",      # eric's
                     "ZRjvW4FQFHIHFGiuxCoI8HAhHc2Y6qeF",      # mario's
                     "p2mgQIlQFHLmYBdfmzUEzaJNw8X20MBp"]      # jonathan's

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, idx):
        key = None
        try:
            key = self.keys[idx]
        except IndexError:
            raise GoogleKeysError('Key index out of range on get')
        return key

    def __setitem__(self, idx, val):
        try:
            self.keys[idx] = val
        except IndexError:
            raise GoogleKeysError('Key index out of range on set')

    def __str__(self):
        return str(self.keys)

    def append(self, key):
        self.keys.append(key)
    
class GoogleKeysError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


"""
Utility functions.
"""
def testUnicode(text):
    if not text:
        return ''
    if isinstance(text, unicode):
        utext = text
    else:
        for charset in ('utf-8', 'latin-1'):
            try:
                #unicode(text,sys.getdefaultencoding(),'strict')
                #unicode(text,'latin-1','strict')
                utext = unicode(text, charset, 'strict')
            except UnicodeDecodeError:
                pass
            else:
                break
        else:
            raise TypeError('Cannot decode %r' % text)
    return utext.encode(config.CHARSET)

def escapeText(text):
    esctext = text.replace("<br>","")
    esctext = esctext.replace("&","&amp;")
    return esctext

"""
Test functions
"""

def testGoogleKeys():
    keys = GoogleKeys()
    print "get key list"
    print keys
    try:
        print "try get out of range"
        print keys[4]
    except GoogleKeysError,e:
        print e.value
    print "try normal set"
    keys[0] = ''
    try:
        print "try set out of range"
        keys[100] = ''
    except GoogleKeysError,e:
        print e.value   
    
def testGoogleWrapper():
    googlequery = 'biodiversity "knowledge commons"'
    print "Google Query: ", googlequery
    numhits = 3
    start = 3  # Google start index starts at 0
    gw = GoogleWrapper(numhits)
    try:
        results = gw.doQuery(googlequery, numhits, start)
    except:
        print "Problem doing Google Query!"
        raise
    if (results):
        print "Query recorded in ResultList object is:  %s" % results.query
        print "Escaped query is: %s" % results.escapedquery
        print "Total hits from Google:  %d" % results.totalhits
        print "Results from %d to %d" % (results.startresult, results.endresult)
        print "Results from ResultList:"
        for result in results:
            #print gw.getCachedPage(result.url)
            print '%d.  <a href="%s">%s</a>' % (result.rank, result.url, 
                                                result.title)
        print "Results from dictionary:"
        dict_results = results.get_dict()
        for result in dict_results["list"]:
            #print result["url"]
            print '%d.  <a href="%s">%s</a>' % (result["rank"], result["url"], 
                                                result["title"])
    else:
        print "No results."

def dummyResults():
    results = TR.ResultList()

    page = TR.ResultPage()

    page.url = 'http://foobar.com/index.html'
    page.rank = 1
    page.title = 'dummy title 1'
    page.summary = '...dummy summary 1...'
    page.size = 10

    results.append(page)

    page = TR.ResultPage()

    page.url = 'http://foobar.com/index.xml'
    page.rank = 2
    page.title = 'dummy title 2'
    page.summary = '...dummy summary 2...'
    page.size = 8

    results.append(page)

    return results

def dummyText():
    return """
    Now is the winter of our discontent, made glorious summer by this son of York.
    Now are our brows bound in glorious wreaths. 
    """

if __name__ == '__main__':
    print "start..."
    testGoogleKeys()
    testGoogleWrapper()
    print "...done"













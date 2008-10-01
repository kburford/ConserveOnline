#!/usr/bin/python
"""
##############################################################################
#
# TNCSearch.py
#
# General Web search interface class. Defines general methods for
# issuing queries to Web search applications.  Parent class for all
# search engine wrappers (like SearchbloxWrapper).
#
# TODO: Create MetaSearch subclass that can broadcast searches
# to multiple different TNCSearch instances (or subclasses).
#
# TODO: Add threaded doQueries to query in parallel for performance
# improvement.
#
############################################################################## 
"""

import threading
import TNCResult as TR

class TNCSearch:
    """
    Super class for classes that execute searches to external
    search engines.
    """
    def __init__(self, numresults=5):
        """
        Create a TNCSearch instance.

        Arguments:
          numresults (default 5) - number of search results to capture for
            each search.
        """
        self.numresults = numresults
        self.id = "TNCSearch"  # Override
        self.name = "TNCSearch" # Override

    def doQuery(self, query, numresults=0):
        """
        Execute a single query.  Return the results as a ResultList - a
        list of canonical search result pages (ResultPage objects)
        plus (optionally) an XML representation.
        
        Subclasses must define this method.

        Arguments:
          query - the query (a string or Query object)
          numresults - number of search results to capture for
            the search, default is the init setting

        Returns:
          a ResultList object
        """
        # Override
        pass

    def doQueries(self, querylist):
        """ 
        Execute a list of queries on the search object and return a list
        of ResultList objects, one for each query.  Use all the
        defaults set when we created the search object.

        Arguments:
          querylist - the list of queries (list of strings or Query objects)

        Returns:
          a list of ResultList objects
        """
        allresults = []
        for query in querylist:
            results = self.doQuery(query)
            if (results):
                allresults.append(results)
            else:
                continue

        return allresults

    def doQueriesThreaded(self, querylist):
        """ 
        Execute a list of queries on the search object using threaded
        search.  Return a list of ResultList objects, one for each
        query.  Use all the defaults set when we created the search
        object.

        Arguments:
          querylist - the list of queries (list of strings or Query objects)

        Returns:
          a list of ResultList objects
        """
        import time
        threads = []
        allresults =[]

        # Build list of search threads
        for query in querylist:
            threads.append(SearchThread(self, query))
        # Start threads
        for thread in threads:
            thread.start()
        # Wait around until threads are done.
        # Do not wait more than 10 seconds.
        # TODO add stopwatch
        while threading.activeCount() > 1:
            time.sleep(0.1)
            pass
        # Threads are done, go through results
        for thread in threads:
            if thread.results:
                allresults.append(thread.results)

        return allresults

    def __transformResults(self, results):
        """
        Private method to transform the search results into the
        canonical form - a ResultList (list of ResultPage objects
        plus optionally an XML representation).

        Subclasses must define this method.

        Arguments:
          results - the list of results in whatever format the search engine
            uses

        Returns:
          a ResultList
        """
        pass

class SearchThread(threading.Thread):
    """ 
    Thread object for searching.
    """
    def __init__(self, searchobj, query):
        """ 
        Create a thread for a search object. The search object must be
        passed in during __init__ and must respond to the doQuery method.
        The search object must be initialized with all parameters that
        it needs (this depends on the engine), except that the query is
        optional.

        Arguments:
          searchobj - the search object (for example, a GoogleWrapper instance)
          query - the query, a Query class instance or a string
        """
        threading.Thread.__init__(self)
        self.setName(searchobj.name + " : " + query)
        self.searchobj = searchobj
        self.query = query

    def run(self):
        """
        Run the thread - that is, do the search.
        """
        self.__doSearch()

    def __doSearch(self):
        """
        Private method to do the search.  May be overridden.
        """
        try:
            self.results = self.searchobj.doQuery(self.query)
        except:
            raise

def activeThreads():
    """
    Display current active threads (not mainthread)
    """
    threads = threading.enumerate()
    for thread in threads:
        name = thread.getName()
        if not name == "MainThread":
            print name
			
if __name__ == '__main__':

    query = "python"
    numhits = 3
    search = TNCSearch(numhits)
    results = search.doQuery(query) # nothing should happen
    print "Numhits is set at %d" % search.numresults

    import time
    import GoogleWrapper
    threads = []
    search = GoogleWrapper.GoogleWrapper()
    queries = ["biodiversity", "ecoregional planning"]
    print "Testing threads..."
    for query in queries:
        threads.append(SearchThread(search, query))
    for thread in threads:
        thread.start()
    # display active processes
    while threading.activeCount() > 1:
        activeThreads()
        time.sleep(1)
    for thread in threads:
        print thread.getName(),  ' found ', str(thread.results.totalhits), \
            'docs'
		
    print "\nDONE:"

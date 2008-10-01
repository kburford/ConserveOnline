#!/usr/bin/python
"""
##############################################################################
#
# TNCResult.py
#
# Classes and methods for managing search results - ResultList and
# ResultPage objects.
#
############################################################################## 
"""

import string
import urllib
import sys

class ResultList:
    """
    Class for managing a list of ResultPage objects, plus (optionally)
    the results in XML format.
    """
    def __init__(self):
        """
        Instantiate a ResultList object
        """
        self.__list = []      # A list of ResultPage objects (private)
        self.query = ""       # The query that created the results
        self.engine = ""      # The id of the search wrapper that created 
        self.totalhits = 0    # How many hits total for the query
        self.startresult = 0  # Rank of first result in the list
        self.endresult = 0    # Rank of last result in the list
        self.pagenum = 0      # Page number of these results
        self.lastpage = 0     # Last page for all results
        self.xml = ""         # The result list as XML
                              # Some engines (Searchblox) provide
                              # For others we need to create

    def __len__(self):
        """
        Return length of list of ResultPage objects.
        (Not total number of hits for the query.)
        """
        return len(self.__list)

    def __getitem__(self, idx):
        """
        Get item at index 'idx'
        """
        return self.__list[idx]

    def getTotalhits(self): 
        """
        Return total number of hits for the query.
        """
        return self.totalhits

    def getXML(self): 
        """
        Return the ResultList in XML format.
        """
        return self.xml

    def appendlist(self, results):
        """
        Add the contents of the input ResultList to self
        """
        for item in results:
            self.append(item)
        # If this had an xmlresult, it is now invalid
        self.xmlresult = ""

    def extend(self, results):
        """
        Add the contents of the input ResultList to self
        using the normal Python list concatenation method name
        """
        self.appendlist(results)

    def append(self, result):
        """
        Append this ResultPage to the list.

        Check for dupes using URL and summary if one exists.
        """
        dupeFound = 0

        for item in self:
            if (result.url and result.url == item.url) and \
                (result.summary and result.summary == item.summary):
                dupeFound = 1
                break

        if not dupeFound: self.__list.append(result)

    def fetch(self, fetchmethod=None):
        """
        Fetch the full-text of each item in the result list.
        Use the provided fetch method, else use standard URL fetch.
        TODO: a threaded fetch method
        """
        for result in self:
            if fetchmethod:
                result.rawpage = fetchmethod(result.url)
            else:
                result.fetchRawPage()

    def sort(self):
        """
        Sort the list by descending score.
        """
        list = [(result.score,result) for result in self]
        list.sort()
        list.reverse()
        self.__list = [result for (score,result) in list]

    def get_dict(self):
        """
        Get results in a list of dicts
        """
        dict_list = []

        # Transform each ResultPage into a dictionary
        for  result in self:
            dict = {}
            keys = dir(result)
            #print str(keys)
            for key in keys:
                if key[0] != '_':
                    dict[key] = getattr(result, key)
            dict_list.append(dict)

        # Transform the ResultList attributes into a dictionary
        dict = {}
        keys = dir(self)
        #print str(keys)
        for key in keys:
            if key[0] != '_':
                dict[key] = getattr(self, key)

        # Add the dictionaries under list 
        dict['list'] = dict_list

        # Return the dictionary with the list items
        return dict
          

class ResultPage:
    """
    Class for holding ResultPage objects - a Web page in the
    context of a search
    """
    def __init__(self, url=None, testfile=None):
        """
        Instantiate a ResultPage object
        """

        # Public attributes
       	self.url = url
        self.title = ''
        self.rank = 0     # From the search engine
        self.score = 0.0  #          "
       	self.summary = '' #          "
        self.date = ''    #          "
        self.size = 0     # Searchblox gives this in KB - if we mix engines
                          # we may have to convert
        self.type = ''    # content type
        self.info = {}
        self.rawpage = ''
        # Private
        self.__testfile = testfile  # for offline testing
    
    def fetchRawPage(self):
        """
        Fetch the raw text for this Web page. Uses standard urllib method.
        """
        if self.__testfile:
            self.setRawPage(open(self.__testfile,"r").read())
        elif not self.rawpage:
            try:
                webpage = urllib.urlopen(self.url)
                self.rawpage = webpage.read()
                self.info = webpage.info()
                webpage.close()
            except:
                return ''   # Return empty page if error.
        return self.rawpage

    def setRawPage(self,rawpage):
        """
        Set the raw text for this Web page.

        Useful for certain testing operations or if raw
        text is fetched using some other method.
        """
        self.rawpage = rawpage
        self.info = {}

    def __len__(self):
        return len(self.rawpage)

    def __str__(self):
        return str(self.url)

#
# Helper functions
#

def printResultPage(page): 
    """
    Print a ResultPage object
    """
    line()
    print "URL:\n", page.url
    print "Title:\n", page.title
    print "Summary:\n", page.summary
    page.fetchRawPage()
    line()
    print "PageInfo:\n", page.info
    line()
    print "RawPage: %d characters\n" % len(page.rawpage)
    print page.rawpage[0:200]
    print "...etc...\n"
    line()

def line():
	print "-" * 60
	
if __name__ == '__main__':

    # Create some ResultPage objects
    page1 = ResultPage("test1.htm","../TNCSearch/test1.htm")
    page1.title = "Move Review: Star Wars: The Phantom Menace"
    page1.summary = "...what a movie, the phantom menace blew my socks off..."
    page2 = ResultPage("http://nature.org/")
    page2.title = "The Nature Conservancy Home Page"
    page2.summary = "...this is TNC's home page..."
    page3 = ResultPage("http://avaquest.com/")
    page3.title = "AvaQuest Home Page"
    page3.summary = "...this is AvaQuest's home page..."
    page4 = ResultPage("http://conserveonline.org/")
    page4.title = "ConserveOnline Home Page"
    page4.summary = "...this is COL's home page..."

    # Create 2 ResultList objects
    rlist1 = ResultList()
    rlist1.append(page1)
    rlist1.append(page2)
    rlist1.append(page3)
    rlist2 = ResultList()
    rlist2.append(page3)
    rlist2.append(page4)

    # Append second list to first - should de-dup
    rlist1.appendlist(rlist2)
    print "Length of combined lists is %d" % len(rlist1)

    # Print 
    for page in rlist1:
        printResultPage(page)

    # Print the dict list
    dict = rlist1.get_dict()
    for r in dict:
	print r["title"]

	

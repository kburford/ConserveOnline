#!/usr/bin/python
"""
##############################################################################
#
# TNCQuery.py
#
# Defines classes and methods for Web search queries.
#
# The Query class provides a framework for translating from one
# search engine's query syntax to another.
# - Each query must have a search engine associated with it (which indicates
#   what query syntax was used)
# - It must be possible to spell check the query (using Google), either
#   automatically, or by suggesting corrections
# - It must be possible to get the query translated into another 
#   search engine's syntax
# - Searchblox to Google translation:
#   - "exact phrases" in quotes mean the same - don't change
#   - plus means something different in Google (include a common word) but 
#     is not harmful - don't change
#   - minus means the same - don't change
#   - Boolean AND could be left unchanged since it will be an ignored
#     stopword, or it could be eliminated - Google always searches for
#     all terms
#   - Boolean OR is the same in Google - do not change
#   - Boolean NOT change to minus
#   - single character (?) and multiple character (*) wildcards don't exist,
#     remove
#   - fielded search:
#     - title: changes to intitle:
#     - description: doesn't exist, remove
#     - url: changes to inurl:
#     - contenttype: changes to filetype:
#     - keywords: doesn't exist, remove
#   - fuzzy search (~ at end of single word) doesn't exist, remove
#   - proximity search (~ at end of quoted phrase) doesn't exist, remove
#
# TODO:
#   - Provide an enhanced query with noun phrases quoted
#
############################################################################## 
"""
import re
import GoogleWrapper
google_spellcheck = GoogleWrapper.GoogleWrapper().spellCheck

class Query:
    """
    Class to encapsulate queries and their translation from one search
    engine's query syntax to another.
    """
    # Define the regular expressions we will use
    wildcard = re.compile("([a-zA-Z]+\?[a-zA-Z]*)|([a-zA-Z]+\*[a-zA-Z]*)", 
                          re.I)
    fuzzyandprox = re.compile("\~[0-9]*", re.I)

    def __init__(self, query="", engine="searchblox", spellcheck=0):
        """
        Create a Query class instance.  Arguments:
          query - the query string (default "")
          engine - the search engine syntax used (a string, choices are
            "searchblox" and "google", default is "searchblox")
          spellcheck - flag to indicate whether to correct spelling errors
            in the query (default 0)
        """
        self.query = query
        if spellcheck:
            try:
                self.query = self.spellcheck()
            except:
                pass # self.query stays the same
        self.engine = engine.lower()

    def spellcheck(self):
        """ 
        Suggest corrections to spelling errors in self.query using
        Google's spell checker.  Return the suggested corrections.
        """
        try:
            correction = google_spellcheck(self.query)
        except:
            correction = self.query
        return correction

    def translate(self, engine):
        """
        Translate query from original query syntax to the syntax of
        the search engine whose name is passed.  Return the translated
        query.
        """
        engine = engine.lower()
        if engine == self.engine:
            return self.query
        elif (engine == "google") and (self.engine == "searchblox"): 
            return self.__searchblox2google()
        else:
            return self.query

        # TODO: add google2searchblox

    def __searchblox2google(self):
        """
        Translate self.query from searchblox to google format. 
        Return the google format query.
        """
        new = self.query
        # Change NOT to minus
        new = new.replace(' NOT ', ' -')
        # Change url: to inurl:
        new = new.replace('url:', 'inurl:')
        # Change contenttype: to filetype:
        new = new.replace('contenttype:', 'filetype:')
        # Change title: to intitle:
        new = new.replace('title:', 'intitle:')
        # Eliminate fuzzy spelling and proximity
        new = re.sub(self.fuzzyandprox, " ", new)
        # Eliminate wildcard expressions
        new = re.sub(self.wildcard, " ", new)
        # Eliminate description: and keyword:
        new = new.replace('description:', '')
        new = new.replace('keywords:', '')

        return new

if __name__ == '__main__':
    sbquery = 'title:biodiversity NOT amphibians'
    googlequery = 'intitle:biodiversity -amphibians' 
    query = Query(sbquery, 'Searchblox')
    translated = query.translate('GOOGLE')
    print "Original query is : %s" % sbquery
    print "Translated query is : %s" % translated
    if not (translated == googlequery):
        print "Expected: %s" % googlequery
    

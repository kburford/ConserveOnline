# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: test_security.py 12505 2007-05-17 16:37:49Z jens $

import unittest

# Load IPyton genutils to get the stdout and stderr right while in an IPython
# shell
try:
    from IPython import genutils
    del genutils
except ImportError:
    pass

from Testing.ZopeTestCase import FunctionalDocFileSuite

from Products.COL3.testing import COL3FunctionalTestCase


def test_suite():
    suite = unittest.TestSuite()
    files = [ 
             #'invitations_tool.txt',
             #'join_requests_tool.txt',
             'crossref_tool.txt',
             ]
    for f in files:
        fsuite = FunctionalDocFileSuite(f,
                                        test_class=COL3FunctionalTestCase,
                                        package='Products.COL3.tools.tests',)
        suite.addTest(fsuite)

    return suite


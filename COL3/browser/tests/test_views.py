# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: test_views.py 40673 2008-07-16 13:02:22Z deo $

import unittest

# Load IPyton genutils to get the stdout and stderr right while in an IPython
# shell
try:
    from IPython import genutils
    del genutils
except ImportError:
    pass

from Testing.ZopeTestCase import FunctionalDocFileSuite

from zope.testing import doctest

from Products.COL3.testing import COL3FunctionalTestCase

def test_suite():
    import z3c.etree.testing
    suite = unittest.TestSuite()
    files = [ 'registration-view.txt',
              'password-reset-view.txt',
              'password-change-view.txt',
              'preferences-view.txt',
              'member-search-view.txt',
              'invitation-add-view.txt',
              'workspace-member-management-view.txt',
              'workspace-docs-bylabel.txt',
              'discussion-views.txt',
            ]
    for f in files:
        fsuite = FunctionalDocFileSuite(f,
                                        test_class=COL3FunctionalTestCase,
                                        package='Products.COL3.browser.tests',
                                        checker = z3c.etree.testing.xmlOutputChecker,
                                        setUp = z3c.etree.testing.etreeSetup,
                                        tearDown = z3c.etree.testing.etreeTearDown,
                                        optionflags=doctest.NORMALIZE_WHITESPACE,)
        suite.addTest(fsuite)

    return suite


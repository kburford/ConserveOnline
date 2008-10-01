# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: tests.py 11233 2007-05-01 18:18:32Z jens $

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
    import z3c.etree.testing
    suite = unittest.TestSuite()
    files = [
        'workspace-browsing.txt',
        'workspace-edit-properties.txt',
        'workspace-management-views.txt',
        'workspace-member-management-view.txt',
        'workspace-rss-feeds.txt',
        'workgroup-creation.txt',
        'discussion-forms.txt',
        'add-registration-forms.txt',
        'user-editnamedesc.txt',
        'exception-views.txt',
        'page-views.txt',
        'file-views.txt',
        'calendar-forms.txt',
        'calendar-views.txt',
        'documents-browsing.txt',
        'edit-label-forms.txt',
        'libraryfile-views.txt',
        'library-listing-view.txt',
        'people-browsing.txt',
        'recommendation-forms.txt',
        'allratings.txt',
         ]
    for f in files:
        fsuite = FunctionalDocFileSuite(
            f,
            test_class=COL3FunctionalTestCase,
            package='Products.COL3.browser.tests',
            checker = z3c.etree.testing.xmlOutputChecker,
            setUp = z3c.etree.testing.etreeSetup,
            tearDown = z3c.etree.testing.etreeTearDown
        )
        suite.addTest(fsuite)

    return suite

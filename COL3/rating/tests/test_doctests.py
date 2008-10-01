# The Nature Conservacy
# Copyright(C), 2007, Enfold Systems, Inc. - ALL RIGHTS RESERVED
#
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied
# this software.  Any inquiries concerning the scope or
# enforceability of the license should be addressed to:
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.COL3.testing import COL3FunctionalTestCase

def test_suite():
    import z3c.etree.testing
    suite = unittest.TestSuite()
    files = [
        'rating.txt',
         ]
    for f in files:
        fsuite = FunctionalDocFileSuite(
            f,
            test_class=COL3FunctionalTestCase,
            package='Products.COL3.rating.tests',
            checker=z3c.etree.testing.xmlOutputChecker,
            setUp=z3c.etree.testing.etreeSetup,
            tearDown=z3c.etree.testing.etreeTearDown
        )
        suite.addTest(fsuite)
    return suite

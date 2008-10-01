# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: tests.py 23016 2007-09-27 20:26:22Z leo $

# Load fixture
from Testing import ZopeTestCase

# Load IPyton genutils to get the stdout and stderr right while in an IPython
# shell
try:
    from IPython import genutils
    del genutils
except ImportError:
    pass

# This needs to come before PloneTestCase
ZopeTestCase.installProduct('COL3')

from Products.PloneTestCase.layer import ZCML as ZCMLLayer

def test_suite():
    import unittest
    import z3c.etree.testing
    from Testing.ZopeTestCase import FunctionalDocFileSuite, FunctionalDocTestSuite

    suite = unittest.TestSuite()
    files = [
        'xmlformlib.txt',
        'xmlfields.txt',
        ]
    for f in files:
        fsuite = FunctionalDocFileSuite(
            f,
            test_class=ZopeTestCase.ZopeTestCase,
            package='Products.COL3.formlib.tests',
            checker = z3c.etree.testing.xmlOutputChecker,
            setUp = z3c.etree.testing.etreeSetup,
            tearDown = z3c.etree.testing.etreeTearDown)
        fsuite.layer = ZCMLLayer
        suite.addTest(fsuite)
    from Products.COL3.formlib import schema
    fsuite = FunctionalDocTestSuite(schema, globs=schema.__dict__)
    fsuite.layer = ZCMLLayer
    suite.addTest(fsuite)
    return suite

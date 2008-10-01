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

import Products.COL3.browser.batch
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.browser.batch import BatchProvider
from Testing.makerequest import makerequest
from Acquisition import Implicit

def make_request():
    return makerequest(Implicit()).REQUEST

class DummyProvider(BatchProvider):
    def query(self, params):
        items = []
        for i in xrange(params['start'], params['end']):
            items.append({'title': 'item %s' % i,
                          'description': 'description %s' % i,
                          })
        return items

DummyBatchFragment = BatchFragmentFactory(DummyProvider)

class BatchTest(unittest.TestCase):

    def testBatchProvider(self):
        provider = DummyProvider(None, None)
        self.assertEquals(len(provider.query({'start':0, 'end':30})), 30)
        self.assertEquals(len(provider.query({'start':0, 'end':10})), 10)

    def testBatchFragmentComputeParams(self):
        request = make_request()

        batch = DummyBatchFragment(None, request)
        self.assertEquals(batch.size, 20)
        params = batch.computeParams()

        self.assertEquals(params['start'], 0)
        self.assertEquals(params['end'], 20)
        self.assertEquals(params['sort_on'], None)
        self.assertEquals(params['sort_order'], None)

        request.set('start', '32')
        params = batch.computeParams()
        self.assertEquals(params['start'], 32)
        self.assertEquals(params['end'], 52)
        self.assertEquals(params['sort_on'], None)
        self.assertEquals(params['sort_order'], None)

        request.set('page', '3')
        params = batch.computeParams()
        self.assertEquals(params['start'], 40)
        self.assertEquals(params['end'], 60)
        self.assertEquals(params['sort_on'], None)
        self.assertEquals(params['sort_order'], None)

        request.set('sort_on', 'title')
        request.set('sort_order', 'desc')
        params = batch.computeParams()
        self.assertEquals(params['start'], 40)
        self.assertEquals(params['end'], 60)
        self.assertEquals(params['sort_on'], 'title')
        self.assertEquals(params['sort_order'], 'desc')

        request.set('sze', '15')
        params = batch.computeParams()
        self.assertEquals(params['start'], 30)
        self.assertEquals(params['end'], 45)
        self.assertEquals(params['sort_on'], 'title')
        self.assertEquals(params['sort_order'], 'desc')

    def testBatchFragmentInfo(self):
        request = make_request()
        batch = DummyBatchFragment(None, request)
        provider = batch.provider(None, request)

        # 'end' is 50 here to generate 50 items.
        results = provider.query({'start': 0, 'end': 50})

        # 'end' is 20 here because we are looking at the first batch.
        info = batch.info({'start': 0, 'end': 20,
                           'sze': 20, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 50)
        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 20)

        self.assertEquals(len(info['pages']), 3)

        self.assertEquals(info['pages'][0]['url'], 'http://foo?start:int=0&sze:int=20') 
        self.assertEquals(info['pages'][0]['current'], True)

        self.assertEquals(info['pages'][1]['url'], 'http://foo?start:int=20&sze:int=20')
        self.assertEquals(info['pages'][1]['current'], False)

        self.assertEquals(info['pages'][2]['url'], 'http://foo?start:int=40&sze:int=20')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failIf(info.has_key('prev'))
        self.failUnless(info.has_key('next'))
        
        self.assertEquals(info['next']['url'], 'http://foo?start:int=20&sze:int=20')

        # Now move it to the second batch and do it all over again
        info = batch.info({'start': 20, 'end': 40,
                           'sze': 20, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 50)
        self.assertEquals(info['start'], 21)
        self.assertEquals(info['end'], 40)

        self.assertEquals(len(info['pages']), 3)

        self.assertEquals(info['pages'][0]['url'], 'http://foo?start:int=0&sze:int=20')
        self.assertEquals(info['pages'][0]['current'], False)

        self.assertEquals(info['pages'][1]['url'], 'http://foo?start:int=20&sze:int=20')
        self.assertEquals(info['pages'][1]['current'], True)

        self.assertEquals(info['pages'][2]['url'], 'http://foo?start:int=40&sze:int=20')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failUnless(info.has_key('prev'))
        self.failUnless(info.has_key('next'))
        
        self.assertEquals(info['prev']['url'], 'http://foo?start:int=0&sze:int=20')
        self.assertEquals(info['next']['url'], 'http://foo?start:int=40&sze:int=20')

def test_suite():
    import z3c.etree.testing
    from zope.testing.doctest import DocFileSuite
    from zope.testing.doctest import DocTestSuite

    suite = unittest.TestSuite()
    files = [
        'batch.txt',
        ]
    for f in files:
        fsuite = DocFileSuite(
            f,
            package='Products.COL3.tests',
            checker = z3c.etree.testing.xmlOutputChecker,
            setUp = z3c.etree.testing.etreeSetup,
            tearDown = z3c.etree.testing.etreeTearDown)
        suite.addTest(fsuite)
    suite.addTest(unittest.makeSuite(BatchTest))
    suite.addTest(
        DocTestSuite(Products.COL3.browser.batch,
                     checker = z3c.etree.testing.xmlOutputChecker,
                     setUp = z3c.etree.testing.etreeSetup,
                     tearDown = z3c.etree.testing.etreeTearDown))
    return suite


# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

import unittest

from Acquisition import Implicit
from Testing.makerequest import makerequest

import Products.COL3.browser.batch
from Products.COL3.browser.batch import BatchFragmentFactory
from Products.COL3.browser.workspacebrowsing import WorkspaceByCountryBatchProvider
from Products.COL3.browser.workspacebrowsing import WSBrowseBySearchtermBatchProvider
from Products.COL3.testing import COL3FunctionalTestCase

WorkspaceByCountryBatchFragment = BatchFragmentFactory(WorkspaceByCountryBatchProvider)
WorkspaceBySearchtermsBatchFragment = BatchFragmentFactory(WSBrowseBySearchtermBatchProvider)

def make_country_content(context):
    context.invokeFactory('Workspace', id='test-ws-1', title='test ws 1')
    context['test-ws-1'].update(country='ARG')
    context.invokeFactory('Workspace', id='test-ws-2', title='test ws 2')
    context['test-ws-2'].update(country='USA')
    context.invokeFactory('Workspace', id='test-ws-3', title='test ws 3')
    context['test-ws-3'].update(country='BRA')
    context.invokeFactory('Workspace', id='test-ws-4', title='test ws 4')
    context['test-ws-4'].update(country='ARG')
    context.invokeFactory('Workspace', id='test-ws-5', title='test ws 5')
    context['test-ws-5'].update(country='ARG')
    context.invokeFactory('Workspace', id='test-ws-6', title='test ws 6')
    context['test-ws-6'].update(country='USA')

def make_keyword_content(context):
    context.invokeFactory('Workspace', id='test-ws-1', title='test ws 1')
    context['test-ws-1'].update(keywords=['Mustard'])
    context.invokeFactory('Workspace', id='test-ws-2', title='test ws 2')
    context['test-ws-2'].update(keywords=['Salami', 'Ham'])
    context.invokeFactory('Workspace', id='test-ws-3', title='test ws 3')
    context['test-ws-3'].update(keywords=['Honey Mustard', 'Cheese'])
    context.invokeFactory('Workspace', id='test-ws-4', title='test ws 4')
    context['test-ws-4'].update(keywords=['Pepper', 'Ham'])
    context.invokeFactory('Workspace', id='test-ws-5', title='test ws 5')
    context['test-ws-5'].update(keywords=['Catchup', 'Cheese'])
    context.invokeFactory('Workspace', id='test-ws-6', title='test ws 6')
    context['test-ws-6'].update(keywords=['Spam', 'Ham'])


class WorkspaceByCountryBatchTest(COL3FunctionalTestCase):

    def testBatchAsElement(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_country_content(self.portal.workspaces)

        batch = WorkspaceByCountryBatchFragment(self.portal.workspaces, request)
        self.failUnless(batch.asElement())

    def testByCountryFilter(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_country_content(self.portal.workspaces)

        batch = WorkspaceByCountryBatchFragment(self.portal.workspaces, request)
        provider = batch.provider(self.portal.workspaces, request)

        results = provider.query({})

        self.assertEquals(len(results), 3)

        self.assertEquals(results[0]['count'], 3)
        self.assertEquals(results[0]['country'], u'Argentina')
        self.assertEquals(results[0]['href'], 'http://nohost/plone/workspaces/withcountry-workspaces.html?country=ARG')

        self.assertEquals(results[1]['count'], 1)
        self.assertEquals(results[1]['country'], u'Brazil')
        self.assertEquals(results[1]['href'], 'http://nohost/plone/workspaces/withcountry-workspaces.html?country=BRA')

        self.assertEquals(results[2]['count'], 2)
        self.assertEquals(results[2]['country'], u'United States of America')
        self.assertEquals(results[2]['href'], 'http://nohost/plone/workspaces/withcountry-workspaces.html?country=USA')


    def testBatchFragmentInfo(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_country_content(self.portal.workspaces)

        batch = WorkspaceByCountryBatchFragment(self.portal.workspaces, request)
        provider = batch.provider(self.portal.workspaces, request)

        results = provider.query({})

        info = batch.info({'start': 0, 'end': 2,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 2)
        self.assertEquals(info['total'], 3)
        self.assertEquals(len(info['pages']), 2)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], True)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], False)

        self.failIf(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['next']['url'], 'http://nohost?start:int=2&sze:int=2')

        # Now move it to the second batch and do it all over again
        info = batch.info({'start': 2, 'end': 4,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['start'], 3)
        self.assertEquals(info['end'], 3)
        self.assertEquals(info['total'], 3)

        self.assertEquals(len(info['pages']), 2)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], False)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], True)

        self.failUnless(info.has_key('prev'))
        self.failIf(info.has_key('next'))

        self.assertEquals(info['prev']['url'], 'http://nohost?start:int=0&sze:int=2')


class WorkspaceBySearchtermsBatchTest(COL3FunctionalTestCase):

    def testBatchAsElement(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_keyword_content(self.portal.workspaces)

        batch = WorkspaceBySearchtermsBatchFragment(self.portal.workspaces, request)
        self.failUnless(batch.asElement())

    def testBatchFragmentInfo(self):
        request = self.portal.REQUEST
        self.setRoles(['Manager'])
        make_keyword_content(self.portal.workspaces)

        batch = WorkspaceBySearchtermsBatchFragment(self.portal.workspaces, request)
        provider = batch.provider(self.portal.workspaces, request)

        # 'end' fetch at least 10 items, if they are available.
        results = provider.query({'start': 0, 'end': 10})

        info = batch.info({'start': 0, 'end': 2,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 8)
        self.assertEquals(info['start'], 1)
        self.assertEquals(info['end'], 2)

        self.assertEquals(len(info['pages']), 4)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], True)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], False)

        self.assertEquals(info['pages'][2]['url'], 'http://nohost?start:int=4&sze:int=2')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failIf(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['next']['url'], 'http://nohost?start:int=2&sze:int=2')

        # Now move it to the second batch and do it all over again
        info = batch.info({'start': 2, 'end': 4,
                           'sze': 2, 'sort_on': None,
                           'sort_order': None}, results)

        self.assertEquals(info['total'], 8)
        self.assertEquals(info['start'], 3)
        self.assertEquals(info['end'], 4)

        self.assertEquals(len(info['pages']), 4)

        self.assertEquals(info['pages'][0]['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['pages'][0]['current'], False)

        self.assertEquals(info['pages'][1]['url'], 'http://nohost?start:int=2&sze:int=2')
        self.assertEquals(info['pages'][1]['current'], True)

        self.assertEquals(info['pages'][2]['url'], 'http://nohost?start:int=4&sze:int=2')
        self.assertEquals(info['pages'][2]['current'], False)

        self.failUnless(info.has_key('prev'))
        self.failUnless(info.has_key('next'))

        self.assertEquals(info['prev']['url'], 'http://nohost?start:int=0&sze:int=2')
        self.assertEquals(info['next']['url'], 'http://nohost?start:int=4&sze:int=2')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(WorkspaceByCountryBatchTest))
    suite.addTest(unittest.makeSuite(WorkspaceBySearchtermsBatchTest))
    return suite

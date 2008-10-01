# COL3
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

"""
This is a 'zopectl run' script that process all the subscriptions.

It's designed to be run via a daily cronjob.
"""

import sys
import transaction
from logging import getLogger
from DateTime.DateTime import DateTime
from zope.app.component.hooks import setSite
from Products.COL3.config import MAX_SUBSCRIPTION_LINKS
from Products.COL3.browser.mail import simple_mail_tool

log = getLogger('Products.ConserveOnline.Extensions.process_subscriptions')

def logger_and_responder(response):
    def log_and_respond(msg):
        response.write(msg + '\n')
        log.info(msg)
    return log_and_respond

def setResponseCharsetAndGetLogger(self):
    response = self.REQUEST.RESPONSE
    charset = self.portal_properties.site_properties.default_charset
    response.setHeader("Content-Type", "text/plain; charset=" + charset)
    logresp = logger_and_responder(response)
    return logresp

def build_query(obj, size):
    query = {
        'sort_on': 'created',
        'sort_order': 'reverse',
    }
    if size > 0:
        query['sort_limit'] = size
    else:
        last_ran = subscription.getLast_ran()
        if last_ran:
            query['created'] = {'query': last_ran, 'range': 'min'}
        else:
            # we don't want to return everything since ConserveOnline's inception
            query['sort_limit'] = MAX_SUBSCRIPTION_LINKS
    fields = [
        'getLanguage',
        'getCountry',
        'getBiogeographic_realm',
        'getOrganization',
        'getHabitat',
        'getConservation',
        'getDirectthreat',
        'getMonitoring',
        'getKeywords',
    ]
    for field in fields:
        accessor = getattr(obj, field)
        value = accessor()
        if value:
            query[field] = value
    return query

def process_subscription(self, subscription, size=-1, log=None, hostname="conserveonline.org"):
    if subscription.getDelivery_method() == 'email':
        smt = simple_mail_tool()
        membership = self.portal_membership
        catalog = self.notification_catalog
        query = build_query(subscription, size)
        results = catalog(**query)[:MAX_SUBSCRIPTION_LINKS]
        member = membership.getAuthenticatedMember()
        userid = member.getId()
        foopath = "http://foo/"
        hostpath = "http://" + hostname + "/"
        if len(results):
            now = DateTime()
            links = []
            for item in results:
                links.append(item.getURL().replace(foopath, hostpath))
            links = '\n'.join(links)
            unsubscribe = self.absolute_url().replace(foopath, hostpath) + '/subscriptions/unsubscription.html'
            email = member.getProperty('email')
            if log:
                log('Sending notification to user %s.' % userid)
            if size > 0:
                smt.sendSubscriptionEmail(self, links, unsubscribe, email)
            else:
                smt.sendSubscriptionDigestEmail(self, links, unsubscribe, email)
            subscription.setLast_ran(now)
        else:
            if log:
            	log("No results to process for user %s." % userid)

if __name__ == '__main__':
    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest
    app = makerequest(app)
    plonesite = 'Plone'
    if len(sys.argv) > 1:
        plonesite = sys.argv[1]
    hostname = "conserveonline.org"
    if len(sys.argv) > 2:
        hostname = sys.argv[2]
    portal = app.unrestrictedTraverse(plonesite)
    setSite(portal)
    logresp = setResponseCharsetAndGetLogger(portal)
    membership = portal.portal_membership
    for subscription in portal.subscriptions.objectValues():
        userid = subscription.getId().split('_', 1)[1]
        member = membership.getMemberById(userid)
        newSecurityManager(None, member)
        process_subscription(portal, subscription, log=logresp, hostname=hostname)

    txn = transaction.get()
    txn.note("Processed all the subscription items.")
    txn.commit()

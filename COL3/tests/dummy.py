# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: dummy.py 17164 2007-07-20 02:05:13Z leo $

from Products.CMFCore.tests.base.dummy import DummyTool
from Products.CMFCore.tests.base.dummy import DummyUser
import Acquisition

class SimpleObject(Acquisition.Implicit):
    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

class DummyMembershipTool(DummyTool):
    """ Extended to provide getMemberById

    Will only return a user if asked for user "dummy"
    """

    def getMemberById(self, id):
        if id in ('dummy',): return DummyUser(id)

class DummyRegistrationTool(DummyTool):
    """ Extended to provide isMemberIdAllowed

    Knows "dummy" member, so "dummy" is not allowed.
    """

    def isMemberIdAllowed(self, id):
        return id != 'dummy'


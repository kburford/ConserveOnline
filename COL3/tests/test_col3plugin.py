# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: test_col3plugin.py 20289 2007-08-29 04:22:57Z leo $

import unittest

from zope.interface.verify import verifyClass
from zope import schema

class COL3MultiPluginTests(unittest.TestCase):

    def _getTargetClass(self):
        from Products.COL3.user import COL3MultiPlugin
        return COL3MultiPlugin

    def _makeOne(self, **kw):
        return self._getTargetClass()('test_plugin', **kw)

    def test_plugin_conformance(self):
        from Products.PluggableAuthService.interfaces.plugins \
            import IPropertiesPlugin
        from Products.PluggableAuthService.interfaces.plugins \
            import IUserFactoryPlugin

        verifyClass(IPropertiesPlugin, self._getTargetClass())
        verifyClass(IUserFactoryPlugin, self._getTargetClass())

    def test_plugin_listInterfaces(self):
        from Products.PluggableAuthService.interfaces.plugins \
            import IPropertiesPlugin
        from Products.PluggableAuthService.interfaces.plugins \
            import IUserFactoryPlugin
        
        listed = self._makeOne().listInterfaces()

        self.failUnless(IPropertiesPlugin.__name__ in listed)
        self.failUnless(IUserFactoryPlugin.__name__ in listed)

    def test_plugin_instantiation(self):
        plugin = self._makeOne(title='foo')
        self.assertEquals(plugin.getId(), 'test_plugin')
        self.assertEquals(plugin.title, 'foo')

    def test_userCreation(self):
        from Products.COL3.user import COL3User

        plugin = self._makeOne()
        user = plugin.createUser('user_id', 'user_name')

        self.failUnless(isinstance(user, COL3User))
        self.assertEquals(user.getId(), 'user_id')
        self.assertEquals(user.getUserName(), 'user_name')

    def test_propertysheet_defaults(self):
        from Products.COL3.user import COL3PropertySheet
        from Products.COL3.interfaces.user import IUserPropertiesSchema

        plugin = self._makeOne()
        user = plugin.createUser('unknown', 'unknown')
        defaults = {}
        property_ids = schema.getFieldNames(IUserPropertiesSchema)
        for p_id in property_ids:
            defaults[p_id] = IUserPropertiesSchema.get(p_id).default

        sheet = plugin.getPropertiesForUser(user)

        self.failUnless(isinstance(sheet, COL3PropertySheet))
        self.assertEquals(sheet.getId(), plugin.getId())
        self.assertEquals(set(property_ids), set(sheet.propertyIds()))

        for key, value in sheet.propertyItems():
            self.assertEquals(value, defaults[key])

    def test_propertysheet_setting_values(self):
        from Products.COL3.user import COL3PropertySheet
        plugin = self._makeOne()
        user = plugin.createUser('user_id', 'user_name')

        data = { 'firstname' : 'John'
               , 'lastname': 'Doe'
               , 'fullname': 'Ignore Me'
               , 'email' : 'johndoe@example.com'
               , 'type_of_organization' : 'Government'
               , 'organization' : 'BND'
               , 'country' : 'Germany'
               , 'biography' : 'I spy on people.'
               , 'bogus_property' : 'bogus_value'
               }
        sheet = COL3PropertySheet( plugin.getId()
                                 , schema=plugin._getPASSchema()
                                 , **data
                                 )
        plugin.setPropertiesForUser(user, sheet)
        saved_sheet = plugin.getPropertiesForUser(user)

        self.failIf('bogus_property' in saved_sheet.propertyIds())
        self.assertEquals(sheet.propertyMap(), saved_sheet.propertyMap())
        sheet_data = dict(sheet.propertyItems())
        # check we got the full name derived from first/lastname instead of
        # the bogus one
        sheet_data.update(fullname='John Doe')
        self.assertEquals( set(sheet_data.items())
                         , set(saved_sheet.propertyItems())
                         )

    def test_validation_turned_off(self):
        from Products.COL3.user import COL3PropertySheet

        plugin = self._makeOne()
        sheet = COL3PropertySheet( plugin.getId()
                                 , schema=plugin._getPASSchema()
                                 )

        # This would raise an exception in the standard implementation
        # since "country" is supposed to be a string value.
        sheet.validateProperty('country', False)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(COL3MultiPluginTests),
        ))



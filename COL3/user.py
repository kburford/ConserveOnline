# COL3
# Copyright(C), 2007, Enfold Systems, Inc. - ALL RIGHTS RESERVED
# 
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied 
# this software.  Any inquiries concerning the scope or 
# enforceability of the license should be addressed to:
#
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from AccessControl import ClassSecurityInfo
from BTrees.OOBTree import OOBTree
from Globals import DTMLFile
from Globals import InitializeClass
from zope.interface import implements
from zope import schema

from Products.PlonePAS.plugins.ufactory import PloneUser
from Products.PlonePAS.sheet import MutablePropertySheet
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from Products.COL3.interfaces.user import IUserPropertiesSchema

manage_addCOL3MultiPluginForm = DTMLFile('www/COL3MultiPluginForm', globals())

def manage_addCOL3MultiPlugin(self, id, title='', RESPONSE=None):
    """ Add a COL3 MultiPlugin
    """
    cp = COL3MultiPlugin(id, title)
    self._setObject(cp.getId(), cp)
    if RESPONSE is not None:
        return RESPONSE.redirect('manage_workspace')


class COL3User(PloneUser):
    """ A COL3 user class derived from the standard PloneUser
    """
    # Provided in case we do need to do some overriding
    pass


class COL3PropertySheet(MutablePropertySheet):
    """ A mutable property sheet that does not do its own validation

    Validation has been done by the Zope 3 formlib machinery
    """

    def validateProperty(self, id, value):
        """ Do not perform validation
        """
        pass


class COL3MultiPlugin(BasePlugin):
    """ A PAS multiplugin for COL3
    """
    implements(IUserFactoryPlugin, IPropertiesPlugin)
    security = ClassSecurityInfo()
    meta_type = 'COL3 MultiPlugin'

    def __init__(self, id, title=''):
        self.id = id
        self.title = title or self.meta_type
        self._storage = OOBTree()

    security.declarePrivate('createUser')
    def createUser(self, user_id, name):
        """ Create a user object
        
        Satisfies the PluggableAuthService IUserFactoryPlugin interface
        """
        return COL3User(user_id, name)

    def _getDefaultValues(self, isgroup=None):
        """ Returns a dictionary mapping property names:default values.
        """
        values = {}
        for name in schema.getFieldNamesInOrder(IUserPropertiesSchema):
            attribute = IUserPropertiesSchema.get(name)
            values[attribute.getName()] = attribute.default

        return values

    def _getPASSchema(self):
        """ Translate between the PAS property schema and our interface schema
        """
        schema_map = []
        for name in schema.getFieldNames(IUserPropertiesSchema):
            attribute = IUserPropertiesSchema.get(name)

            if isinstance(attribute, schema.Bool):
                attribute_type = 'boolean'
            else:
                attribute_type = 'string'
            
            schema_map.append((attribute.getName(), attribute_type))

        return schema_map


    def getPropertiesForUser(self, user, request=None):
        """ Return a mapping of properties for this user

        Satisfies the PluggableAuthService IPropertiesPlugin interface
        """
        # If the user is not a PropertiedUser for some reason, bail
        if not IPropertiedUser.providedBy(user):
            return None

        # Retrieve the data and fill in default keys and values if they
        # do not exist.
        defaults = self._getDefaultValues()
        data = self._storage.get(user.getId()) or {}

        for key, val in defaults.items():
            if not data.has_key(key):
                data[key] = val

        # treat fullname specially
        if data['firstname'] is not None and data['lastname'] is not None: 
            data['fullname'] = u' '.join((data['firstname'] or u'',
                                          data['lastname'] or u''))
        else:
            data['fullname'] = data['lastname'] or data['firstname']

        return COL3PropertySheet( self.getId()
                                , schema=self._getPASSchema()
                                , **data
                                )

    def setPropertiesForUser(self, user, propertysheet):
        """Set the properties of a user or group based on the contents of a
        property sheet.
        """
        properties = dict(propertysheet.propertyItems())
        userid = user.getId()
        userprops = self._storage.get(userid)

        # fullname is readonly
        properties.pop('fullname', None)

        if userprops is not None:
            userprops.update(properties)
            self._storage[userid] = self._storage[userid]   # notify persistence machinery of change
        else:
            self._storage.insert(user.getId(), properties)

InitializeClass(COL3MultiPlugin)

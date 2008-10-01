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
from DateTime import DateTime
from plone.i18n.normalizer import urlnormalizer #@UnresolvedImport
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField, LinesField
from Products.Archetypes.public import BooleanField
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View

import workspace

def uncollideId(objId, container):
    currentIds = container.objectIds()
    schemaIds = container.Schema().keys()
    uncollided = objId
    i = 0
    while (not container.checkIdAvailable(uncollided)
           or uncollided in currentIds
           or uncollided in schemaIds
           ):
        uncollided = objId + "-" + str(i)
        i += 1
    return uncollided

def idFromTitle(title, container):
    normalized = urlnormalizer.normalize(title)
    uncollided = uncollideId(normalized, container)
    return uncollided

def generateOID(container):
    oidAlreadyExists = True
    pcat = getToolByName(container, 'portal_catalog')
    oid_prefix = '10.3411/col'
    month_day_time = DateTime().strftime('.%m%d%H%M')
    oid = baseoid = oid_prefix+month_day_time
    i = 1
    libfolderpath = '/'.join(container.getPhysicalPath())
    #XXX this will change once we begin making oid's persistent
    while oidAlreadyExists:
        if pcat.searchResults(path={'query':libfolderpath, 'depth':1}, oid=oid):
            oid = baseoid + "." + str(i)
            i += 1
        else:
            oidAlreadyExists = False
    return oid

class Taxonomy:
    """ mixin for content that participates in taxonomy
        Taxonomy fields: Language, 
                         Country,
                         Biogeographic Realm, 
                         Habitat Type, 
                         Conservation Action, 
                         Direct Threat, <- in edit label spec, not on library screen
                         Monitoring Type, 
                         Genus/Species, <- in edit label, not on library screen
                         Other Searchterms/Keyword (on the front end, Keyword has been replaced by Searchterm, anywhere you 
                                                    see Keyword in the code, this is directly analagous to Searchterm)
    """
    security = ClassSecurityInfo()
    
    schema = Schema((
        StringField('language'),
        StringField('country', index='FieldIndex:schema',),
        StringField('biogeographic_realm'),
        LinesField('habitat',),
        LinesField('conservation',),
        LinesField('directthreat',),
        StringField('organization',),
        LinesField('monitoring',),
        LinesField('keywords',), #Note, in the UI, this is now Search Terms
        ))


    security.declareProtected(View, 'getLibraryKeywords')
    def getLibraryKeywords(self):
        """ Only return keywords if inside the Library
        """
        if 'library' in self.getPhysicalPath():
            return self.getKeywords()
        return ()

    security.declareProtected(View, 'getWorkspaceKeywords')
    def getWorkspaceKeywords(self):
        """ Only return keywords if inside the Workspaces
        """
        if 'workspaces' in self.getPhysicalPath():
            return self.getKeywords()
        return ()


InitializeClass(Taxonomy)


class IsPrivateMixin:
    """ mixin to provide facility to make content private/public"""

    schema = Schema((
        BooleanField('is_private'),
        ))

    # map workflow status to is_private field value
    __status_map = {'private'  : True,
                    'published': False,}
    # map desired is_private field value to workflow transition
    __action_map = {True  : 'hide',
                    False : 'publish'}

    def getIs_private(self, **kw):
        wt = getToolByName(self, 'portal_workflow')
        status = wt.getInfoFor(self, 'review_state')
        value = self.__status_map[status]
        return value

    def setIs_private(self, value, **kw):
        """ Mutator to change workflow state """
        oldvalue = self.getIs_private()
        newvalue = bool(value)
        if newvalue != oldvalue:
            wt = getToolByName(self, 'portal_workflow')
            action = self.__action_map[newvalue]
            wt.doActionFor(self, action)

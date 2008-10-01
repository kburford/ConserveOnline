from AccessControl.SecurityInfo import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.Archetypes.public import registerType

from Products.COL3.content.base import Taxonomy

def addCOLSubscription(self, id, title='', description=''):
    """ Create a new subscription """
    colsub = COLSubscription(id, title=title, description=description)
    self._setObject(id, colsub)

class COLSubscription(ATCTContent):
    """ Content type to hold information for a users subscription information """
    _at_rename_after_creation = True
    myschema = Schema((
         DateTimeField('last_ran',),
         StringField('delivery_method',),
         ))
    security = ClassSecurityInfo()  
    meta_type = portal_type = archetype_name = 'COLSubscription'

    schema = BaseContent.schema.copy() + Taxonomy.schema.copy() + myschema
              
registerType(COLSubscription)
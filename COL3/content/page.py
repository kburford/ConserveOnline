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

from zope.interface import implements
from AccessControl.SecurityInfo import ClassSecurityInfo

from Products.Archetypes.public import Schema, registerType
from Products.Archetypes.public import LinesField
from Products.ATContentTypes.content.document import ATDocument

from Products.COL3.content.base import Taxonomy, IsPrivateMixin
from Products.COL3.content.label import LabelledMixin

from Products.COL3.interfaces.page import IPage

class COLPage(ATDocument, IsPrivateMixin, LabelledMixin):
    """ a Rich Text content type for ConserveOnline
    """
    
    _at_rename_after_creation = True
    implements(IPage)
    myschema = Schema((
         LinesField('document_type',)
         ))
        
    meta_type = portal_type = archetype_name = 'COLPage'
    security = ClassSecurityInfo()
    schema = (ATDocument.schema.copy() +  #@UndefinedVariable
              IsPrivateMixin.schema.copy() + #@UndefinedVariable
              LabelledMixin.schema.copy() + #@UndefinedVariable
              myschema
              )

def addCOLPage(self, id, title='', description=''):
    """ Create a new document
    """
    wg = COLPage(id, title=title, description=description)
    self._setObject(id, wg)

registerType(COLPage)

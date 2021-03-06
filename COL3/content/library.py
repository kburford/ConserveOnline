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

from plone.app.blob.field import BlobMarshaller
from plone.app.blob.content import ATBlob, ATBlobSchema

from Products.Archetypes.public import Schema, registerType
from Products.Archetypes.public import FileField, BooleanField
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import LinesField, ReferenceField
from Products.Archetypes.public import StringField, DateTimeField
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.COL3.content.base import Taxonomy
from Products.COL3.interfaces.library import ILibraryFile

def addLibraryFile(self, id, title='', description=''):
    """ Create a new workgroup
    """
    wg = LibraryFile(id, title=title, description=description)
    self._setObject(id, wg)

class LibraryFile(ATBlob, Taxonomy):
    """ File in the ConserveOnline Library
    """
    implements(ILibraryFile)
    meta_type = portal_type = archetype_name = 'LibraryFile'
    security = ClassSecurityInfo()

    schema = (ATBlobSchema.copy() + #@UndefinedVariable
              Taxonomy.schema.copy() + #@UndefinedVariable
              Schema((LinesField('authors'),
                      LinesField('document_type'),
                      DateTimeField('dateauthored'),
                      StringField('oid'),
                      StringField('license'),
                      FileField('gisdata'),
                      StringField('createdoi')
                      ))
              )
    schema['title'].required = False
    finalizeATCTSchema(schema, folderish=False, moveDiscussion=False)
    schema.registerLayer('marshall', BlobMarshaller())

    def _isIDAutoGenerated(self, id):
        """ Block renaming on setting the file field
        """
        return False

    def getLibraryAuthors(self):
        """ Only return authors if inside the Library
        """
        if 'library' in self.getPhysicalPath():
            return self.getAuthors()
        return ()

registerType(LibraryFile)

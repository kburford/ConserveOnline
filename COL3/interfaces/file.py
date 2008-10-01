# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.schema import Text, TextLine, Choice

from Products.COL3.formlib.schema import File
from Products.COL3.formlib.schema import ChoiceSet
from Products.COL3.formlib.schema import Labels
from Products.COL3.formlib.schema import VocabularyChoice
from Products.COL3 import config
from Products.COL3.validators import validateGISFileMimetype, validateFileSize

class IFileEditSchemaBase(Interface):
    """ Schema with required file upload field """

    file = File(title=u'File',
                description=u'FILE IS STORED - Leave blank unless you want to change the file',
                required=False,
                constraint=validateFileSize)

class IFileSchema(Interface):
    """ Common schema for the Add/Edit views of a page """

    file = File(title=u'File',
                required=True,
                constraint=validateFileSize)

    title = TextLine(title=u'Title',
                     required=True)

    description = Text(title=u'Description',
                       required=True)

    labels = Labels(title=u'Keywords',
                    required=True)

    document_type = ChoiceSet(title=u'Purpose',
                              vocabulary=config.DOCUMENT_TYPE_VOCABULARY,
                              required=False,
                              description=u'Describes the purpose of the document, if applicable.')

    is_private = Choice(title=u'Private?',
                        vocabulary=config.CONTENT_ISPRIVATE_OPTIONS,
                        default=config.CONTENT_ISPRIVATE_DEFAULT,
                        required=False)

    license = VocabularyChoice(
        vocabulary=config.LICENSES_VOCABULARY,
        default=config.LICENCES_DEFAULT,
        title=u"License",
        required=True)
    
    gisdata = File(title=u'GIS Metadata',
                   description=u'To add or update GIS specific metadata (e.g., FGDC metadata) to this file, click the browse button to locate the metadata file on your hard drive.',
                   required=False,
                   constraint=validateGISFileMimetype)

class IFileEditSchema(IFileEditSchemaBase, IFileSchema):
    """ Schema for editing files, with non-required file field """

class IFile(Interface):
    """Marker interface for page objects, to hang views off of"""

class IGISDataFile(Interface):
    """ Marker interface to apply a custom view to gisdata files """

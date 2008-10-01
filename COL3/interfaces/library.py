# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.schema import TextLine, Text, Choice
from zope.app.container.interfaces import IContainer

from Products.COL3 import config
from Products.COL3.formlib.schema import ZDateTime
from Products.COL3.formlib.schema import File
from Products.COL3.formlib.schema import Authors
from Products.COL3.formlib.schema import ChoiceSet
from Products.COL3.formlib.schema import Keywords
from Products.COL3.formlib.schema import VocabularyChoice
from Products.COL3.validators import validateGISFileMimetype


class IDocumentLibrary(IContainer):
    """ Marker interface for the document library
    """

class ILibraryFileEditSchemaBase(Interface):

    file = File(title=u'File',
                description=u'FILE IS STORED - Leave blank unless you want to change the file',
                required=False,
                )

class ILibraryFileSchema(Interface):
    """
    """
    file = File(title=u'File',
                     required=True)

    title = TextLine(title=u'Title',
                     required=True)

    authors = Authors(title=u'Authors',
                      required=True)

    document_type = ChoiceSet(title=u'Purpose',
                              vocabulary=config.DOCUMENT_TYPE_VOCABULARY,
                              required=False,
                              description=u'Describes the purpose of the document, if applicable.')

    description = Text(title=u'Abstract', 
                       description=u'Up to 1000 characters.',
                       required=True)

    language = VocabularyChoice(title=u'Language',
                                vocabulary=config.LANGUAGES_VOCABULARY,
                                default=config.LANGUAGES_DEFAULT,
                                required=True,)

    dateauthored = ZDateTime(title=u'Date authored',
                             required=True,
                             description=u'Select Year : Month : Day')

    country = VocabularyChoice(
        vocabulary=config.NATIONS,
        default=config.NATIONS_DEFAULT,
        title=u"Region/Country",
        required=True)

    biogeographic_realm = VocabularyChoice(
        vocabulary=config.BIOGEOGRAPHIC_REALMS,
        default=config.BIO_REALMS_DEFAULT,
        title=u"Biogeographic realm",
        required=True)

    habitat = ChoiceSet(
        title=u'Habitat type',
        vocabulary=config.HABITAT_VOCABULARY,
        required=False)

    conservation = ChoiceSet(
        title=u'Conservation action',
        vocabulary=config.CONSERVATION_VOCABULARY,
        required=False)

    directthreat = ChoiceSet(
        title=u'Direct threat',
        vocabulary=config.DIRECT_THREAT_VOCABULARY,
        required=False)

    organization = TextLine(title=u'Organization',
        description=u'Examples: The Nature Conservancy, World Wildlife Fund, IUCN.',
        required=False)

    monitoring = ChoiceSet(
        title=u'Monitoring type',
        vocabulary=config.MONITORING_VOCABULARY,
        description=u'The methods used to determine whether the conservation actions described in this document are succeeding.',
        required=False)

    keywords = Keywords(
        title=u'Other Search Terms',
        description=u'Examples: biodiversity, freshwater, Natural Heritage Programs, panthera leo.',
        missing_value=(),
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
    
    createdoi = Choice(title=u"Create DOI?",
                       description=u"Choose whether a DOI should be created for this file or not.",
                       vocabulary=config.GENERATE_DOI_OPTIONS,
                       default=config.GENERATE_DOI_OPTIONS_DEFAULT,
                       required=True) 

class ILibraryFileEditSchema(ILibraryFileEditSchemaBase, ILibraryFileSchema):
    """ Schema for editing a Library File """

class ILibraryFile(Interface):
    """ Marker interface for the library file. To hang views off of """

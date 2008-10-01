from zope import schema
from zope.interface import Interface

from Products.COL3 import config
from Products.COL3.formlib import schema as colschema

class ILabel(Interface):
    """Marker interface for labels, to hang views off of"""

class ILabelEditSchema(Interface):

    title = schema.TextLine(
        title=u'Keyword',
        description=u"""Provide a descriptive name for this keyword.""",
        required=True)
    description = schema.Text(
        title=u'Description',
        description=u"This is the keyword's description and will be displayed with the keyword",
        required=True)
    text = schema.Text(
        title=u'Content',
        description=u"Any text you provide here will appear above the list of documents that have this keyword.",
        required=False)
    footer = schema.Text(
        title=u'Footer',
        description=u"Any text you provide here will appear below the list of documents that have this keyword.",
        required=False)
    language = colschema.VocabularyChoice(
        vocabulary=config.LANGUAGES,
        default=config.LANGUAGES_DEFAULT,
        title=u"Language",
        required=True)
    country = colschema.VocabularyChoice(
        vocabulary=config.NATIONS,
        default=config.NATIONS_DEFAULT,
        title=u"Region/Country",
        required=True)
    biogeographic_realm = colschema.VocabularyChoice(
        vocabulary=config.BIOGEOGRAPHIC_REALMS,
        title=u"Biogeographic Realm",
        default=config.BIO_REALMS_DEFAULT,
        required=True)
    habitat = colschema.ChoiceSet(
        title=u'Habitat type',
        vocabulary=config.HABITAT_VOCABULARY,
        required=False)
    conservation = colschema.ChoiceSet(
        title=u'Conservation action',
        vocabulary=config.CONSERVATION_VOCABULARY,
        required=False)
    directthreat = colschema.ChoiceSet(
        title=u'Direct threat',
        vocabulary=config.DIRECT_THREAT_VOCABULARY,
        required=False)
    organization = schema.TextLine(
        title=u"Organization",
        description=u"Examples: The Nature Conservancy, World Wildlife Fund, IUCN",
        required=False)
    monitoring = colschema.ChoiceSet(
        vocabulary=config.MONITORING_VOCABULARY,
        title=u"Monitoring Type",
        required=False)


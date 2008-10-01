from zope.interface import Interface

from zope.schema import Choice

from Products.COL3 import config
from Products.COL3.formlib.schema import VocabularyChoice, ChoiceSet, Keywords

class ISubscriptionFolder(Interface):
    """ Marker interface for subscriptions folder """

class ISubscriptionSchema(Interface):

    delivery_method = Choice(
        title=u'Preferred Delivery Method',
        vocabulary=config.DELIVERY_CHOICE,
        description=u'If email is selected, the email address in your profile (%s) will be used',
        required=True)
    country = VocabularyChoice(
#        vocabulary=config.NATIONS,
        vocabulary=config.nation_vocab,
#        default=config.NATIONS_DEFAULT,
        default='',
        title=u"Region/Country",
        description=u'GLOBAL refers to those documents tagged as GLOBAL',
        required=False)
    biogeographic_realm = VocabularyChoice(
#        vocabulary=config.BIOGEOGRAPHIC_REALMS,
        vocabulary=config.bio_vocab,
#        default=config.BIO_REALMS_DEFAULT,
        default='',
        title=u"Biogeographic Realm",
        required=False)
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
    monitoring = ChoiceSet(
        vocabulary=config.MONITORING_VOCABULARY,
        title=u"Monitoring Type",
        required=False)
    keywords = Keywords(
        title=u'Keywords',
        description=u'Examples: biodiversity, freshwater, Natural Heritage Programs, panthera leo',
        missing_value=(),
        required=False)


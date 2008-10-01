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

from zope.interface import alsoProvides
from Products.ZCTextIndex.ZCTextIndex import PLexicon, ZCTextIndex, CosineIndex
from Products.ZCTextIndex.HTMLSplitter import HTMLWordSplitter
from Products.ZCTextIndex.Lexicon import CaseNormalizer
from Products.ZCatalog.ZCatalog import manage_addZCatalog
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone import ADD_CONTENT_PERMISSION

from Products.COL3.interfaces.library import IDocumentLibrary
from Products.COL3.interfaces.workspace import IWorkspaceContainer
from Products.COL3.interfaces.subscription import ISubscriptionFolder
from Products.COL3.browser.portal import IAboutFolder
from Products.COL3.user import manage_addCOL3MultiPlugin
from Products.COL3 import config, gsa_config

def setupCaptchas(context):
    """ Install and configure qPloneCaptchas
    """
    if context.readDataFile('col3.txt') is None:
        return

    portal = context.getSite()

    # Is qPloneCaptchas installed? If not, do so now.
    qi = portal.portal_quickinstaller
    if not qi.isProductInstalled('qPloneCaptchas'):
        qi.installProduct('qPloneCaptchas')

    # Set up the correct skins path for dynamic skins
    # The software offers no convenient way to do this
    skinstool = portal.portal_skins
    for skin in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skin)
        new_path=path.replace('plone_captchas/static','plone_captchas/dynamic')
        skinstool.addSkinSelection(skin, new_path)

def setupQuickInstallerDependencies(context):
    if context.readDataFile('col3.txt') is None:
        return
    portal = context.getSite()
    qi = portal.portal_quickinstaller
    for product in config.QUICKINSTALLER_DEPENDENCIES:
        if product and not qi.isProductInstalled(product):
            try:
                qi.installProduct(product)
            except KeyError:
                #import pdb, sys;pdb.post_mortem(sys.exc_info()[2])
                raise

def setupPlacefulWorkflow(context):
    """ Set up a placeful workflow on /workgroups """
    if context.readDataFile('col3.txt') is None:
        return
    portal = context.getSite()

    # Is CMFPlacefulWorkflow installed? If not, do so now.
    qi = portal.portal_quickinstaller
    if not qi.isProductInstalled('CMFPlacefulWorkflow'):
        qi.installProduct('CMFPlacefulWorkflow')
    wg_container = portal.workspaces
    tool = portal.portal_placeful_workflow
    policy_id = 'workgroups_policy'

    # XXX This is just a starting point, the policy will need adjusting
    # XXX based on customer requirements!
    types_in_workgroups = ('Document', 'Event', 'Favorite', 'File', 'Folder',
                           'Image', 'Link', 'News Item', 'Topic',
                           'Large Plone Folder',)

    # Return if already existing
    if policy_id in tool.objectIds():
        return

    # Create a new policy
    tool.manage_addWorkflowPolicy(policy_id, duplicate_id='portal_workflow')
    policy = tool.getWorkflowPolicyById(policy_id)
    policy.setTitle('Workgroups container policy')

    for type_id in types_in_workgroups:
        policy.setChain(type_id, ('transparent_workflow',))

    # Bind the policy to the workgroups container
    dispatcher = wg_container.manage_addProduct['CMFPlacefulWorkflow']
    dispatcher.manage_addWorkflowPolicyConfig()
    config = tool.getWorkflowPolicyConfig(wg_container)
    config.setPolicyIn(policy='')
    config.setPolicyBelow(policy=policy_id)

def setupNotificationCatalog(portal):
    """ This will be used for the notification searches indexed by metadata"""
    catalog_indexes = ({'name':'allowedRolesAndUsers',
                        'type':'KeywordIndex'},
                       {'name':'created',
                        'type':'DateIndex'},
                       {'name':'getLanguage',
                        'type':'FieldIndex'},
                       {'name':'getCountry',
                        'type':'FieldIndex'},
                       {'name':'getBiogeographic_realm',
                        'type':'FieldIndex'},
                       {'name':'getOrganization',
                        'type':'FieldIndex'},
                       {'name':'getHabitat',
                        'type':'KeywordIndex'},
                       {'name':'getConservation',
                        'type':'KeywordIndex'},
                       {'name':'getDirectthreat',
                        'type':'KeywordIndex'},
                       {'name':'getMonitoring',
                        'type':'KeywordIndex'},
                       {'name':'getKeywords',
                        'type':'KeywordIndex'},)
    # These columns are only used by the RSS feed
    catalog_columns = ('Title',
                       'Description',
                       'Creator',
                       'Subject',
                       'created',
                       'Type',)
    portal.notification_catalog.id = 'notification_catalog'
    portal.notification_catalog.title = 'Notification Catalog'
    for column in catalog_columns:
        if column not in portal.notification_catalog.schema():
            portal.notification_catalog.addColumn(column)
    for index in catalog_indexes:
        if index.get('name') not in portal.notification_catalog.indexes():
            portal.notification_catalog.addIndex(index.get('name'), index.get('type'))

def setupPeopleCatalog(portal):
    """ Creating catalog to index simple people objects for searching """
    catalog_indexes = ({'name':'userid',
                        'type':'FieldIndex'},
                       {'name':'firstname',
                        'type':'FieldIndex'},
                       {'name':'lastname',
                        'type':'FieldIndex'},
                       {'name':'organization',
                        'type':'FieldIndex'},
                       {'name':'country',
                        'type':'FieldIndex'},)
    catalog_columns = ('userid',
                       'firstname',
                       'lastname',
                       'organization',
                       'country',)
    if 'people_catalog' not in portal.objectIds():
        manage_addZCatalog(portal, 'people_catalog', 'People Catalog')
        for column in catalog_columns:
            portal.people_catalog.addColumn(column)
        for index in catalog_indexes:
            portal.people_catalog.addIndex(index.get('name'), index.get('type'))
        people_lexicon = PLexicon('people_lexicon', '', HTMLWordSplitter(), CaseNormalizer())
        portal.people_catalog._setObject('people_lexicon', people_lexicon)
        people_zcti = ZCTextIndex('lastname_user',
                                  caller=portal.people_catalog,
                                  index_factory=CosineIndex,
                                  field_name='lastname',
                                  lexicon_id='people_lexicon')
        portal.people_catalog._catalog.addIndex('lastname_user', people_zcti)
    if 'searchableAuthors' not in portal.portal_catalog.indexes():
        auth_zcti = ZCTextIndex('searchableAuthors',
                                 caller=portal.portal_catalog,
                                 index_factory=CosineIndex,
                                 field_name='getAuthors',
                                 lexicon_id='htmltext_lexicon')
        portal.portal_catalog._catalog.addIndex('searchableAuthors', auth_zcti)

### I commented out the bits that actually change stuff ###
def setupTransforms(context):
    if context.readDataFile('col3.txt') is None:
        return
    portal = context.getSite()
    from Products.CMFDefault.utils import VALID_TAGS
    from Products.CMFDefault.utils import NASTY_TAGS

    valid_tags = VALID_TAGS.copy()
    nasty_tags = NASTY_TAGS.copy()

    # calling pop removes the entry
    #nasty_tags.pop('embed')
    #nasty_tags.pop('object')

    # here you can set the values on the keys
    valid_tags['abbr'] = 1
    valid_tags['acronym'] = 1
    valid_tags['address'] = 1
    valid_tags['col'] = 1
    valid_tags['colgroup'] = 1
    valid_tags['tfoot'] = 1
    valid_tags['thead'] = 1

    # Also need to add these table attributes somehow
    # This can be done in Plone site setup on HTML Filtering page
    #lang
    #valign
    #halign
    #border
    #frame
    #rules
    #cellspacing
    #cellpadding
    #bgcolor


    kwargs = {'nasty_tags': nasty_tags,
              'valid_tags': valid_tags}

    transform = getattr(getToolByName(portal, 'portal_transforms'), 'safe_html')

    for k in list(kwargs):
        if isinstance(kwargs[k], dict):
            v = kwargs[k]
            kwargs[k+'_key'] = v.keys()
            kwargs[k+'_value'] = [str(s) for s in v.values()]
            del kwargs[k]

    transform.set_parameters(**kwargs)

def setupInitialContent(context):
    if context.readDataFile('col3.txt') is None:
        return
    portal = context.getSite()
    content = portal.objectIds()
    if 'workspaces' not in content:
        _createObjectByType('Workspaces Container', portal, 'workspaces')
    if 'library' not in content:
        _createObjectByType('Large Plone Folder', portal, 'library')
    if 'about' not in content:
        _createObjectByType('Large Plone Folder', portal, 'about')
    if 'subscriptions' not in content:
        _createObjectByType('Large Plone Folder', portal, 'subscriptions')

    # Set up some marker interfaces to match against views
    alsoProvides(portal.workspaces, IWorkspaceContainer)
    alsoProvides(portal.library, IDocumentLibrary)
    alsoProvides(portal.about, IAboutFolder)
    alsoProvides(portal.subscriptions, ISubscriptionFolder)

    # Do some minor content manipulation
    tool = portal.portal_workflow
    if tool.getInfoFor(portal.library, 'review_state') == 'private':
        tool.doActionFor(portal.library, 'publish')
    if tool.getInfoFor(portal.about, 'review_state') == 'private':
        tool.doActionFor(portal.about, 'publish')
    if tool.getInfoFor(portal.subscriptions, 'review_state') == 'private':
        tool.doActionFor(portal.subscriptions, 'publish')
    portal.subscriptions.manage_role(config.COMMUNITY_MEMBER_ROLE,
                                    (ADD_CONTENT_PERMISSION,))
    portal.library.manage_role(config.COMMUNITY_MEMBER_ROLE,
                               (ADD_CONTENT_PERMISSION,))
    # Add extra stuff to 'about' area
    if 'about' not in portal.objectIds():
        portal.about.invokeFactory('PortalHomeConfig', 'homepageconfig')
        tool.doActionFor(portal.about.homepageconfig, 'publish')
        portal.about.homepageconfig.setTitle('Portal Homepage Configuration')
        portal.about.invokeFactory('Document', 'aboutus')
        tool.doActionFor(portal.about.aboutus, 'publish')
        portal.about.aboutus.setTitle('What Is ConserveOnline?')
    setupNotificationCatalog(portal)
    setupPeopleCatalog(portal)

def setupPAS(context):
    """ Create a COL3 PAS plugin and register it
    """
    if context.readDataFile('col3.txt') is None:
        return
    portal = context.getSite()
    pas = portal.acl_users

    if 'col3_plugin' in pas.objectIds():
        return

    # Create the COL3 plugin
    manage_addCOL3MultiPlugin(pas, 'col3_plugin', title='COL3 Multiplugin')

    # Deactivate the old user factory
    for plugin_id in pas.plugins.listPluginIds(IUserFactoryPlugin):
        pas.plugins.deactivatePlugin(IUserFactoryPlugin, plugin_id)

    # Activate the interesting interfaces from our own plugin
    pas.plugins.activatePlugin(IUserFactoryPlugin, 'col3_plugin')
    pas.plugins.activatePlugin(IPropertiesPlugin, 'col3_plugin')
    # move our plugin above the default property one
    pas.plugins.movePluginsUp(IPropertiesPlugin, ['col3_plugin'])

    # Let the roles plugin know about our new roles
    for r_id in ( config.COMMUNITY_MEMBER_ROLE
                , config.WORKGROUP_MEMBER_ROLE
                , config.WORKGROUP_ADMINISTRATOR_ROLE
                ):
        pas.portal_role_manager.addRole(r_id, title=r_id)

def setupPortalIndexes(context):
    """Add custom indexes/metadata to portal catalog
    """
    if context.readDataFile('col3.txt') is None:
        return
    catalog_columns = ('getDocumentSize',
                       'getDocument_type',
                       'getDateauthored',
                       'getContentType',
                       'getRawFooter',
                       'getRawText',
                       'getCountry',
                       'getAuthors',
                       'getKeywords',
                       )
    catalog_indexes = ({'name':'getDocumentSize',
                        'type':'FieldIndex'},
                       {'name':'getDocument_type',
                        'type':'KeywordIndex'},
                       {'name':'getRawLabels',
                        'type':'KeywordIndex'},
                       {'name':'getAuthors',
                        'type':'KeywordIndex'},
                       {'name':'getLibraryAuthors',
                        'type':'KeywordIndex'},
                       {'name':'getKeywords',
                        'type':'KeywordIndex'},
                       {'name':'getLibraryKeywords',
                        'type':'KeywordIndex'},
                       {'name':'getWorkspaceKeywords',
                        'type':'KeywordIndex'},
                       {'name':'getCountry',
                        'type':'FieldIndex'},
                       {'name':'getWorkspaceCountry',
                        'type':'FieldIndex'},
                       {'name':'getContentType',
                        'type':'FieldIndex'},
                       {'name':'getDateauthored',
                        'type':'FieldIndex'},
                       {'name':'oid',
                        'type':'FieldIndex'},)
    portal = context.getSite()
    pcat = portal.portal_catalog
    # add indexes and metadatas to the portal catalog
    for column in catalog_columns:
        if not column in pcat.schema():
            pcat.addColumn(column)
    for index in catalog_indexes:
        if not index['name'] in pcat.indexes():
            pcat.addIndex(**index)
    pcat.refreshCatalog()

def setupGSATool(context):
    if context.readDataFile('col3.txt') is None:
        return
    portal = context.getSite()
    qi = portal.portal_quickinstaller
    if not qi.isProductInstalled('CachedGSAIndexer'):
        qi.installProduct('CachedGSAIndexer')
    portal_gsa = portal.portal_gsa
    portal_gsa.configureTool(gsa_host=gsa_config.GSA_HOST,
                             gsa_feed_port=gsa_config.GSA_FEED_PORT,
                             gsa_feed=gsa_config.GSA_FEED,
                             threshold=100,
                             qenabled=True)

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
import calendar

from AccessControl.Permissions import add_user_folders
from Products.CMFPlone import ADD_CONTENT_PERMISSION

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import ContentInit
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone import utils as plone_utils
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry
from Products.PluggableAuthService import registerMultiPlugin

from Products.COL3 import config
from Products.COL3.content import indexer
from Products.COL3.content.workspace import Workspace, addWorkspace
from Products.COL3.content.page import COLPage, addCOLPage
from Products.COL3.content.file import COLFile, addCOLFile
from Products.COL3.content.subscription import COLSubscription, addCOLSubscription
from Products.COL3.content.library import LibraryFile, addLibraryFile
from Products.COL3.content.label import Label, addLabel
from Products.COL3.content.portalhomeconfig import PortalHomeConfig, addPortalHomeConfig
#from Products.COL3.content.indexer import setup_gsa
from Products.COL3.permissions import ADD_WORKGROUPS_PERMISSION
from Products.COL3.user import COL3MultiPlugin
from Products.COL3.user import manage_addCOL3MultiPlugin
from Products.COL3.user import manage_addCOL3MultiPluginForm
from Products.COL3.tools.invitations import InvitationsTool
from Products.COL3.tools.joinrequests import JoinRequestsTool
from Products.COL3.tools.crossreference import CrossRefTool

# Register the skins directory
registerDirectory(config.SKINS_DIR, config.GLOBALS)

# Register our PAS plugin
try:
    registerMultiPlugin(COL3MultiPlugin.meta_type)
except RuntimeError:
    # already registered, this happens on refresh
    pass

def initialize(context):
    # activate monkey patches
    from Products.COL3 import patches
    del patches

    tools = (InvitationsTool, JoinRequestsTool, CrossRefTool)

    plone_utils.ToolInit(config.PROJECT_NAME + ' Tool',
                         tools=tools,
                         icon='www/tool.gif',
                        ).initialize(context)


    ContentInit( config.PROJECT_NAME + ' Content'
               , content_types=(Workspace,)
               , permission=ADD_WORKGROUPS_PERMISSION
               , extra_constructors=(addWorkspace,)
               ).initialize(context)

    ContentInit( config.PROJECT_NAME + ' Content'
               , content_types=( COLFile
                               , COLPage
                               , COLSubscription
                               , LibraryFile
                               , Label
                               , PortalHomeConfig
                               )
               , permission=ADD_CONTENT_PERMISSION
               , extra_constructors=( addCOLFile
                                    , addCOLPage
                                    , addCOLSubscription
                                    , addLibraryFile
                                    , addLabel
                                    , addPortalHomeConfig
                                    )
               ).initialize(context)

    context.registerClass( COL3MultiPlugin
                         , permission=add_user_folders
                         , constructors=( manage_addCOL3MultiPluginForm
                                        , manage_addCOL3MultiPlugin
                                        )
                         , visibility=None
                         , icon='www/col3multiplugin.png'
                         )

    profile_registry.registerProfile(
        'default', 'COL3',
        "Installs ConserveOnline3 configuration.",
        'profiles/default', 'COL3', EXTENSION, for_=IPloneSiteRoot,) 

#    setup_gsa()


# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id$

from zope.interface import Interface
from zope.schema import BytesLine
from zope.schema import TextLine
from zope.schema import Text
from zope.schema import Choice
from Products.COL3.formlib.schema import VocabularyChoice, ChoiceSet, Keywords
from zope.app.container.interfaces import IContainer 

from Products.COL3 import config
from Products.COL3.formlib.schema import RichText
from Products.COL3.formlib.schema import File

class IWorkspace(IContainer):
    """ Marker interface for a workgroup
    """

class IPortalHomeConfig(Interface):
    """ Marker interface for the featured workspace
    """

class IWorkspaceContainer(IContainer):
    """ Marker interface for a workgroup
    """

class IWorkspaceNeedsSetup(IWorkspace):
    """ Marker interface for a workspace that needs setup
    """

class IWorkspaceMembers(IContainer):
    """ Marker interface for workspace members folder
        only to register member list view against
    """ 

# marker interface for folders that get created inside the workspace and that
# have specific functions 
class IWorkspaceCalendar(IContainer):
    """ Marker interface for the workspace calendar
    """

class IWorkspaceDocumentsFolder(IContainer):
    """ Marker interface for the documents folder of a workspace
    """

class IWorkspaceImportedDocsFolder(IContainer):
    """ Marker interface for the documents folder of a workspace
    """

class IWorkspaceMemberManagement(Interface):
    """ API for management of members and their roles in a workgroup 
    """
    # XXX update interface to match tool
    def listAllMembers(): #@NoSelf
        """ List members of the workgroup, both regular and managers """

    def listManagerMembers(): #@NoSelf
        """ List managers of the workspace """

    def addMember(): #@NoSelf
        """ Add a community member as a regular workspace member
        """

    def addManager(): #@NoSelf
        """ Add a community member as a workspace manager
        """

class IInviteByEmailSchema(Interface):
    """ Form schema for uploading CSV files to be parsed """
    
    memberEmails = BytesLine(title=u'e-mails of Members to be invited',
                             required=False, missing_value='')

class IInviteByMemberIDSchema(Interface):
    """ Form schema for uploading CSV files to be parsed """
    
    memberIDs = BytesLine(title=u'user ids of Members to be invited',
                             required=False, missing_value='')

class IMemberSearchSchema(Interface):
    """ Form schema for uploading CSV files to be parsed """
    
    name = TextLine(title=u'Search members by their first or last name',
                    required=True)

class IWorkspaceMemberManagementSchema(Interface):
    """ Form schema for promoting/demoting/removing workspace members """

    promoteMembers = BytesLine(title=u'UserIDs of workspace members to promote to managers',
                               required=False, missing_value='')

    demoteMembers = BytesLine(title=u'UserIDs of workspace managers to demote to members',
                              required=False, missing_value='')

    removeMembers = BytesLine(title=u'UserIDs of workspace members to delete',
                              required=False, missing_value='')

class IWorkspaceEditPropertiesSchema(Interface):
    """ Form schema for editing workspace properties """
    title = TextLine(title=u'Workspace Name (up to 75 characters)',
                            description=u"""Examples: Colorado Federal Public Lands Strategy, Western State Trust """
                            u"""Lands, Kenya's Biodiversity Mapping Project.""",
                            max_length=75,
                            required=True) 
    workspacelogo = File(title=u'Logo',
                         description=u'An image in PNG format to identify your workspace.',
                         required=False)
    workspaceicon = File(title=u'Icon',
                         description=u'A 32x32 pixel image to identify your workspace (if this is left blank the logo file above (if supplied) will be used for the icon image)',
                         required=False)
    remove_logo = Choice(title=u"Remove Logo?",
                         description=u"Remove the uploaded logo and return the icon to the default.",
                         vocabulary=config.WORKGROUP_REMOVELOGO_OPTIONS,
                         default=config.WORKGROUP_REMOVELOGO_DEFAULT,
                         required=True)   
    description = Text(title=u'Purpose',
                       description=u"This description will appear on the home page of your workspace",
                       max_length=250,
                       required=False)
    content = RichText(title=u'Content',
                       required=False)
    is_private = Choice(title=u"Is the workspace public or private?",
                        vocabulary=config.WORKGROUP_ISPRIVATE_OPTIONS,
                        default=config.WORKGROUP_ISPRIVATE_DEFAULT,
                        required=True)
    language = VocabularyChoice(
               vocabulary=config.LANGUAGES,
               default=config.LANGUAGES_DEFAULT,
               title=u"Language",
               required=True)
    country = VocabularyChoice(
              vocabulary=config.NATIONS,
              default=config.NATIONS_DEFAULT,
              title=u"Region/Country",
              required=True)
    biogeographic_realm = VocabularyChoice(
              vocabulary=config.BIOGEOGRAPHIC_REALMS,
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
             description=u"Examples: The Nature Conservancy, World Wildlife Fund, IUCN.",
             required=False)
    monitoring = ChoiceSet(
             title=u'Monitoring type',
             vocabulary=config.MONITORING_VOCABULARY,
             description=u'The methods used to determine whether the conservation actions described in this document are succeeding',
             required=False)
    keywords = Keywords(
            title=u'Other Search Terms',
            description=u'Examples: biodiversity, freshwater, Natural Heritage Programs, panthera leo',
            missing_value=(),
            required=False)
    license = VocabularyChoice(
              vocabulary=config.LICENSES_VOCABULARY,
              default=config.LICENCES_DEFAULT,
              title=u"License",
              required=True)

class ICancelInvitationSchema(Interface):
    """ Form schema for promoting/demoting/removing workspace members """

    invitationIds = BytesLine(title=u'Invitation IDs of invitations to cancel',
                              required=False, missing_value='')

class IReSendInvitationSchema(Interface):
    """ Form schema for promoting/demoting/removing workspace members """

    invitationIds = BytesLine(title=u'Invitation IDs of invitations to re-send',
                              required=False, missing_value='')

class IWorkspaceJoinSchema(Interface):
    """ Form schema allowing a person to request joining a workspace"""
    reason = Text(title=u'Join A Workspace', 
                  description=u'The reason for wanting to join a group',
                  required=True)

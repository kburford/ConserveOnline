# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope import schema
from Products.CMFPlone.interfaces.basetool import IPloneBaseTool

class IInvitationManager(IPloneBaseTool):
    """ Marker interface for the invitations manager tool
    """

class IInvitation(Interface):
    """ Interface for the invitations themselves """

    workspaceID = schema.BytesLine(
        description=u"ID of the workspace to which the member is being invited"
    )
    inviterID = schema.BytesLine(
        description=u"user id of the member who sent the invitation"
    )
    email = schema.BytesLine(
        description=u"e-mail address of the invited member"
    )

class IJoinRequestsManager(IPloneBaseTool):
    """ Marker interface for the join requests manager tool
    """

class IJoinRequest(Interface):
    """ Interface for the join request """

class ICrossReference(Interface):
    """ Interface for the CrossRef tool"""

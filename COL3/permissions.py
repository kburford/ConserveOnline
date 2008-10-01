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

from Products.CMFCore.permissions import setDefaultRoles
from Products.COL3.config import WORKGROUP_MEMBER_ROLE
from Products.COL3.config import COMMUNITY_MEMBER_ROLE
from Products.COL3.config import WORKGROUP_ADMINISTRATOR_ROLE

ADD_WORKGROUPS_PERMISSION = 'Add workgroups'
setDefaultRoles(ADD_WORKGROUPS_PERMISSION, ('Manager', COMMUNITY_MEMBER_ROLE))

VIEW_PROFILE_PERMISSION = 'COL: View Community Member Profile'
setDefaultRoles(ADD_WORKGROUPS_PERMISSION, ('Manager', COMMUNITY_MEMBER_ROLE))

MANAGE_PROFILE_PERMISSION = 'COL: Manage Community Member Profile'
setDefaultRoles(MANAGE_PROFILE_PERMISSION, ('Manager',))

LIST_WORKSPACE_MEMBERS_PERMISSION = 'COL: List Workspace Members'
setDefaultRoles( LIST_WORKSPACE_MEMBERS_PERMISSION
               , ('Manager', WORKGROUP_MEMBER_ROLE)
               )

MANAGE_WORKSPACE_PERMISSION = 'COL: Manage Workspace'
setDefaultRoles( MANAGE_WORKSPACE_PERMISSION
               , ('Manager', WORKGROUP_ADMINISTRATOR_ROLE)
               )

from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName

def applyCommunityMemberRoles(self):
    portal = self
    p_mem = getToolByName(self, 'portal_membership')
    p_role_mgr = portal.acl_users.portal_role_manager
    roles_added = StringIO()
    roles_added.seek(0)
    memberlist = [member.id for member in p_mem.listMembers()]
    portal.manage_delLocalRoles(memberlist)
    roles_added.write('Adding Community Member roles...\n')
    for member in memberlist:
        roles_added.write('Added role for '+member+'\n')
        p_role_mgr.assignRoleToPrincipal('Community Member', member)
    roles_added.write('Added Community Member roles for '+str(len(memberlist))+' members')
    roles_added.seek(0)
    return roles_added.read()
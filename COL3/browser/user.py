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

from cgi import parse_qs
from zope.formlib.form import action
from zExceptions import NotFound
from xml.parsers.expat import ExpatError
from smtplib import SMTPRecipientsRefused
from Products.COL3.etree import fromstring
from Products.COL3.etree import Element, SubElement

from DateTime import DateTime
from zExceptions import Redirect
from zExceptions import BadRequest
from zope.formlib import form
from Acquisition import aq_inner, aq_parent
from AccessControl.SecurityManagement import newSecurityManager

from Products.CMFCore.utils import getToolByName

from Products.COL3.config import CHARSET, COL_ADMIN
from Products.COL3.content.indexer import index as gsa_index
from Products.COL3.content.indexer import reindex as gsa_reindex
from Products.COL3.browser.mail import simple_mail_tool
from Products.COL3.browser.base import SafeRedirect
from Products.COL3.browser.base import createViewNode
from Products.COL3.browser.base import Page, Fragment
from Products.COL3.browser.utils import getBaseUrl, strip
from Products.PasswordResetTool.PasswordResetTool import PasswordResetTool
from Products.COL3.interfaces.user import IEditBioSchema, IUserPreferencesSchema
from Products.COL3.interfaces.user import IUserRegistrationSchema, IResetPasswordSchema
from Products.COL3.browser.common import COMMON_VIEWS
from Products.COL3.browser.member import MemberWorkspacesMixin
from Products.COL3.formlib.xmlform import NO_VALIDATION
from Products.COL3.formlib.xmlform import ResetPasswordFormFragment
from Products.COL3.formlib.xmlform import EditFormFragment, AddFormFragment
from Products.COL3.browser.common import cleanup
from Products.COL3.browser.common import COMMON_VIEWS_NORESOURCE
from Products.COL3.browser.people import PersonObj
from Products.COL3.interfaces.user import IPasswordResetSchema
from Products.COL3.interfaces.subscription import ISubscriptionSchema
from Products.COL3.Extensions.process_subscriptions import process_subscription
from Products.COL3.permissions import MANAGE_PROFILE_PERMISSION

def getPersonObj(member):
    return PersonObj(member.getId(),
                     strip(member.getProperty('firstname') and
                           member.getProperty('firstname') or
                          'None Given'),
                     strip(member.getProperty('lastname') and
                           member.getProperty('lastname') or
                          'None Given'),
                     strip(member.getProperty('country') and
                           member.getProperty('country') or
                          'None Given'),
                     strip(member.getProperty('organization') and
                           member.getProperty('organization') or
                          'None Given'),)

class ViewProfileFragment(Fragment):
    """ fragment that gets the user's profile"""
    def asElement(self):
        context = self.context
        request = self.request
        baseurl = getBaseUrl(context, request)
        pmem = getToolByName(context, 'portal_membership')
        authuser = pmem.getAuthenticatedMember()
        userid = request.get('userid', '')
        user = pmem.getMemberById(userid)
        if userid and user is None:
            raise NotFound('No user found for id: ' + userid)
        root = Element('profile')
        editprofile_url = ''
        editbio_url = ''
        if authuser.id == userid:
            editprofile_url = '%s%s' % (baseurl,'edit-profile.html')
            editbio_url = '%s%s' % (baseurl,'edit-bio.html')
        elif authuser.id == COL_ADMIN:		#.getUser().has_permission(MANAGE_PROFILE_PERMISSION, authuser):
            editprofile_url = '%s%s%s' % (baseurl,'edit-profile.html?userid=',userid)
            editbio_url = '%s%s%s' % (baseurl,'edit-bio.html?userid=',userid)
        aboutelem = SubElement(root,
                               'about',
                               {'href': editprofile_url})
        if pmem.getPersonalPortrait(user.getId()).id != 'defaultUser.gif':
            SubElement(aboutelem,'portrait',
                       href=pmem.getPersonalPortrait(user.getId()).absolute_url())
        if authuser.id == userid or authuser.id == COL_ADMIN: 	
            SubElement(aboutelem, 'email').text = user.getProperty('email')
        SubElement(aboutelem, 'userid').text = userid
        SubElement(aboutelem, 'firstname').text = user.getProperty('firstname')
        SubElement(aboutelem, 'lastname').text = user.getProperty('lastname')
        SubElement(aboutelem, 'password').text = '********'
        SubElement(aboutelem, 'country').text = user.getProperty('country')
        SubElement(aboutelem, 'background').text = user.getProperty('background')
        org = user.getProperty('organization')
        SubElement(aboutelem, 'organization').text = org and org or 'None Given'
        SubElement(aboutelem, 'organizationtype').text = user.getProperty('organizationtype')
        SubElement(aboutelem, 'joined').text = user.getProperty('join_date')
        elem = SubElement(aboutelem, 'bio', {'href': editbio_url})
        if user.getProperty('description'):
            description = None
            try:
                description = fromstring(user.getProperty('description'))
            except ExpatError:
                description = cleanup(user.getProperty('description'))
            elem.append(description)
        return root

class UserInvitationPortletFragment(Fragment):
    """ This portlet displays a user's outstanding workspace invitations"""
    def asElement(self):
        context = self.context
        request = self.request
        pmem = getToolByName(context, 'portal_membership')
        userid = request.get('userid', '')
        mem = pmem.getMemberById(userid)
        root = Element('portlet', {'title':'My Invitations', 'type':'invitations'})
        if mem:
            invtool = getToolByName(context, 'workspace_invitations')
            invites = invtool.getInvitationsForEmail(mem.getProperty('email'))
            if invites:
                for invite in invites:
                    if invite:
                        workspace = invtool.getWorkspaceFor(invite)
                        accept_invite_url = '%s/%s?id=%s' % (workspace.absolute_url(),'accept-invitation.html', invite.id)
                        resourceelem = SubElement(root, 'resource', {'href':accept_invite_url})
                        SubElement(resourceelem, 'title').text = workspace.title_or_id()
                        inviter = pmem.getMemberById(invite.getProperty('inviterID'))
                        inviterFullName = inviter.getProperty('firstname')+' '+inviter.getProperty('lastname')
                        SubElement(resourceelem, 'manager').text = inviterFullName
                        inviteDate = invite.getProperty('lastSent')
                        if inviteDate:
                            inviteDate = inviteDate.ISO8601()
                        SubElement(resourceelem, 'created').text = inviteDate
            return root

class UserWorkspacesPortletFragment(Fragment, MemberWorkspacesMixin):
    """ This portlet lists the workspaces a user is a member of"""
    def asElement(self):
        context = self.context
        request = self.request
        pmem = getToolByName(context, 'portal_membership')
        userid = request.get('userid', '')
        member = pmem.getMemberById(userid)
        authmember = pmem.getAuthenticatedMember()
        mgr_ws_ids, member_ws_ids = self._getMemberWorkspaceIds(member)
        portlet_title = 'My Workspaces'
        if not userid == authmember.id:
            portlet_title = 'Member of Workspaces'
        root = Element('portlet', {'title':portlet_title, 'type':'workspaces'})
        if mgr_ws_ids or member_ws_ids:
            mgrworkspaces = self._workspaceRecordsFromIds(mgr_ws_ids)
            memberworkspaces = self._workspaceRecordsFromIds(member_ws_ids)
            workspaces = []
            for ws in mgrworkspaces:
                if ws:
                    href = ''
                    if getattr(ws, 'getURL', None) is not None:
                        href = ws.getURL()
                    else:
                        href = ws.absolute_url()
                    resourceelem = SubElement(root, 'resource',
                                      {'href':href})
                    title = ws.Title and ws.Title or ws.id
                    SubElement(resourceelem, 'title').text = title
                    workspaces.append(ws.id)
                    SubElement(resourceelem, 'status').text = 'Manager'
                    SubElement(resourceelem, 'created').text = ws.created.ISO8601()
            for ws in memberworkspaces:
                if ws:
                    title = ws.Title and ws.Title or ws.id
                    href = ''
                    if getattr(ws, 'getURL', None) is not None:
                        href = ws.getURL()
                    else:
                        href = ws.absolute_url()
                    try:
                        workspaces.index(ws.id)
                    except ValueError:
                        #value is not in the list so add it to the results
                        resourceelem = SubElement(root, 'resource',
                                          {'href':href})
                        SubElement(resourceelem, 'title').text = title
                        SubElement(resourceelem, 'status').text = 'Member'
                        SubElement(resourceelem, 'created').text = ws.created.ISO8601()
        return root

class ViewProfilePortletFragment(Fragment):
    """"""
    def asElement(self):
        context = self.context
        request = self.request
        root = Element('portlets')
        invitefrag = UserInvitationPortletFragment(context, request)
        wsfrag = UserWorkspacesPortletFragment(context, request)
        pmem = getToolByName(context, 'portal_membership')
        userid = request.get('userid', '')
        authmember = pmem.getAuthenticatedMember()
        if userid == authmember.id:
            root.append(invitefrag.asElement())
        root.append(wsfrag.asElement())
        return root

class ViewProfileViewFragment(Fragment):
    """<view name="profile.html" type="profile" title="My Profile" section="people"/>"""
    def asElement(self):
        pmem = getToolByName(self.context, 'portal_membership')
        userid = self.request.get('userid', '')
        authmember = pmem.getAuthenticatedMember()
        if userid == authmember.id:
            title = 'My Profile'
        else:        
            member = pmem.getMemberById(userid)
            fname = member.getProperty('firstname')
            lname = member.getProperty('lastname')
            title = 'Profile for ' + fname + ' ' + lname
        return Element('view',
                       name='profile.html',
                       type='profile',
                       title=title,
                       section='people')

class EditMenuFragment(Fragment):
    """ fragment to add the edit menu
    """
    def asElement(self):
        pmem = getToolByName(self.context, 'portal_membership')
        memberid = self.request.get('userid', '')
        member = pmem.getMemberById(memberid)
        authmember = pmem.getAuthenticatedMember()
        #if authmember.id == COL_ADMIN:		#.has_permission(MANAGE_PROFILE_PERMISSION, authmember):
        href = '%s%s' % ('edit-profile.html?userid=',memberid)
        #else:
        #    href = 'edit-profile.html'
        root = Element('menus')
        menuelem = SubElement(root, 'actionmenu')
        SubElement(menuelem, 'entry', {'href':href}).text = 'Edit'
        return root

class ViewProfilePage(Page):

    views = COMMON_VIEWS

    def __call__(self):
        ADDITIONAL_VIEWS = (ViewProfileViewFragment,
                            ViewProfileFragment,
                            ViewProfilePortletFragment,)
        context = self.context
        request = self.request
        pmem = getToolByName(context, 'portal_membership')
        memberid = request.get('userid', '')
        member = pmem.getMemberById(memberid)
        authmember = pmem.getAuthenticatedMember()
        if member and authmember:
            if member.id == authmember.id or authmember.id == COL_ADMIN:	
                ADDITIONAL_VIEWS = ADDITIONAL_VIEWS + (EditMenuFragment, )
        self.views = self.views + ADDITIONAL_VIEWS
        return super(ViewProfilePage, self).__call__()

    def getResponse(self):
        """ Overriding to set some variables"""
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        request = self.request
        memberid = request.get('userid', '')
        member = pmem.getMemberById(memberid)
        authmember = pmem.getAuthenticatedMember()
        try:
            fname = member.getProperty('firstname')
        except:
            fname = ""
        lname = member.getProperty('lastname')
        if member and authmember and member.id == authmember.id:
            title = 'My Profile - '
        else:
            title = 'Profile for '
        self.xtra_breadcrumb_ids = ({'title':title+fname+' '+lname,
                                     'href':''}, ) #don't really "need" href, here for illustrative purposes
        return super(ViewProfilePage, self).getResponse()

######################################
### classes for view profile end   ###
######################################

########################################
###      Begin ResetPassword         ###
########################################

class ResetPasswordViewFragment(Fragment):
    """" View fragment for password reset page """
    def asElement(self):
        return Element('view',
                       name="reset-password.html",
                       type="site",
                       title="Reset Password",
                       section="people"
                       )

class ResetPasswordForm(ResetPasswordFormFragment):
    """"""
    form_fields = form.FormFields(IResetPasswordSchema)

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)
        putils = getToolByName(context, 'plone_utils')
        if data is None:
            return
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getMemberById(data['username'].encode('ascii'))
        if member:
            prt = getToolByName(context, PasswordResetTool.id)
            resetReq = prt.requestReset(data['username'].encode('ascii'))
            smt = simple_mail_tool()
            try:
                querystr = '/completereset-password.html?key='+resetReq['randomstring']
                url = self.context.absolute_url()+querystr
                smt.sendPasswordResetEmail(context, url, member.getProperty('email'))
                raise SafeRedirect(self.context.absolute_url()+'/confirmreset-password.html?username='+data['username'])
            except SMTPRecipientsRefused:
                putils.addPortalMessage('Email was unable to be sent, please try again...')
                raise SafeRedirect(self.context.absolute_url()+'/reset-password.html')
        else:
            putils.addPortalMessage('No user found for id '+data['username'])
            raise SafeRedirect(self.context.absolute_url()+'/reset-password.html')
        return context.absolute_url().replace("https://","http://")

    def cancelURL(self):
        return self.context.absolute_url().replace("https://","http://")

class ResetPasswordPage(Page):
    """The view for resetting a user's password"""
    views = (ResetPasswordViewFragment, ResetPasswordForm, ) + COMMON_VIEWS

########################################
###        End ResetPassword         ###
########################################

########################################
###      Begin ResetPassword         ###
########################################

class CompleteResetPasswordViewFragment(Fragment):
    """" View fragment for view that user enters the new password on """
    def asElement(self):
        return Element('view',
                       name="completereset-password.html",
                       type="site",
                       title="Reset Password",
                       section="people"
                       )

class CompleteResetPasswordForm(AddFormFragment):
    """ """
    form_fields = form.FormFields(IPasswordResetSchema)

    def createAddAndReturnURL(self, data):
        context = self.context
        request = self.request
        userid = request.get('form.username', '')
        password = request.get('form.password', '')
        querystr = self.request.get('QUERY_STRING')
        key = querystr[querystr.index('=')+1:]
        prt = getToolByName(context, PasswordResetTool.id)
        try:
            prt.resetPassword(userid, key, password)
        except Exception, e:
            getToolByName(context, 'plone_utils').addPortalMessage('Failed to reset password, please try again. ('+e+')')
            raise SafeRedirect(context.absolute_url()+'/completereset-password.html')
        ## log the user in with the newly created password
        self.request.form['__ac_name'] = userid
        self.request.form['__ac_password'] = password
        acl_users = getToolByName(self.context, 'acl_users')
        # Switch security context to the user
        ascuserid=userid
        if isinstance(userid, (str,unicode)):
            ascuserid=ascuserid.encode('ascii')
        user = acl_users.getUserById(ascuserid).__of__(acl_users)
        newSecurityManager(self.request, user)
        # set the cookies
        acl_users.credentials_cookie_auth.login()
        # and the login times
        mtool = getToolByName(self.context, 'portal_membership')
        mtool.setLoginTimes()
        url = self.context.absolute_url()+'/view-profile.html?userid='+userid
        return url.replace("https://","http://")

    def cancelURL(self):
        return self.context.absolute_url().replace("https://","http://")

class CompleteResetPasswordPage(Page):
    """The view for resetting a user's password"""
    views = (CompleteResetPasswordViewFragment,
             CompleteResetPasswordForm, ) + COMMON_VIEWS

########################################
###        End ResetPassword         ###
########################################

########################################
###    Start ConfirmResetPassword    ###
########################################

class ConfirmResetPasswordViewFragment(Fragment):
    def asElement(self):
        """ View fragment for confirm password reset """
        context = self.context
        request = self.request
        queryStr = request.get('QUERY_STRING')
        userid = queryStr[queryStr.index('=')+1:]
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getMemberById(userid)
        emailaddress = member.getProperty('email', '')
        viewelem =  Element('view',
                            name='confirmreset-password.html',
                            type='site',
                            title='Reset Password',
                            section='people')
        SubElement(viewelem, 'resetemail').text = emailaddress
        return viewelem

class ConfirmResetPasswordPage(Page):
    views = (ConfirmResetPasswordViewFragment, ) + COMMON_VIEWS

########################################
###     End ConfirmResetPassword     ###
########################################

########################################
### classes for edit name/desc start ###
########################################

class UserEditNameDescViewFragment(Fragment):
    """ <view name="edit.html" type="namedescription" title="About Me" section="people"/> """
    def asElement(self):
        pmem = getToolByName(self.context, 'portal_membership')
        userid = self.request.get('userid', '')
        try:
       	    member = pmem.getMemberById(userid)
        except AttributeError:
            member = pmem.getAuthenticatedMember()
        name = member.getProperty('firstname') +' '+member.getProperty('lastname')
        viewattribs = {'name':'edit.html',
                       'type':'profile',
                       'title':'Edit Profile: '+name,
                       'section':'people'}
        return createViewNode(viewattribs)

class UserEditNameDescForm(EditFormFragment):
    """This produces the formcontroller fragment"""
    form_fields = form.FormFields(IUserPreferencesSchema, omit_readonly=True)

    def getDataFromContext(self):
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        userid = self.request.get('userid', '')
        member = pmem.getMemberById(userid)
        #member = pmem.getAuthenticatedMember()
        data = {}
        data['userid'] = userid
        if member.getProperty('firstname'):
            data['firstname'] = member.getProperty('firstname')
        if member.getProperty('lastname'):
            data['lastname'] = member.getProperty('lastname')
        if member.getProperty('country'):
            data['country'] = member.getProperty('country')
        if member.getProperty('organization'):
            data['organization'] = member.getProperty('organization')
        if member.getProperty('organizationtype'):
            data['organizationtype'] = member.getProperty('organizationtype')
        if member.getProperty('background'):
            data['background'] = member.getProperty('background')
        if member.getProperty('email'):
            data['email'] = member.getProperty('email')
        if member.getProperty('description'):
            data['description'] = member.getProperty('description')
        data['portrait'] = None
        return data

    def applyChangesAndReturnURL(self, data):
        """ Handle preferences changes
        """
        context = self.context
        membership_tool = getToolByName(context, 'portal_membership')
        userid = self.request.get('userid', '')
        member = membership_tool.getMemberById(userid)
        #member = membership_tool.getAuthenticatedMember()
        # portrait is dealt with specially:
        portraitfile = data['portrait']
        del data['portrait']
        member.setMemberProperties(data)
        member_id = member.getId()
        gsa_reindex(member)

        if portraitfile is not None:
            membership_tool.changeMemberPortrait(portraitfile, member_id)
        if data.get('password') and data.get('confirm_password'):
            membership_tool.setPassword(data['password'])
        self.context.people_catalog.catalog_object(getPersonObj(member))
        # XXX set status in the message-status infrastructure
        self.status = u'Preferences changed for user %s' % member_id
        url = '%s/view-profile.html?userid=%s' % (context.absolute_url(), member_id)
        return url.replace("https://","http://")

    def cancelURL(self):
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        userid = self.request.get('userid', '')
        member = pmem.getMemberById(userid)
        #member = pmem.getAuthenticatedMember()
        url = '%s/view-profile.html?userid=%s' % (context.absolute_url(), member.getId())
        # force back into http if in https
        return url.replace("https://","http://")

class UserEditNameDescView(Page):
    views = (UserEditNameDescViewFragment, UserEditNameDescForm, ) + COMMON_VIEWS

######################################
### classes for edit name/desc end ###
######################################

###########################################
### classes for Accept Invitation start ###
###########################################

class AcceptInvitationViewFragment(Fragment):
    """ <view name='accept-invitation.html' type='people' title='Join Workspace' section='people'/> """
    def asElement(self):
        context = aq_inner(self.context)
        request = self.request
        membertool = getToolByName(context, 'portal_membership')
        invitetool = getToolByName(context, 'workspace_invitations')
        member = membertool.getAuthenticatedMember()
        baseurl = getBaseUrl(context, request)
        mode = request.get('mode', None)
        inviteId = self.request.get('id')
        if mode is not None:
            self._processInvitation(member, baseurl, mode, invitetool, inviteId)
        viewattribs = {'name':'accept-invitation.html',
                       'type':'people',
                       'title':'Invitation to Join Workspace',
                       'section':'people',}
        viewnode = createViewNode(viewattribs)
        querystr = '/accept-invitation.html?id=%s&mode=' % inviteId
        url = context.absolute_url()
        SubElement(viewnode, 'accept', href='%s%s%s' % (url, querystr, 'accept'))
        SubElement(viewnode, 'reject', href='%s%s%s' % (url, querystr, 'reject'))
        SubElement(viewnode, 'cancel', href='%s%s%s' % (url, querystr, 'cancel'))
        return viewnode

    def _processInvitation(self, member, baseurl, mode, invitationtool, invId):
        memberid = member.getId()
        profileurl = '%s%s%s' % (baseurl, 'view-profile.html?userid=', memberid)
        if mode == 'accept':
            invalid = invitationtool.acceptInvitation(invId, member)
            if invalid:
                raise BadRequest('Invitation id is not valid: '+ invId)
            raise SafeRedirect(profileurl)
        elif mode == 'reject':
            invalid = invitationtool.rejectInvitation(invId)
            if invalid:
                raise BadRequest('Invitation id is not valid: '+ invId)
            raise SafeRedirect(profileurl)
        elif mode == 'cancel':
            raise SafeRedirect(profileurl)

class AcceptInvResourceFragment(Fragment):
    def asElement(self):
        root = None
        context = self.context
        inviteId = self.request.get('id')
        invitetool = getToolByName(context, 'workspace_invitations')
        invitation = invitetool.getInvitationById(inviteId)
        if invitation:
            root = Element('resource')
            pmem = getToolByName(context, 'portal_membership')
            pcat = getToolByName(context, 'portal_catalog')
            workspace = pcat.searchResults(type='Workspace',
                                           id=invitation.workspaceID)
            title = ''
            if workspace:
                title = workspace[0].Title and workspace[0].Title or workspace[0].id
            else:
                title = invitation.workspaceID
            SubElement(root, 'title').text = title
            member = pmem.getMemberById(invitation.inviterID)
            firstname = member.getProperty('firstname')
            lastname = member.getProperty('lastname')
            SubElement(root, 'manager').text = '%s %s' % (firstname, lastname)
        return root

class AcceptInviationView(Page):

    views = (AcceptInvitationViewFragment,
             AcceptInvResourceFragment) + COMMON_VIEWS_NORESOURCE

#########################################
### classes for Accept Invitation end ###
#########################################

###############################################
### classes for Add User Registration Start ###
###############################################

class AddRegistrationViewFragment(Fragment):
    """<view name="add-registration.html" type="registration" title="Register"
             section="people" />"""
    def asElement(self):
        # it's for anonymous only
        context = aq_inner(self.context)
        if not getToolByName(context,
                             'portal_membership').isAnonymousUser():
            raise Redirect(context.absolute_url())
        return Element('view',
                       name="add-registration.html",
                       type="registration",
                       title="Register",
                       section="people")

class AddRegistrationFormFragmentBase(AddFormFragment):
    """formcontroller fragment for adding a registration"""

    form_fields = form.FormFields(IUserRegistrationSchema, omit_readonly=True)

    def cancelURL(self):
        # force back into http if in https
        return self.context.absolute_url().replace('https://',
                                                   'http://')

    def destinationURLForMember(self, member):
        url = (self.context.absolute_url() +
               "/view-profile.html?userid=" + member.getId())
        # force back into http if in https
        return url.replace("https://","http://")

    def addProfileAndLogin(self, data):
        # Munge the data so the registration tool can deal with it
        data['id'] = data['username']
        # The standard mechanism may have trouble dealing with the unicode
        # values sent back by the Zope 3 form handling, so converting
        # a few here:
        encoding = CHARSET
        for key in ('password', 'confirm'):
            if isinstance(data[key], unicode):
                data[key] = data[key].encode(encoding)
        data['join_date'] = DateTime().ISO8601()
        registration_tool = getToolByName(self.context, 'portal_registration')
        registration_tool.addMember( data['id']
                                   , data['password']
                                   , properties=data
                                   )
        #add person to the people_catalog for use in browsing people pages
        membership_tool = getToolByName(self.context, 'portal_membership')
        member = membership_tool.getMemberById(data['id'])
        self.context.people_catalog.catalog_object(getPersonObj(member))
        # give the user the proper roles
        prole_mgr = self.context.acl_users.portal_role_manager
        prole_mgr.assignRoleToPrincipal('Community Member', data['id'])

        # set the credential cookie
        self.request.form['__ac_name'] = data['id']
        self.request.form['__ac_password'] = data['password']
        acl_users = getToolByName(self.context, 'acl_users')
        # Switch security context to the user
        user = acl_users.getUserById(data['id']).__of__(acl_users)
        newSecurityManager(self.request, user)
        # set the cookies
        acl_users.credentials_cookie_auth.login()
        # and the login times
        mtool = getToolByName(self.context, 'portal_membership')
        mtool.setLoginTimes()
        # XXX Add status message

class AddRegistrationFormFragment(AddRegistrationFormFragmentBase):

    def createAddAndReturnURL(self, data):
        self.addProfileAndLogin(data)
        context = aq_inner(self.context)
        # redirect to the just created user profile
        member = getToolByName(context,
                               'portal_membership').getAuthenticatedMember()
        url = self.destinationURLForMember(member)
        return url

    @form.action("Register", name="register")
    def handle_add(self, action, data): #@UnusedVariable
        url = self.createAddAndReturnURL(data)
        raise SafeRedirect(url)

    @form.action("Cancel", name="cancel", validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())

class AddRegistrationPage(Page):
    views = (AddRegistrationViewFragment,
             AddRegistrationFormFragment,) + COMMON_VIEWS

def getInvitationIdFromRequest(request):
    qstring = request.get('QUERY_STRING', '')
    qparams = parse_qs(qstring)
    invitation_id, = qparams.get('invitationid', (None,))
    return invitation_id

class InvitationAddRegistrationViewFragment(Fragment):
    """
    <view name="add-registration.html" type="registration" title="Register"
             section="people">
        <invitation id="08098430">
            <workspace title="California Birds"
                       href="/workspaces/california-birds"/>
            <inviter>Kathy Adams</inviter>
        </invitation>
    </view>
    """

    def asElement(self):
        request = self.request
        context = aq_inner(self.context)
        invitation_id = getInvitationIdFromRequest(request)
        # there must be an invitation in the request
        if invitation_id is None:
            raise BadRequest("No invitationid provided")
        #and it must exist
        invtool = getToolByName(context, 'workspace_invitations')
        invitation = invtool.get(invitation_id, None)
        if invitation is None:
            raise BadRequest("Invitation id is not valid: " + invitation_id)
        # it's for anonymous only
        if not getToolByName(context,
                             'portal_membership').isAnonymousUser():
            # authenticated users should go straight to the
            # accept invitation form
            raise Redirect(context.absolute_url() +
                           "/accept-invitation.html?id=" +
                           invitation_id)

        view_tag = Element('view',
                           name="add-registration.html",
                           type="registration",
                           title="Register",
                           section="people")
        invitation_tag = SubElement(view_tag, 'invitation', id=invitation_id)
        workspace = invtool.getWorkspaceFor(invitation)
        SubElement(invitation_tag, 'workspace',
                   title=workspace.Title(), href=workspace.absolute_url())
        inviter = invtool.getInviterFor(invitation)
        if inviter is not None:
            inviter_tag = SubElement(invitation_tag, 'inviter')
            inviter_tag.text = inviter.getProperty('fullname')
        return view_tag

class InvitationAddRegistrationFormFragment(AddRegistrationFormFragmentBase):

    def createAddAndReturnURL(self, data):
        context = aq_inner(self.context)
        self.addProfileAndLogin(data)
        # we should be now authenticated
        member = getToolByName(context,
                               'portal_membership').getAuthenticatedMember()
        invId = getInvitationIdFromRequest(self.request)
        invtool = getToolByName(context, 'workspace_invitations')
        invtool.acceptInvitation(invId, member)
        # redirect to the just created user profile
        url = self.destinationURLForMember(member)
        return url

    @form.action("Register", name="register")
    def handle_register(self, action, data): #@UnusedVariable
        url = self.createAddAndReturnURL(data)
        raise SafeRedirect(url)

    @form.action("Reject", name="reject", validator=NO_VALIDATION)
    def handle_reject(self, action, data): #@UnusedVariable
        context = aq_inner(self.context)
        invId = getInvitationIdFromRequest(self.request)
        invtool = getToolByName(context, 'workspace_invitations')
        invtool.rejectInvitation(invId)
        raise SafeRedirect(self.cancelURL())

    @form.action("Cancel", name="cancel", validator=NO_VALIDATION)
    def handle_cancel(self, action, data):
        raise SafeRedirect(self.cancelURL())

class InvitationAddRegistrationPage(Page):
    views = (InvitationAddRegistrationViewFragment,
             InvitationAddRegistrationFormFragment,
             ) + COMMON_VIEWS

###############################################
###   classes for User Subscription Start   ###
###############################################

class UserSubscriptionViewFragment(Fragment):

    def asElement(self):
        return Element('view',
                       name='subscription.html',
                       type='site',
                       title='Subscribe To ConserveOnline',
                       section='subscribe')

class UserSubscriptionAddForm(AddFormFragment):
    """ Fragment the defines the form structure and contains the methods to act
        upon submitted form data
    """
    form_fields = form.FormFields(ISubscriptionSchema)

    def provideInitialDefaults(self):
        """ provide intial data if they've already got a subscription object """
        defaults = {}
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getAuthenticatedMember()
        portal_obj = aq_parent(aq_inner(context))
        subscription_folder = portal_obj['subscriptions']
        try:
            subscription = subscription_folder['subscription_'+member.id]
            subscription_schema = subscription.Schema()
            for field in self.form_fields:
                name = field.__name__
                value = None
                accessor = subscription_schema[name].getAccessor(subscription)
                value = accessor()
                if value:
                    defaults[name] = value
        except KeyError: #this means the subscription object doesn't exist
            pass
        delivery_method_field =  [r for r in self.form_fields if r.__name__=='delivery_method']
        if delivery_method_field:
            delivery_method_field = delivery_method_field[0]
            desc = delivery_method_field.field.description
            desc = desc[:desc.index('(')+1]+'%s'+desc[desc.index(')'):]
            delivery_method_field.field.description = desc % member.getProperty('email')
        return defaults

    def createAddAndReturnURL(self, data):
        """ method that takes the from data and creates the subscription object """
        context = self.context
        subscription_obj = None
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getAuthenticatedMember()
        portal_obj = aq_parent(aq_inner(context))
        subscription_folder = portal_obj['subscriptions']
        first = False
        try:
            subscription_obj = subscription_folder['subscription_'+member.id]
        except KeyError:
            first = True
            subid = subscription_folder.invokeFactory('COLSubscription', 'subscription_'+member.id)
            subscription_obj = subscription_folder[subid]
        subscription_obj.update(**data)
        if first:
            process_subscription(portal_obj, subscription_obj, 10)
        return portal_obj.absolute_url()+'/subscriptions/success.html'

    @action("Subscribe", name="add")
    def handle_add(self, action, data): #@UnusedVariable
        url = self.createAddAndReturnURL(data)
        raise SafeRedirect(url)

class UserSubscriptionPage(Page):
    views = (UserSubscriptionViewFragment,
             UserSubscriptionAddForm,) + COMMON_VIEWS


class UserUnsubscriptionViewFragment(Fragment):
    """ View fragment for view that user unsubscribes """
    def asElement(self):
        return Element('view',
                       name='unsubscription.html',
                       type='site',
                       title='Unsubscribe From ConserveOnline',
                       section='subscribe')


class UserUnsubscriptionAddForm(AddFormFragment):
    """ Fragment to defines the form structure and contains the methods to act
        upon submitted form data
    """
    form_fields = ()

    def createAddAndReturnURL(self, data):
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        member = pmem.getAuthenticatedMember()
        portal_obj = aq_parent(aq_inner(context))
        subscription_folder = portal_obj['subscriptions']
        subid = 'subscription_' + member.id
        if subscription_folder.has_key(subid):
            subscription_folder.manage_delObjects([subid])
        return portal_obj.absolute_url() + '/subscriptions/success.html'

    def cancelURL(self):
        return self.context.absolute_url().replace('https://', 'http://')


class UserUnsubscriptionPage(Page):
    """The view for proceeding with an unsubscription"""
    views = (UserUnsubscriptionViewFragment,
             UserUnsubscriptionAddForm,) + COMMON_VIEWS


###############################################
###   classes for User Subscription End     ###
###############################################

###############################################
### classes for Subscription Success Start  ###
###############################################

class SubscriptionSuccessViewFragment(Fragment):
    """ View fragment for view that user unsubscribes """
    def asElement(self):
        return Element('view',
                       name='success.html',
                       type='site',
                       title='Thank You For Subscribing',
                       section='subscriptions')

class SubscriptionSuccessFragment(Fragment):
    """ contains the delivery method and the rss url"""
    def asElement(self):
        context = self.context
        pmem = getToolByName(context, 'portal_membership')
        portal_obj = aq_parent(aq_inner(context))
        member = pmem.getAuthenticatedMember()
        subid = 'subscription_' + member.id
        subscr_obj = context[subid]
        delivery_method = subscr_obj.getDelivery_method()
        root = Element('subscribe')
        SubElement(root, 'email').text = (delivery_method == 'email') and 'true' or 'false'
        SubElement(root, 'rss').text = portal_obj.absolute_url() + '/subscriptions/feed.xml'
        return root

class SubscriptionPage(Page):
    views = (SubscriptionSuccessViewFragment,
             SubscriptionSuccessFragment) + COMMON_VIEWS

###############################################
### classes for Subscription Success End    ###
###############################################

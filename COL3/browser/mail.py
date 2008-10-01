from Products.CMFCore.utils import getToolByName

from Products.COL3 import config

class simple_mail_tool:

    resend_invite_template = config.INVITATION_EMAIL_BODY

    def sendJoinRequestNotification(self, workspace, to_email):
        mailhost = getToolByName(workspace, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.WORKSPACE_JOINREQUEST_TEMPLATE % (workspace.Title(),
                                                            workspace.absolute_url())
        subject = config.WORKSPACE_JOINREQUEST_SUBJECT % workspace.Title()
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendEmailAcceptance(self, workspace, to_email):
        mailhost = getToolByName(workspace, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.WORKSPACE_ACCEPT_TEMPLATE % (workspace.Title(),)
        subject = config.WORKSPACE_ACCEPT_SUBJECT % workspace.Title()
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendEmailRejection(self, workspace, to_email):
        mailhost = getToolByName(workspace, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.WORKSPACE_REJECT_TEMPLATE % (workspace.Title())
        subject = config.WORKSPACE_REJECT_SUBJECT % workspace.Title()
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendEmailRemoved(self, workspace, to_email):
        mailhost = getToolByName(workspace, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.WORKSPACE_REMOVED_TEMPLATE % (workspace.Title())
        subject = config.WORKSPACE_REMOVED_SUBJECT % workspace.Title()
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendInvitationRejection(self, workspace, to_email, userid):
        mailhost = getToolByName(workspace, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.WORKSPACE_INVITEREJECTED_TEMPLATE
        subject = config.WORKSPACE_INVITEREJECTED_SUBJECT % (userid, workspace.Title())
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendEmailToCrossRefAdmin(self, context, msg, to_email, submit_id, batch_id, doi):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.CROSSREF_EMAIL_BODY % (submit_id, batch_id, doi, msg)
        subject = config.CROSSREF_EMAIL_SUBJECT % submit_id
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendCrossrefEmailToTNC(self, context, msg, submit_id, batch_id, doi, to_email=config.TNC_ADMIN):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.CROSSREF_EMAIL_BODY % (submit_id, batch_id, doi, msg)
        subject = config.CROSSREF_EMAIL_SUBJECT % submit_id
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendSubscriptionEmail(self, context, links, unsubscribe, to_email):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.SUBSCRIPTION_EMAIL_BODY % (links, unsubscribe)
        subject = config.SUBSCRIPTION_EMAIL_SUBJECT
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendSubscriptionDigestEmail(self, context, links, unsubscribe, to_email):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.SUBSCRIPTION_DIGEST_EMAIL_BODY % (links, unsubscribe)
        subject = config.SUBSCRIPTION_DIGEST_EMAIL_SUBJECT
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendRecommendationReportEmail(self, context, mfrom, info, to_email=config.TNC_ADMIN):
        mailhost = getToolByName(context, 'MailHost')
        template = config.RECOMMENDATION_REPORT_BODY % info
        subject = config.RECOMMENDATION_REPORT_SUBJECT
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendRecommendationBadContentEmail(self, context, info, to_email=config.TNC_ADMIN):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.RECOMMENDATION_BAD_CONTENT_BODY % info
        subject = config.RECOMMENDATION_BAD_CONTENT_SUBJECT
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendPasswordResetEmail(self, context, reset_url, to_email):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.RESET_PASSWORD_EMAIL_BODY % reset_url
        subject = config.RESET_PASSWORD_SUBJECT
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

    def sendAdminErrorEmail(self, context, to_email=config.mail):
        mailhost = getToolByName(context, 'MailHost')
        mfrom = config.NOREPLY_SENDER_ADDRESS
        template = config.ERROR_EMAIL_BODY % context.__str__()
        subject = config.ERROR_EMAIL_SUBJECT
        mailhost.secureSend(template, mto=to_email, mfrom=mfrom, subject=subject)

##parameters=member=None, password='secret'
##
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.utils import decode
from Products.CMFDefault.utils import makeEmail
from Products.CMFDefault.utils import Message as _

atool = getToolByName(context, 'portal_actions')
ptool = getToolByName(context, 'portal_properties')
utool = getToolByName(context, 'portal_url')
portal = utool.getPortalObject()
portal_url = utool()


options = {}
options['password'] = password

to_name = member and member.getProperty('fullname') or ''
to_email = member and member.getProperty('email') or 'foo@example.org'

headers = {}
headers['Subject'] = _(u'${portal_title}: Membership reminder',
                      mapping={'portal_title': decode(ptool.title(), script)})
headers['From'] = '%s <%s>' % (portal.getProperty('email_from_name'),
                               portal.getProperty('email_from_address'))
headers['To'] = '%s <%s>' % (to_name, to_email)

mtext = context.password_email_template(**decode(options, script))
return makeEmail(mtext, script, headers)

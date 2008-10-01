from Products.CMFCore import utils as cmfutils

from Products.COL3.browser.base import XSLTView
from Products.COL3 import config

WSCDN = config.WORKSPACE_SESSION_CREATION_DATA_NAME

class NewsItemView(XSLTView):
    """ View class for newsitem views """

    def update(self):
        """ """
        super(NewsItemView, self).update()
        context = self.context
        trans = cmfutils.getToolByName(context, 'translation_service')
        mship = cmfutils.getToolByName(context, 'portal_membership')
        mdata = cmfutils.getToolByName(context, 'portal_memberdata')

        modification_date = context.ModificationDate()
        self.modification_date =  trans.ulocalized_time(modification_date,
                                                        True, context, domain='plone')
        author_id = context.Creator()
        author = mship.getMemberInfo(author_id)
        name=author and author['fullname'] or author_id
        # assume no name means no membership and
        author_url = name and (mdata.absolute_url() + "/" + author_id +
                               "/display.html" or None)
        self.author = dict(name=author and author['fullname'] or author_id,
                           url=author_url)
        self.body = context.CookedBody(stx_level=2)

from Products.CMFCore.utils import getToolByName

def processCrossRefEmails(self):
    """ Simple method that will call the appropriate method on the
        CrossRef tool to access the email account set up for responses
        to CrossRef submissions and process...
    """
    crossref_tool = getToolByName(self, 'crossreference_tool')
    crossref_tool.processEmailReports()
    return 'CrossRef email processing method executed successfully...'
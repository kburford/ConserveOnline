from Products.CMFCore.utils import getToolByName

def listQueuedCrossrefFiles(self, area='test'):
    """ Simple method that will call the appropriate method on the
        CrossRef tool to update the CrossRef site with library dois
    """
    crossref_tool = getToolByName(self, 'crossreference_tool')
    return crossref_tool.listQueuedFiles()
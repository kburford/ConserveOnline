from zExceptions import Redirect
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.app.publisher.browser import BrowserView

class LibraryRedirect(BrowserView):
    implements(IPublishTraverse)
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    def __call__(self):
        """ Grab the filename off the end of the traversal path and redirect to the proper library folder """
        librarypath = self.context.absolute_url()
        tpath = self.traverse_subpath[:]
        tpath.reverse()
        if len(tpath) >= 1:
            librarypath = librarypath + '/library/' + tpath[0]
        raise Redirect(librarypath)
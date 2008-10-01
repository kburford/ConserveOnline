from Products.COL3.etree import Element, SubElement

from Products.COL3.browser.base import Page, Fragment
from Products.COL3.browser.portal import NewWorkgroupPortletFragment
from Products.COL3.browser.portal import NewDocInLibraryPortletFragment

class ViewFragment(Fragment):
    def asElement(self):
        ctx = self.context
        req = self.request
        workgroupfragment = NewWorkgroupPortletFragment(ctx, req)
        librarydocfragment = NewDocInLibraryPortletFragment(ctx, req)
        contextfragment = ContextFragment(ctx, req)
        elem = Element('view')
        elem.append(workgroupfragment.asElement())
        elem.append(librarydocfragment.asElement())
        return elem

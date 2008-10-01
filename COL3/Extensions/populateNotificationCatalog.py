import sys, string, transaction
from zope.app.component.hooks import setSite

def populateNoficationCatalog(self):
    """Script to add existing content to the notification catalog."""
    write = self.REQUEST.RESPONSE.write
    write('Cleaning up the notification catalog...\n')
    self.notification_catalog.manage_catalogClear()
    results = self.portal_catalog(portal_type=['LibraryFile', 'COLFile', 'COLPage'])
    total = len(results)
    write('Indexing %s items:\n\n' % total)
    catalog_object = self.notification_catalog.catalog_object
    for n, item in enumerate(results):
        catalog_object(item.getObject(), None)
        write('%s/%s %s\n' % (n, total, item.getURL()))
    write('\nDone.')

if __name__=='__main__':
    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest
    app=makerequest(app)
    plonesite=sys.argv[1]
    portal = app.unrestrictedTraverse(plonesite)
    setSite(portal)
    newSecurityManager(None, portal.getWrappedOwner())

    populateNoficationCatalog(portal)

    txn = transaction.get()
    txn.note("Completed populating notification catalog")
    txn.commit()


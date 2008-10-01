from zope.interface import implements

from Products.Archetypes.public import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.Archetypes.Field import ReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.COL3.interfaces.workspace import IPortalHomeConfig


class PortalHomeConfig(ATCTContent):
    implements(IPortalHomeConfig)
    featured_ws_schema = Schema((ReferenceField('sideimageone',
                                                widget=ReferenceBrowserWidget(label='Side Image One',
                                                                              startup_directory='about'),
                                                relationship='ReferenceToImageOne',),
                                 StringField('sideimageoneurl',
                                             widget=StringWidget(label='Image One Url')),
                                 ReferenceField('sideimagetwo',
                                                widget=ReferenceBrowserWidget(label='Side Image Two',
                                                                              startup_directory='about'),
                                                relationship='ReferenceToImageTwo',),
                                 StringField('sideimagetwourl',
                                             widget=StringWidget(label='Image Two Url')),
                                 ReferenceField('sideimagethree',
                                                widget=ReferenceBrowserWidget(label='Side Image Three',
                                                                              startup_directory='about'),
                                                relationship='ReferenceToImageThree',),
                                 StringField('sideimagethreeurl',
                                             widget=StringWidget(label='Image Three Url')),
                                 TextField('featurecontent',
                                           default_content_type = 'text/html',
                                           default_output_type = 'text/html',
                                           allowable_content_types=('text/html',),
                                           widget=RichWidget(label='Feature Content')),
                                 ReferenceField('featuredimage',
                                                widget=ReferenceBrowserWidget(label='Feature Image',
                                                                              startup_directory='about'),
                                                relationship='RefersToTheFeaturedImage'),
                                 ReferenceField('featuredworkspace',
                                                widget=ReferenceBrowserWidget(label='Featured Workspace',
                                                                              startup_directory='workspaces'),
                                                relationship='RefersToTheFeaturedWorkspace',),
                               ))
    schema = BaseSchema + featured_ws_schema
    _at_rename_after_creation = True
    
registerType(PortalHomeConfig)

def addPortalHomeConfig(self, id, **kw):
    """ Create a new document
    """
    fws = PortalHomeConfig(id)
    self._setObject(id, fws)

""" Schema extender/modifier for gallery aware items. """

# Zope
from zope.component import adapts
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

# ext
from archetypes.markerfield import InterfaceMarkerField
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

# local
from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content.interfaces import IHomePage
from younglives.content.interfaces import IGalleryReferenceAware, \
    IGalleryContainerAware, IGalleryContainerMarker
from younglives.policy import _

class ExtReferenceField(ExtensionField, atapi.ReferenceField):
    """ A reference field  """


class GalleryReferenceExtender(object):
    """ New fields:
    
    gallery -- reference to gallery folder (any folder with images)
    """
        
    adapts(IGalleryReferenceAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [ 

        ExtReferenceField('gallery',
            required = 0,
            multiValued = 0,
            relationship = 'relatedGallery',
            allowed_types = ('Folder'),
            widget = ReferenceBrowserWidget(
                label = _(u"gallery-ext_gallery_label", 
                          default = u"Gallery"),
                description = _(u"gallery-ext_gallery_desc", 
                                default = u"Select folder with images."),)), 

    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        if IHomePage.providedBy(self.context):
            return []
        return self.fields
    
    
class GalleryContainerExtender(object):
    """ New fields:
    
    isGallery -- marks gallery folder
    """
        
    adapts(IGalleryContainerAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [ 

        InterfaceMarkerField('isGallery',
            required = 0,
            interfaces = (IGalleryContainerMarker,),
            widget = atapi.BooleanWidget(
                label = _(u"gallery-ext_is-gallery_label", 
                    default = u"Gallery"),
                description = _(u"gallery-ext_is-gallery_desc",
                    default = u"Mark this folder as images gallery"),)), 

    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields
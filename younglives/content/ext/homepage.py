""" Schema extender/modifier for Topic content type. """

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
from archetypes.markerfield.utils import addMarkerInterface, removeMarkerInterface

# local
from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content.interfaces import IHomePage
from younglives.content.interfaces import IHomepageHeroAware, \
    IHomepageHeroMarker, IHomepageBoxAware, IHomepageBoxMarker
from younglives.policy import _
    
class ExtHeroImageField(ExtensionField, atapi.ImageField):
    """A image field  """
    
    def set(self, instance, value, **kwargs):
        if value and value!="DELETE_IMAGE":
            addMarkerInterface(instance, IHomepageHeroMarker)
        else:
            removeMarkerInterface(instance, IHomepageHeroMarker)
        super(ExtHeroImageField, self).set(instance, value, **kwargs)
    

class HomepageHeroExtender(object):
    """ New fields:
    
    showHeroOnHomepage -- mark this item to show on homepage photo rotator 
    homepageHeroImage -- image for homepage photo rotator
    """
        
    adapts(IHomepageHeroAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [
              
        ExtHeroImageField("homepageHeroImage",
            required = 0,
            schemata = 'homepage',
            languageIndependent = 1,
            pil_quality = 100,
            original_size = (468, 239),
            sizes = {'thumb':(117,60)},
            validsizes = (468, 239),
            validators = ("checkImageSize",),
            storage = atapi.AnnotationStorage(),
            widget = atapi.ImageWidget(
                label = _(u"homepage-ext_hero-image_label",
                          default = u"Hero image"),
                description = _(u"homepage-ext_hero-image_desc",
                                default = u"Upload image for homepage photo \
rotator. Required size is 468x239px."),)),


    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        if IHomePage.providedBy(self.context):
            return []
        return self.fields


class ExtBoxImageField(ExtensionField, atapi.ImageField):
    """A image field  """
    
    def set(self, instance, value, **kwargs):
        if value and value!="DELETE_IMAGE":
            addMarkerInterface(instance, IHomepageBoxMarker)
        else:
            removeMarkerInterface(instance, IHomepageBoxMarker)
        super(ExtBoxImageField, self).set(instance, value, **kwargs)
    
    
class HomepageBoxExtender(object):
    """ New fields:
    
    homepageBoxImage -- image for homepage middle section box
    """
        
    adapts(IHomepageBoxAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [
              
        ExtBoxImageField("homepageBoxImage",
            required = 0,
            schemata = 'homepage',
            languageIndependent = 1,
            pil_quality = 100,
            original_size = (222, 87),
            sizes = {'thumb':(111,44)},
            validsizes = (222, 87),
            validators = ("checkImageSize",),
            storage = atapi.AnnotationStorage(),
            widget = atapi.ImageWidget(
                label = _(u"homepage-ext_homepage-image_label",
                          default = u"Box image"),
                description = _(u"homepage-ext_homepage-image_desc",
                                default = u"Upload image for homepage middle \
section box. Required size is 222x87px."),)),

    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields

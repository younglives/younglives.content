""" Schema extender/modifier for items with banner image. """

# Zope
from zope.component import adapts
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

# local
from younglives.content.interfaces.content import IBannerAware
from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content import _


class ExtImageField(ExtensionField, atapi.ImageField):
    """ An Image field.  """


class BannerExtender(object):
    """ Adding new fields:

    banner -- banner image for folders
    """

    adapts(IBannerAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [

        ExtImageField(
            "bannerImage",
            required=0,
            languageIndependent=1,
            pil_quality=100,
            original_size=(492, 123),
            sizes={'preview': (246, 62)},
            validsizes=(492, 123),
            validators=("checkImageSize",),
            storage=atapi.AnnotationStorage(),
            widget=atapi.ImageWidget(
                label=_(
                    u"banner-ext_banner-image_label",
                    default=u"Banner image"),
                description=_(
                    u"banner-ext_banner-image_desc",
                    default=u"Upload banner image. \
                        Required size is 492x123px."),)),

        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

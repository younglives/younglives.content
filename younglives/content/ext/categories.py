""" Schema extender/modifier for Document content type. """

# Zope
from zope.component import adapts
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IBaseContent
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

# local
from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content import _

class ExtLinesField(ExtensionField, atapi.LinesField):
    """A lines field  """
    

class CategoriesExtender(object):
    """ New fields:
    
    theme -- theme tags
    topic -- topic tags
    """

    adapts(IBaseContent)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [
              
        ExtLinesField('theme',
            required = 0,
            multiValued = 1,
            accessor = 'theme',
            schemata = 'categorization',
            languageIndependent = 0,
            widget = atapi.KeywordWidget(
                label = _(u"category_theme_label", 
                    default = u"Theme"),
                description = _(u"category_theme_desc",
                    default = u"Select or create new theme to tag this item."),
            ),
        ),
                    
        ExtLinesField('categoryCountry',
            required = 0,
            multiValued = 1,
            #accessor = 'categoryCountry',
            schemata = 'categorization',
            languageIndependent = 0,
            widget = atapi.KeywordWidget(
                label = _(u"categoryCountry_label",
                    default = u"Country"),
                description = _(u"categoryCountry_desc",),
            ),
        ),
    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields
    
    def getOrder(self, original):
        categorization = original['categorization']
        subject = categorization.index('subject')
        categorization.remove('theme')
        categorization.insert(subject, 'theme')
        categorization.remove('categoryCountry')
        categorization.insert(subject, 'categoryCountry')
        return original

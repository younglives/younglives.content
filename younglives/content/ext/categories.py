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

from younglives.international.browser.interfaces import IYounglivesInternational

# local
from younglives.content import _

class ExtLinesField(ExtensionField, atapi.LinesField):
    """A lines field  """
    

class CategoriesExtender(object):
    """ New fields:
    
    categoryCountry -- theme tags
    """

    adapts(IBaseContent)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesInternational

    fields = [
                    
        ExtLinesField('categoryCountry',
            required = 0,
            multiValued = 1,
            #accessor = 'categoryCountry',
            schemata = 'categorization',
            languageIndependent = 0,
            widget = atapi.KeywordWidget(
                label = _(u"categoryCountry_label",
                    default = u"Country"),
                description = _(u"categoryCountry_desc",
                    default = u""),
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
        categorization.remove('categoryCountry')
        categorization.insert(subject, 'categoryCountry')
        return original

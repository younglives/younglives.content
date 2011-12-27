""" Schema extender/modifier for Document content type. """

# Zope
from zope.component import adapts
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

# local
from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content.interfaces import IQuoteAware
from younglives.content import _

class ExtStringField(ExtensionField, atapi.StringField):
    """A string field  """

class QuoteExtender(object):
    """ New fields:
    
    quote -- the quote to display
    """
        
    adapts(IQuoteAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [
              
        ExtStringField('quote',
            required = 0,
            schemata = 'default',
            languageIndependent = 0,
            widget = atapi.StringWidget(
                label = _(u"quote_label", 
                    default = u"Quote"),
                description = _(u"quote_desc",
                    default = u"Enter quote text that appears at the bottom"),)),

    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields


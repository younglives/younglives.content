""" Schema extender/modifier for Document content type. """

# Zope
from zope.component import adapts
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

# local
from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content.interfaces import IQuoteAware
from younglives.content import _

class ExtLinesField(ExtensionField, atapi.LinesField):
    """A lines field  """
    

class CategoriesExtender(object):
    """ New fields:
    
    theme -- theme tags
    topic -- topic tags
    """
        
    adapts(IQuoteAware)
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
                    default = u"Select or create new theme to tag this item."),)),
                    
        ExtLinesField('topic',
            required = 0,
            multiValued = 1,
            accessor = 'topic',
            schemata = 'categorization',
            languageIndependent = 0,
            widget = atapi.KeywordWidget(
                label = _(u"category_topic_label", 
                    default = u"Topic"),
                description = _(u"category_topic_desc",
                    default = u"Select or create new topic to tag this item."),)),

    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields
    
    def getOrder(self, original):
        categorization = original['categorization']
        subject = categorization.index('subject')
        categorization.remove('topic')
        categorization.insert(subject, 'topic')
        categorization.remove('theme')
        categorization.insert(subject, 'theme')
        return original

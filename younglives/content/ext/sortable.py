""" Schema extender for items with sortable content. """

# Zope
from zope.component import adapts
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

# local
from younglives.content.interfaces import IYoungLivesContentLayer
from younglives.content.interfaces import ISortableAware
from younglives.policy import _

LISTING_INDEXES_TO_SORT_ON = atapi.DisplayList((
    ('Date', 'Date'),
    ('start', 'Event start date'),
    ('getObjPositionInParent', 'Position in folder'),
    ('getId', 'Title'),))

class ExtStringField(ExtensionField, atapi.LinesField):
    """ A String field.  """
       

class SortableExtender(object):
    """ Adding new fields:
    
    sortOn -- catalog index
    sortOrder -- sorting order
    """
        
    adapts(ISortableAware)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYoungLivesContentLayer

    fields = [

        ExtStringField('sortOn',
            required = 0,
            schemata = 'settings',
            languageIndependent = 1,
            vocabulary = LISTING_INDEXES_TO_SORT_ON,
            widget = atapi.SelectionWidget(
                label = _(u"folder_sort-on_label", 
                    default = u"Sort by"),
                description = _(u"folder_sort-on_desc",
                    default = u"Select index to sort items on."),)),
                    
        ExtStringField('sortOrder',
            required = 0,
            schemata = 'settings',
            languageIndependent = 1,
            vocabulary = ('ascending','descending'),
            widget = atapi.SelectionWidget(
                label = _(u"folder_sort-order_label", 
                    default = u"Sort order"),
                description = _(u"folder_sort-order_desc",
                    default = u"Select sort order."),)),

    ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self.fields


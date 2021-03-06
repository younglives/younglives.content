from zope.component import adapts
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces.file import IATFile
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

from younglives.content.browser.interfaces import IYounglivesContent
from younglives.content import _

DOCUMENT_TYPES = atapi.DisplayList((
    ('full text', 'Full text'),
    ('summary', 'Summary'),
    ('translation', 'Translation'),))


class ExtLinesField(ExtensionField, atapi.LinesField):
    """ A Lines field.  """


class FileExtender(object):
    """ Adding new fields to File type:

    documentType -- document type
    """

    adapts(IATFile)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IYounglivesContent

    fields = [

        ExtLinesField(
            'documentType',
            schemata='categorization',
            required=0,
            languageIndependent=1,
            vocabulary=DOCUMENT_TYPES,
            storage=atapi.AnnotationStorage(),
            widget=atapi.SelectionWidget(
                label=_(u"file-ext_document-type_label",
                        default=u"Document type"),
                description=_(
                    u"file-ext_document-type_desc",
                    default=u"Select document type, if applicable."),)),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

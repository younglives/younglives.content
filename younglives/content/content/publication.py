""" Definition of the Publication content type. """


# Zope
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

# ext
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

# local
from younglives.policy import _
from younglives.content.interfaces import IPublication
from younglives.content.config import *

PublicationSchema = ATDocument.schema.copy() + atapi.Schema((

    atapi.StringField('subtitle',
        required = 0,
        searchable = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.StringWidget(
            label = _(u"publication_subtitle_label", 
                      default = u"Subtitle"),
            description = _(u"publication_subtitle_desc", 
                            default = u"Enter publication subtitle."),)),                                  

    atapi.StringField('author',
        required = 1,
        searchable = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.StringWidget(
            label = _(u"publication_author_label", 
                      default = u"Author"),
            description = _(u"publication_author_desc", 
                            default = u"Enter publication's author."),)),

    atapi.StringField('series',
        required = 0,
        searchable = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.StringWidget(
            label = _(u"publication_series_label", 
                      default = u"Series"),
            description = _(u"publication_series_desc", 
                            default = u"Enter publication's series."),)),
         
    atapi.DateTimeField('publication_date',
        required = 1,
        searchable = 0,
        languageIndependent = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.CalendarWidget(
            label = _(u"publication_publication-date_label", 
                      default = u"Date"),
            description = _(u"publication_publication-date_desc", 
                            default = u"Publication date"),)),

    atapi.ReferenceField('files',
        required = 1,
        multiValued = 1,
        relationship = 'relatedPublicationFiles',
        allowed_types = ("File",),
        widget = ReferenceBrowserWidget(
            hide_inaccessible = 1,
            force_close_on_insert = 0,
            image_portal_types = ('File',),
            startup_directory_method = 'refBrowserFolder',
            label = _(u"publication_files_label",
                      default = u"Files"),
            description = _(u"publication_files_desc", 
                            default = u"Select publication files."),)),

    ))

PublicationSchema.moveField('subtitle', after='title')
PublicationSchema["title"].storage = atapi.AnnotationStorage()
PublicationSchema["description"].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PublicationSchema, moveDiscussion=False)


class Publication(ATDocument):
    """ YoungLives publication archetype. """
    implements(IPublication)
    
    publication_date = atapi.ATFieldProperty("publication_date")

    meta_type = "Publication"
    schema = PublicationSchema

    def refBrowserFolder(self):
        """Start up directory for the reference browser widget"""
        return '/files'

atapi.registerType(Publication, PROJECTNAME)

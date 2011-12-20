""" Definition of the Audio content type. """


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
from younglives.content.interfaces import IAudio
from younglives.content.config import *

# TODO: add file format validator
AudioSchema = ATDocument.schema.copy() + atapi.Schema((

    atapi.FileField("file",
        required = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.FileWidget(
            label = _(u"audio_file_label",
                      default = u"Audio file"),
            description = _(u"audio_file_desc",
                            default = u"Upload audio file. \
Required format is '.mp3'."),))
            
))

AudioSchema["title"].storage = atapi.AnnotationStorage()
AudioSchema["description"].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(AudioSchema, moveDiscussion=False)


class Audio(ATDocument):
    """ YoungLives audio archetype. """
    implements(IAudio)

    meta_type = "Audio"
    schema = AudioSchema

atapi.registerType(Audio, PROJECTNAME)
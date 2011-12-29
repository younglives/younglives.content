from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore.utils import ContentInit
from Products.validation.config import validation

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('younglives.content')

from content.publication import Publication
from config import PROJECTNAME

from validators import ImageSizeValidator
validation.register(ImageSizeValidator('checkImageSize'))

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        ContentInit('%s: %s' % (PROJECTNAME, atype.portal_type),
            content_types      = (atype,),
            permission         = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)

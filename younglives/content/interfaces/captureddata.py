""" Captured data interfaces. """


# Zope
from zope import schema
from zope.interface import Interface

# local
from younglives.policy.i18n import younglivesMessageFactory as _


class ICapturedData(Interface):
    """ A helper interface used to build form fields """
    
    country = schema.TextLine(title=_(u"Country"), required=1, default=u"UK")
    jobtitle = schema.TextLine(title=_(u"Job Title"), required=1)
    organization = schema.TextLine(title=_(u"Organization"), required=0)

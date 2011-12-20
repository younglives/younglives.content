""" User profiles interfaces. """


# Zope
from zope import schema
from zope.interface import Interface
from zope.schema import ValidationError

# Plone
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

# local
from younglives.policy import _

# email validation
class InvalidEmailAddress(ValidationError):
    "Invalid email address"

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

#===============================================================================
# General user properties
#===============================================================================

class IUserProfile(Interface):
    """ A helper interface used to build form fields """
    
    fullname = schema.TextLine(title=_(u"Full Name"), required=1)
    location = schema.TextLine(title=_(u"Location"), required=0)
    jobtitle = schema.TextLine(title=_(u"Job Title"), required=0)
    
class IUserAddProfile(Interface):
    """ A helper interface used to build form fields """
    
    fullname = schema.TextLine(title=_(u"Full Name"), required=1)
    email = schema.TextLine(title=_(u"Email"),
                            constraint=validateaddress, 
                            required=1,)
    location = schema.TextLine(title=_(u"Location"), required=0)
    jobtitle = schema.TextLine(title=_(u"Job Title"), required=0)
    
class IUserMultiAddProfile(Interface):
    """ A helper interface used to build form fields """
    
    csv = schema.Text(title=_(u"Members list"),
                      required=1,
                      description=_(u"List of members. Required columns are: \
full name, email, location and job title. Use ',' to separate values."))
    
class IUserPassword(Interface):
    """ A helper interface used to build form fields """

    password1 = schema.Password(title=_(u"Password"), required=1)
    password2 = schema.Password(title=_(u"Retype password"), required=1)
    
class IUserNotifications(Interface):
    """ A helper interface used to build form fields """

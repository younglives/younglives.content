""" Configlets (sites settings) interfaces """


# Python
import re

# Zope
from zope import schema
from zope.interface import Interface

# Plone
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

# local
from younglives.policy.i18n import younglivesMessageFactory as _


# email validation
class InvalidEmailAddress(schema.ValidationError):
    "Invalid email address"

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True


# email validation
class InvalidRegularExpression(schema.ValidationError):
    "Invalid regular expression"

def validatepattern(value):
    try:
        for line in value:
            re.compile(line)
    except:
        raise InvalidRegularExpression(value)
    return True


class IYoungLivesSettings(Interface):
    """ General settings """
    
    from_name = schema.TextLine(
        title = _(u" Site 'From' name"),
        description = _(u"Site generates e-mail using this name as the e-mail \
sender."),
        required = 1,
        default = u"Young Lives administrator")
    
    from_email = schema.TextLine(
        title = _(u"Site 'From' email"),
        description = _(u"Plone generates e-mail using this address as the \
e-mail return address."),
        required = 1,
        default = u"chris@fry-it.com",
        constraint = validateaddress)
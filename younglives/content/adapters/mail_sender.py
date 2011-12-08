""" Mail sender adapter.  """

# Python
import logging

# Zope
from zope.interface import implements
from zope.component import ComponentLookupError

# Plone
from Products.CMFCore.utils import getToolByName

# local
from younglives.content.interfaces import IMailSender


logger = logging.getLogger('younglives.mailsender')

class MailSender(object):    
    implements(IMailSender)
    
    def __init__(self, context):
        self.context = context
    
    def sendMail(self, subject, message, email_recipient=None):
        # Sometime cannot use acquisition
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        mailhost = portal.MailHost
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to \
execute this action.'
    
        email_charset = portal.getProperty('email_charset')
    
        from_email = portal.getProperty('email_from_address')
        if not from_email:
            raise ValueError, 'You must provide a source address for this \
action or enter an email in the portal properties.'
            
        email_recipient = email_recipient or from_email
        
        from_name = portal.getProperty('email_from_name')
        source = "%s <%s>" % (from_name, from_email)
        
        # don't send if it is local instance, just print
        if portal.absolute_url().find('.local')>=0:
            logger.info(source)
            logger.info(subject)
            logger.info(message)
            return
    
        mailhost.secureSend(message, email_recipient, source,
                            subject=subject, subtype='plain',
                            charset=email_charset, debug=True)
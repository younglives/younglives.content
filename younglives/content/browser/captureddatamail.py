""" Sends captured data notification. """


# Zope
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Plone
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

# local
from younglives.content.interfaces import IMailSender


class CapturedDataMailView(BrowserView):
    
    admin_notify_template = ViewPageTemplateFile('captureddata_mail_template.pt')
    
    def __call__(self):
        """ Sends captured data notification to site admin. """
        
        try:
            mail_sender = IMailSender(self.context)
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            portal_title = portal.pretty_title_or_id()
            data = {}
            data['admin_fullname'] = portal.getProperty('email_from_name')
            data['captureddata_settings_url'] = '%s/captured-data-settings' % \
                portal.absolute_url()
            subject = "Captured data notification for %s" % portal_title
            message = self.admin_notify_template(self.context, **data)
            mail_sender.sendMail(subject, message)
        except:
            return 0

        return 1
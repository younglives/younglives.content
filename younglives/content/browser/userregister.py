""" Self registering new users 

User can register directly:
  1. User registers himself through this form and after that he is 
    added to pending users. Notification is sent to site admin.
  2. Site managers can approve or reject new users through Intranet Users 
    management console ('Users' tab).
  3. After approval user becomes intranet folder viewer and password resetting 
    email is sent to him.
     
""" 

# Zope
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Plone
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

# local
from younglives.policy import _
from younglives.content.interfaces import IGroupManager
from younglives.content.interfaces import IUserAddProfile, IUserStorage, \
    IMailSender

class UserRegisterForm(form.AddForm):
    template = ViewPageTemplateFile('userregister_form.pt')
    admin_notify_template = ViewPageTemplateFile('userregister_mail_template.pt')
    prefix = "register."
    label = _(u'Registration')
    formErrorsMessage = _('There were some errors.')
    fields = field.Fields(IUserAddProfile)
    errors = {}
    next_url = None     
 
            
    @button.buttonAndHandler(_('Register'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
           self.status = self.formErrorsMessage
           return
        obj = self.create(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True


    def create(self, data):
        email = data['email'].encode("utf-8")
        
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        plone_utils = getToolByName(self.context, 'plone_utils')
        portal_registration = getToolByName(self.context, 'portal_registration')
        acl_users = getToolByName(self.context, 'acl_users')
        group_manager = IGroupManager(portal)
        user_storage = IUserStorage(portal)
        
        try: 
            viewers = group_manager.viewers()
        except:
            msg = u'Could not find intranet viewers group.'
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None
        
        try:
            editors = group_manager.editors()
        except:
            msg = u'Could not find intranet editors group.'
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None

        if not user_storage.add(data):
            msg = u'This user is already waiting for approval.'
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None
        elif [u for u in viewers if u['id']==email]:
            msg = u'This user is already a member.'
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None
        elif [u for u in editors if u['id']==email]:
            msg = u'This user is already a member.'
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None
        else:
            #sends notification to current site administrator
            mail_sender = IMailSender(self.context)
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            portal_title = portal.pretty_title_or_id()
            data['admin_fullname'] = portal.getProperty('email_from_name')
            data['users_settings_url'] = '%s/intranet/users-settings' % \
                self.context.absolute_url()
            subject = "New users notification for %s" % portal_title
            message = self.admin_notify_template(self.context, **data)
            mail_sender.sendMail(subject, message)
            msg ='We are dealing with your registration and you will receive \
an email with your login information shortly.'
            IStatusMessage(self.request).addStatusMessage(msg, type="info")
            
        return object()
        
        
    def nextURL(self):
        if self.next_url:
            return self.next_url
        return "%s/register-user" % self.context.absolute_url() 
    
    
UserRegisterView = wrap_form(UserRegisterForm)

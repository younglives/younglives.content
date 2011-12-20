""" Adds new user. """


# Python
import string, logging

# Zope
from zope import schema
from zope.interface import implements, Interface
from zope.component import getMultiAdapter
from zope.schema import getFieldNamesInOrder
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Plone
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

# local
from younglives.policy import _
from younglives.content.interfaces import IGroupManager, IUserStorage
from younglives.content.interfaces import IUserAddProfile, IUserMultiAddProfile
from younglives.content.interfaces import IMailSender

logger = logging.getLogger('younglives.useradd')

class IMultiForm(Interface):
    """ A markup interface for form with subforms. """

class UserSingleAddForm(form.AddForm):
    template = ViewPageTemplateFile('useraddsingle_form.pt')
    user_notify_template = ViewPageTemplateFile('useradd_mail_template.pt')
    prefix = 'single'
    label = _(u'Add user')
    formErrorsMessage = _('There were some errors.')
    fields = field.Fields(IUserAddProfile)
    errors = {}
    next_url = None
    
    
    def __init__(self, context, request):
        super(UserSingleAddForm, self).__init__(context, request)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        self.user_storage =  IUserStorage(portal)
        self.group_manager = IGroupManager(portal)


    @button.buttonAndHandler(_('Add'), name='add')
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
        
        plone_utils = getToolByName(self.context, 'plone_utils')
        portal_registration = getToolByName(self.context, 'portal_registration')
        acl_users = getToolByName(self.context, 'acl_users')
        
        # user is in pending
        if self.user_storage.get(email):
            msg = u"User '%s' is waiting for your approval." % email
            IStatusMessage(self.request).addStatusMessage(msg, type="info") 
            return object()  
        
        # user already exists
        user = acl_users.getUserById(email)
        if user:
            try:
                if email in self.group_manager._viewers():
                    msg = u"User '%s' is already in viewers group." % email 
                elif email in self.group_manager._editors():  
                    msg = u"User '%s' is already in editors group." % email 
                else:
                    self._add_user_to_viewers(user, data)
                    msg = u"User '%s' already exists. Added to viewers group." \
                        % email
                IStatusMessage(self.request).addStatusMessage(msg, type="info")
                return object()
            except:
                #most possibly cause
                msg = u"User '%s' already exists but not assigned to any \
intranet group. Error: could not find intranets groups." % email
                IStatusMessage(self.request).addStatusMessage(msg, type="error")
                return None
        
        # new user
        password = portal_registration.generatePassword() 
        try:
            portal_registration.addMember(email, password)
        except ValueError:            
            msg = u"The email '%s' is already in use or is not valid." % email
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None

        #set the properties
        user = acl_users.getUserById(email)
        try:
            self._add_user_to_viewers(user, data)
        except:
            #most possibly cause
            msg = u"User '%s' registered but not assigned to any intranet \
groups. Error: could not find intranet groups." % email
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return None
            
        #sends notification to new user
        mail_sender = IMailSender(self.context)
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        portal_title = portal.pretty_title_or_id()
        subject = "New users notification for %s" % portal_title
        options = {}
        options['portal'] = portal
        options['member_id'] = user.getId()
        options['member_username'] = user.getUserName()
        options['member_fullname'] = user.getProperty('fullname', '')
        message = self.user_notify_template(self.context, **options)
        mail_sender.sendMail(subject, message, email_recipient=email)
        msg = u"User '%s' has been added." % email
        IStatusMessage(self.request).addStatusMessage(msg, type="info")
        return object()


    def nextURL(self):
        if self.next_url:
            return self.next_url
        return "%s/add-user" % self.context.absolute_url()


    def _add_user_to_viewers(self, user, data):
        acl_users = getToolByName(self.context, 'acl_users')
        user.setProperties(**data)
        self.group_manager.addViewer(user.getId())
        self.user_storage.remove(user.getId())
        
        
class UserMultiAddForm(form.AddForm):
    template = ViewPageTemplateFile('useraddmulti_form.pt')
    prefix = 'multi'
    label = _(u'Import multiple users')
    formErrorsMessage = _('There were some errors.')
    fields = field.Fields(IUserMultiAddProfile)
    errors = {}
    next_url = None
    
    def updateWidgets(self):
        super(UserMultiAddForm, self).updateWidgets()
        self.widgets['csv'].rows = 10
        self.widgets['csv'].style = u'width:600px;'
    
    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        field_names = getFieldNamesInOrder(IUserAddProfile)
        adduser_view = UserSingleAddForm(self.context, self.request)
        if errors:
           self.status = self.formErrorsMessage
           return
        cols = data['csv'].split('\n')
        for line, row in enumerate(cols):
            user_data = row.split(',')
            if len(user_data)==4:
                user = {}
                for index, field in enumerate(field_names):
                    user[field] = user_data[index].strip()
                result = adduser_view.create(user)
            else:
                msg = u"Wrong number of columns in line %s." % line
                IStatusMessage(self.request).addStatusMessage(msg, type="error")
        # mark only as finished if we get the new object
        self._finishedAdd = True
            
    def nextURL(self):
        if self.next_url:
            return self.next_url
        return "%s/add-user" % self.context.absolute_url()
    
    
class UserAddForm(form.Form):
    template = ViewPageTemplateFile('useradd_form.pt')
    ignoreContext = True
    
    def update(self):
        self.single_add = UserSingleAddForm(self.context, self.request)
        self.single_add.update()
        self.multi_add = UserMultiAddForm(self.context, self.request)
        self.multi_add.update()
        self.subforms = [self.single_add, self.multi_add]
        super(UserAddForm, self).update()


class UserAddView(FormWrapper):
    implements(IMultiForm)
    form = UserAddForm
    def __init__(self, context, request):
        super(UserAddView, self).__init__(context, request)
        
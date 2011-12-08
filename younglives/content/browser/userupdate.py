""" User profile update form. """


# Zope
from AccessControl import Unauthorized
from zope import schema
from zope.interface import implements, Interface
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Plone
from z3c.form import form, field, button
from plone.app.z3cform.layout import FormWrapper
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from plone.memoize import view

# local
from younglives.policy.i18n import younglivesMessageFactory as _
from younglives.content.interfaces import IUserProfile, IUserPassword


class IMultiForm(Interface):
    """ A markup interface for form with subforms. """


def resolveUser(self):
    username = self.request.get('username')
    acl = getToolByName(self.context, 'acl_users')
    mtool = getMultiAdapter((self.context, self.request), 
                            name=u"plone_tools").membership()
    
    if username:
        if not mtool.checkPermission(permissions.ModifyPortalContent, 
                                     self.context):
            raise Unauthorized
        return acl.getUserById(username)
    else:
        return mtool.getAuthenticatedMember()


class UserProfileForm(form.Form):
    template = ViewPageTemplateFile('userupdate-profile_form.pt')
    prefix = 'profile.'
    label = _(u'Personal details')
    formErrorsMessage = _('There were some errors.')
    fields = field.Fields(IUserProfile)
    errors = {}
    
    def getContent(self):
        dict = {}
        user = self.user()
        if user:
            for name in schema.getFieldNames(IUserProfile):
                dict[name] = user.getProperty(name)
        return dict
        
    @view.memoize
    def user(self):
        return resolveUser(self)
    
    @button.buttonAndHandler(u'Update')
    def handleUpdate(self, action):
        data, errors = self.extractData()
        if errors:
            self.errors = errors
            self.status = self.formErrorsMessage
            return
        
        if data:
            try:
                self.user().setProperties(**data)
            except:
                self.error_status = _(u'Updating profile failed.')
                return

        self.status = _(u'Profile successfully updated.')
        return

class UserPasswordForm(form.Form):
    template = ViewPageTemplateFile('userupdate-password_form.pt')
    ignoreContext = True
    prefix = 'password.'
    label = _(u'Login details')
    formErrorsMessage = _('There were some errors.')
    fields = field.Fields(IUserPassword)
    errors = {}
    
    @view.memoize
    def user(self):
        return resolveUser(self)
    
    @button.buttonAndHandler(u'Update')
    def handleUpdate(self, action):
        data, errors = self.extractData()
        if errors:
            self.errors = errors
            self.status = self.formErrorsMessage
            return

        membership = getMultiAdapter((self.context, self.request), 
                                     name=u"plone_tools").membership()
        registration = getToolByName(self.context, u'portal_registration')
        
        password = data.get('password1')
        confirm = data.get('password2')
        failMessage = registration.testPasswordValidity(password, confirm)
        if failMessage:
            self.status = failMessage
            return
        
        acl = getToolByName(self.context, 'acl_users')
        userid = self.user().getId()
        acl.userSetPassword(userid, password)
        membership.credentialsChanged(password)
        self.status = _(u'Password successfuly changed.')
                

class UserUpdateForm(form.Form):
    template = ViewPageTemplateFile('userupdate_form.pt')
    ignoreContext = True
    
    @view.memoize
    def user(self):
        return resolveUser(self)

    def update(self):
        self.profile = UserProfileForm(self.context, self.request)
        self.profile.update()
        self.password = UserPasswordForm(self.context, self.request)
        self.password.update()
        self.subforms = [self.profile, self.password]
        super(UserUpdateForm, self).update()
        
    @property
    def fullname(self):
        user = self.user()
        return user and user.getProperty('fullname') or user.getId()

#wraps this form to disable view actions
class UserUpdateView(FormWrapper):
    implements(IMultiForm)
    form = UserUpdateForm
    def __init__(self, context, request):
        super(UserUpdateView, self).__init__(context, request)
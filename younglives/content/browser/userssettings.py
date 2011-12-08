""" Users management console """ 


# Python
import string, logging
from StringIO import StringIO

# Zope
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Plone
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view

# local
from younglives.content.interfaces import IGroupManager
from younglives.content.interfaces import IUserStorage, IMailSender


logger = logging.getLogger('younglives.usersettings')

class UserSettingsView(BrowserView):
    
    error_status = None
    info_status = None
    user_storage = None
    group_manager = None
    
    approved_template = ViewPageTemplateFile('userapproved_mail_template.pt')
    add_template = ViewPageTemplateFile('useradd_mail_template.pt')
    
    def __init__(self, context, request):
        super(UserSettingsView, self).__init__(context, request)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        self.user_storage =  IUserStorage(portal)
        self.group_manager = IGroupManager(portal)

    def __call__(self):
        
        users = self.request.get("users")
        
        if self.request.has_key("confirm") and users:
            self.approve_users(users)

        elif self.request.has_key("reject") and users:
            self.reject_users(users)
            
        elif self.request.has_key("upgrade") and users:
            self.upgrade_users(users)  
            
        elif self.request.has_key("downgrade") and users:
            self.downgrade_users(users)
            
        elif self.request.has_key("remove") and users:
            self.remove_users(users)
            
        return super(UserSettingsView, self).__call__()
    
    def pending(self):
        return self.user_storage.users().values()
    
    def viewers(self):
        try:
            viewers = self.group_manager.viewers()
            viewers.sort(key=lambda x: x['fullname'].lower())
            return viewers
        except:
            self.error_status = "Could not find intranet viewers group."
        return []
    
    def editors(self):
        try:
            editors = self.group_manager.editors()
            editors.sort(key=lambda x: x['fullname'].lower())
            return editors
        except:
            self.error_status = "Could not find intranet editors group."
        return []
    
    def remove_users(self, users):
        acl_users = getToolByName(self.context, 'acl_users')
        gtool = getToolByName(self.context, 'portal_groups')
        mtool = getToolByName(self, 'portal_membership')
    
        not_removable_users = []
        for userid in users:
            self.group_manager.removeUser(userid)
            # remove from portal only if plain member 
            # who doesn't belong to any other groups 
            try:
                user = acl_users.getUserById(userid)
                groups = gtool.getGroupsForPrincipal(user)
                roles = user.getRoles()
                logger.info(roles)
                logger.info(groups)
                if len(groups)==1 and 'AuthenticatedUsers' in groups:
                    if len(roles)==2 and ('Member' and 'Authenticated' in roles):
                        mtool.deleteMembers(userid, 
                                            delete_memberareas=0, 
                                            delete_localroles=1, 
                                            REQUEST=self.context.REQUEST)
                    else: 
                        not_removable_users.append(userid)
                else:
                    not_removable_users.append(userid) 
            except:
                pass
        if not_removable_users:
            self.info_status = u"Could not completely remove following users \
from portal: %s. They belong to other groups or have higher permissions then \
Member. Please go to Settings / Users and Groups to delete them." % \
(', '.join(not_removable_users))
            return
        self.info_status = u"Selected viewers have been removed."
        
    def reject_users(self, users):
        mail_sender = IMailSender(self.context)
        
        for user in users:
            self.user_storage.remove(user)
            # TODO notification mail
            
    def upgrade_users(self, users):
        for user in users:
            self.group_manager.upgradeViewer(user)
        next_url = "%s/users-settings#fieldsetlegend-editors" % \
            self.context.absolute_url()
        info_status = u"Selected viewers have been upgraded."
        self.context.plone_utils.addPortalMessage(info_status, 'info')
        self.request.response.redirect(next_url)
            
    def downgrade_users(self, users):
        for user in users:
            self.group_manager.degradeEditor(user)
        next_url = "%s/users-settings#fieldsetlegend-viewers" % \
            self.context.absolute_url()
        info_status = u"Selected editors have been degraded."
        self.context.plone_utils.addPortalMessage(info_status, 'info')
        self.request.response.redirect(next_url)
            
    def approve_users(self, users):
        acl_users = getToolByName(self.context, 'acl_users')
        portal_registration = getToolByName(self.context, 'portal_registration')
        
        #creates portal members
        for userid in users:
            try:
                if acl_users.getUserById(userid):
                    user_notify_template = self.approved_template
                else:
                    password = portal_registration.generatePassword()
                    portal_registration.addMember(userid, password)
                    user_notify_template = self.add_template
            except ValueError:            
                self.error_status = \
                    u"The email %s is already in use or not valid." % userid
                return
            
            #set user properties
            data = self.user_storage.get(userid)
            user = acl_users.getUserById(userid)
            user.setProperties(**data)
            self.user_storage.remove(userid)
    
            #adds members to viewers group.
            try:
                self.group_manager.addViewer(userid)
            except:
                viewers = self.group_manager._getViewersGroup()
                #probably cause
                self.error_status = "Could not find %s group." % viewers
            
            #user approval notification
            mail_sender = IMailSender(self.context)
            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            portal_title = portal.pretty_title_or_id()
            subject = "New users notification for %s" % portal_title
            options = {}
            options['portal'] = portal
            options['portal_title'] = portal_title
            options['member_id'] = user.getId()
            options['member_username'] = user.getUserName()
            options['member_fullname'] = user.getProperty('fullname', '')
            message = user_notify_template(self.context, **options)
            mail_sender.sendMail(subject, message, email_recipient=userid)
            next_url = "%s/users-settings#fieldsetlegend-viewers" % \
                self.context.absolute_url()
            info_status = u"Selected viewers have been approved."
            self.context.plone_utils.addPortalMessage(info_status, 'info') 
            self.request.response.redirect(next_url)
            
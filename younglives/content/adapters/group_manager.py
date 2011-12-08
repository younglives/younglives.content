""" Group manager: helps adding, removing and assigning members to groups. """


# Python
from datetime import datetime, timedelta

# Zope
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

# local
from younglives.content.interfaces import IGroupManager
from younglives.content.utils import runAsGod


VIEWERS_GROUP = "intranet_viewers"
EDITORS_GROUP = "intranet_editors"

class GroupManager(object):
    implements(IGroupManager)
   
    def __init__(self, context):
        self.context = context
        self.acl_users = getToolByName(self.context, 'acl_users')
        self.portal_groups = getToolByName(self.context, 'portal_groups')
        
        
    def initGroups(self):
        """ Prepares the group """
        
        acl_users = getToolByName(self.context, 'acl_users')
        portal_groups = getToolByName(self.context, 'portal_groups')
        
        self.context.__ac_local_roles_block__ = False 

        # adds editors group
        if acl_users.getGroupById(EDITORS_GROUP) is None:
            portal_groups.addGroup(EDITORS_GROUP)
        self.context.manage_addLocalRoles(EDITORS_GROUP, ['Contributor',
                                                          'Editor',
                                                          'Reader'])

        # adds viewers group
        if acl_users.getGroupById(VIEWERS_GROUP) is None:
            portal_groups.addGroup(VIEWERS_GROUP)             
        self.context.manage_addLocalRoles(VIEWERS_GROUP, ['Reader'])  


    def viewers(self):
        """ Looks up all users in viewers group"""
        users = self._viewers()
        return self._getUsersData(users)
   
    def editors(self):
        """ Looks up all users in editors group"""
        users = self._editors()
        return self._getUsersData(users)
    
    @runAsGod
    def addViewer(self, user_id):
        self._addViewer(user_id)
        self.context.reindexObject()
    
    @runAsGod
    def addEditor(self, user_id):
        self._addEditor(user_id)
        self.context.reindexObject()
        
    @runAsGod
    def upgradeViewer(self, user_id):
        self._removeViewer(user_id)
        self._addEditor(user_id)
        self.context.reindexObject()

    @runAsGod
    def degradeEditor(self, user_id):
        self._removeEditor(user_id)
        self._addViewer(user_id)
        self.context.reindexObject()

    @runAsGod
    def removeUser(self, user_id):
        self._removeViewer(user_id)
        self._removeEditor(user_id)
        self.context.reindexObject()

    
    #===========================================================================
    # Helpers
    #===========================================================================
    def _viewers(self):
        """ Looks up all users in viewers group """
        users = set(self._getGroupUsers(VIEWERS_GROUP))
        return list(users)

    def _editors(self):
        """ Looks up all users in editors group """
        users = set(self._getGroupUsers(EDITORS_GROUP))
        return list(users)
    
    def _addViewer(self, user_id):
        """ Adds user as a viewer - adds user to a viewers group """
        acl_users = getToolByName(self.context, 'acl_users')
        group = acl_users.getGroupById(VIEWERS_GROUP)
        group.addMember(user_id)
        
    def _addEditor(self, user_id):
        """ Adds user as a editor - adds user to a editors group """
        acl_users = getToolByName(self.context, 'acl_users')
        group = acl_users.getGroupById(EDITORS_GROUP)
        group.addMember(user_id)
        
    def _removeViewer(self, user_id):
        """ Removes user as a viewer """
        group = self.acl_users.getGroupById(VIEWERS_GROUP)
        group.removeMember(user_id)
    
    def _removeEditor(self, user_id):
        """ Removes user as a editor """
        group = self.acl_users.getGroupById(EDITORS_GROUP)
        group.removeMember(user_id)
        
    def _getGroupUsers(self, group_id):
        group = self.acl_users.getGroupById(group_id)
        return group.getAllGroupMemberIds()
    
    
    def _getUsersData(self, users):
        acl_users = getToolByName(self.context, 'acl_users')
        usersdata = []
        for user_id in users:
            user = acl_users.getUserById(user_id)
            user_dict = dict(
                id = user.getId(),
                fullname = user.getProperty('fullname') or user_id,
                email = user.getProperty('email'),
                location = user.getProperty('location') or '',
                jobtitle = user.getProperty('jobtitle') or '')
            usersdata.append(user_dict)
        return usersdata

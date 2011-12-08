""" Export intranet viewers/editors group users to CVS file. """


#Python
from time import strftime

# Zope
from zope.schema import getFieldNames

# Plone
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

# local
from younglives.policy.i18n import younglivesMessageFactory as _
from younglives.content.interfaces import IGroupManager, IUserStorage, \
    IUserProfile


class UsersExportView(BrowserView):

    def __call__(self):
        """ Exports users to CSV file. """
        
        text = ''
        
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.group_manager = IGroupManager(portal)
        self.field_names = getFieldNames(IUserProfile)
    
        memberProperties = []
        for name in self.field_names:
            memberProperties.append(name)
        memberProperties.append('email')
        memberProperties.append('group')
        
        membership = getToolByName(self.context, 'portal_membership')
        
        for p in memberProperties:
            text += p + ','
            
        #remove trailing comma
        text=text[:-1]
        
        text += chr(13)+chr(10) #first line has been written
        text += self.records(self._pending(), 'pending')
        text += self.records(self._viewers(), 'viewers')
        text += self.records(self._editors(), 'editors')
        
        filename = 'intranet_users_%s.csv' % strftime("%Y%m%d")
        self.context.REQUEST.response.setHeader("Content-type", "text/csv")
        self.request.response.setHeader('Content-Disposition', 'attachment; \
filename="%s"' % filename)
        
        return text
    
    def records(self, members, group=''):
        text = ''
        for member in members:
            for name in self.field_names:
                text+='%s,' % member[name]
            text+='%s,' % member['email']
            text+=group
            text+='\n'
        return text
    
    def _pending(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        user_storage = IUserStorage(portal)
        return user_storage.users().values()
    
    def _viewers(self):
        try:
            viewers = self.group_manager.viewers()
            return viewers
        except:
            return []
    
    def _editors(self):
        try:
            editors = self.group_manager.editors()
            return editors
        except:
            return []
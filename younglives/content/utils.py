""" Various utilities """


# Zope
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

# Plone
from Products.CMFCore.utils import getToolByName

    
def makeMeGOD(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    # Don't make me god if I already am ( sort of )
    membership = getToolByName(context, 'portal_membership')
    if membership.checkPermission("Manage users", portal):
        return None

    uf = getToolByName(portal, 'acl_users')
    user = uf.getUserById("user_manager")
    if not hasattr(user, 'aq_base'):
        user = user.__of__(uf)
    sm = getSecurityManager()
    newSecurityManager(None, user)
    return sm

def makeMeHuman(sm):
    if sm:
        setSecurityManager(sm)

def runAsGod(fn):
    
    def grant_privilages(self, *args, **kw):
        sm = makeMeGOD(self.context)
        result = fn(self, *args, **kw)
        if sm:
            makeMeHuman(sm)
        return result
    return grant_privilages
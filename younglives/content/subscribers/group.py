""" Creates intranet groups """


# local
from younglives.content.interfaces import IGroupManager


def initGroups(obj, event):
    """ Creates plone groups for moderators and members """
    
    group_manager = IGroupManager(obj)
    group_manager.initGroups()
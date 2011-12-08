""" Adapters interfeaces. """


# Zope
from zope.interface import Interface

    
class IGroupManager(Interface):
    """ An adapter to get info and manipulate subsites groups. """
        
    def editors():
        """ Return assigned editors -
            looks up all users in editors group.
        """
    
    def viewers():
        """ Return assigned viewers -
            looks up all users in viewers group.
        """
        
class IUserStorage(Interface):
    """ Adapter for storing not yet approved users. """
    
class ICapturedDataStorage(Interface):
    """ Adapter for storing data captured in pop-ups. """
    
    
class IMailSender(Interface):
    """ An adapter to simplify email sending. """
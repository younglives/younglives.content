""" Interfaces for browser views. """

# Zope
from zope.interface import Interface

#===============================================================================
# content types views
#===============================================================================

class IPublicationView(Interface):
    """ Publication content type view. """
    
#===============================================================================
# general views
#===============================================================================
class IFolderListingView(Interface):
    """ Replacement for folder listing """
    
#===============================================================================
# marker interfaces
#===============================================================================

class IIntranetFolderMarker(Interface):
    """ Marker interface for Intranet folder. """

class IOurPublicationsFolderMarker(Interface):
    """ Marker interface for Our Publications folder. """
    
class IOurThemesFolderMarker(Interface):
    """ Marker interface for Our Themes folder. """
    
class IWhatWeDoFolderMarker(Interface):
    """ Marker interface for What We Do folder. """
    
class IWhereWeWorkFolderMarker(Interface):
    """ Marker interface for Where We Work folder. """
    
class IWhoWeAreFolderMarker(Interface):
    """ Marker interface for Who We Are folder. """
    
class INewsletterMarker(Interface):
    """ Marker interface for newsletter form. """

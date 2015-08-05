""" Interfaces for browser views. """

# Zope
from zope.interface import Interface

# =============================================================================
# general views
# =============================================================================


class IFolderListingView(Interface):
    """ Replacement for folder listing """

# =============================================================================
# marker interfaces
# =============================================================================


class INewsletterMarker(Interface):
    """ Marker interface for newsletter form. """

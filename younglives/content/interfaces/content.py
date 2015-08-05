""" Interfaces for content types. """
"""
http://plone.org/products/collective.blogging/issues/7
In the uninstall code you can probably repeat over all content with that marker
using the object_provides index, and call noLongerProvides on it.
"""
# Zope
from zope.interface import Interface

# =============================================================================
# markers
# =============================================================================

class IGalleryContainerMarker(Interface):
    """ Marker interface for gallery folders. """

# =============================================================================
# extenders
# =============================================================================


class IBannerAware(Interface):
    """ For all items with with banner image. """


class ICategoriesAware(Interface):
    """ For all items with with additional keywords fields. """


class IGalleryContainerAware(Interface):
    """ For all gallery folders. """


class IQuoteAware(Interface):
    """ Adds a field and displays it at the footer as a quote. """
    # TODO remove this interface


class ISortableAware(Interface):
    """ For all items with sortable content. """

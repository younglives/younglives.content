""" Default browser view for News items. """


# Zope
from Acquisition import aq_parent

# Plone
from plone.memoize import view
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class NewsView(BrowserView):
    pass
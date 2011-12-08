""" Default browser view for listing items. """

# Python
import logging


# Zope
from zope.interface import implements
from zope.component import getMultiAdapter

# Plone
from Products.ATContentTypes.interface import IATTopic
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch
from plone.app.layout.icons.interfaces import IContentIcon
from plone.memoize import view

# local
from younglives.content.interfaces import IFolderListingView


logger = logging.getLogger('younglives.folderlisting')

class FolderListingView(BrowserView):
    implements(IFolderListingView)
    
    @view.memoize
    def banner(self):
        banner_field = self.context.getField("bannerImage")
        if banner_field:
            return banner_field.get(self.context)
        return None
    
    @view.memoize
    def items(self):
        catalog = getToolByName(self, 'portal_catalog')
        plone_view = getMultiAdapter((self.context, self.request), name=u'plone')
        
        path = self.context.getPhysicalPath()
        path = "/".join(path) 
        
        if IATTopic.providedBy(self.context):
            items = self.context.queryCatalog()
        else:
            sort_on = 'getObjPositionInParent'
            sort_order = 'ascending'
            sort_on_field = self.context.getField('sortOn')
            if sort_on_field and sort_on_field.get(self.context):
                sort_on = sort_on_field.get(self.context)[0]
            sort_order_field = self.context.getField('sortOrder')
            if sort_order_field and sort_order_field.get(self.context):
                sort_order = sort_order_field.get(self.context)[0]
            items = catalog.searchResults(path = {'query':path, 'depth':1},
                                          sort_on = sort_on,
                                          sort_order = sort_order)
            
        b_start = self.request.get('b_start', 0)
        return Batch(items, 20, int(b_start), orphan=0)
        
    def snippet(self, brain):
        obj = brain.getObject()
        render =  getMultiAdapter( (obj, self.request), name="listing_snippet")
        return render()
        
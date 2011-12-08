""" Default browser view for Homepage item. """

# Zope
from zope.interface import implements

# Plone
from Products.ATContentTypes.interfaces import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.memoize import view

# local
from younglives.content.interfaces import IHomePageView 
from younglives.content.interfaces import IHomepageBoxAware, IHomepageHeroMarker


class HomePageView(BrowserView):
    implements(IHomePageView)
    
    
    @view.memoize
    def html_description(self):
        portal_transforms = getToolByName(self.context, 'portal_transforms')
        return portal_transforms.convert('text_to_html', 
                                         self.context.Description())
      
        
    @view.memoize   
    def homepage_boxes(self):
        items = []
        home_boxes_ref = self.context.getHomeBoxes()
        for box_ref in home_boxes_ref:
            if IHomepageBoxAware.providedBy(box_ref):
                item = dict(title = box_ref.Title(),
                            url = box_ref.absolute_url(),
                            description = box_ref.Description(),
                            links = [])
                brains = box_ref.queryCatalog()
                for brain in brains:
                    item['links'].append(dict(title = brain.Title,
                                              url = brain.getURL(),))                            
                items.append(item)
        
        return items

  
    @view.memoize 
    def homepage_news(self):
        item = None
        home_news_ref = self.context.getHomeNews()
        if IHomepageBoxAware.providedBy(home_news_ref):
            item = dict(title = home_news_ref.Title(),
                        url = home_news_ref.absolute_url(),
                        links = [])
            brains = home_news_ref.queryCatalog()
            for brain in brains:
                item['links'].append(dict(title = brain.Title,
                                          url = brain.getURL(),
                                          date = brain.Date))
        
        return item


    @view.memoize
    def boxes(self):
        wtool = getToolByName(self.context, 'portal_workflow')
        results = []
        for box in ["1","2","3"]:
            links = eval("self.context.getBox%sLinks()" % box) or []
            results.append( dict(
                title = eval("self.context.getBox%sTitle" % box),
                description = eval("self.context.getBox%sDescription()" % box),
                image = eval("self.context.getBox%sImage()" % box),
                links = [{'title':x.Title,'url':x.absolute_url} for x in links],))
        return results


    def rotator_images(self):
        ctool = getToolByName(self.context, 'portal_catalog')
        return ctool(UID=self.context.getRawHomeRotatorImages())
  

""" A portlet which shows image with link to gallery it's coming from. """


# Python
from random import choice

# Zope
from Acquisition import aq_inner
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.app.form.browser import RadioWidget as _RadioWidget

# CMF
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

# Plone
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import IContextSourceBinder, \
  SearchableTextSource

# local
from younglives.policy.i18n import younglivesMessageFactory as _
from younglives.content.interfaces import IGalleryContainerMarker


def RadioWidget(field, request):
    vocabulary = field.vocabulary
    widget = _RadioWidget(field, vocabulary, request)
    return widget


class GallerySourceBinder:

    implements(IContextSourceBinder)

    def __call__(self,context):
        catalog = getToolByName(context, 'portal_catalog')
        terms = []
        
        galleries = catalog(object_provides = IGalleryContainerMarker.__identifier__)
        for gallery in galleries:
            gallery_obj = gallery.getObject()
            path = gallery_obj.getPhysicalPath()
            path = "/".join(path) 
            images = catalog.searchResults(path = {'query':path, 'depth':1},
                                           portal_type = 'Image',
                                           sort_on = "getObjPositionInParent")
            if images:
                image = images[0]
                value = "<a href='%s' target='_blank'><img src='%s/image_mini'/></a>" % \
                    (gallery.getURL(), image.getURL())
            else:
                value = "<a href='%s' target='_blank'>%s</a> (EMPTY GALLERY)" % \
                    (gallery.getURL(), gallery.Title)
            term = SimpleVocabulary.createTerm(gallery.UID, gallery.UID, safe_unicode(value))
            terms.append(term)
            
        return SimpleVocabulary(terms)
    

class IGalleryPortlet(IPortletDataProvider):
    """ A portlet which shows image with link to gallery it's coming from. """
    
    gallery = schema.Choice(title = _(u'Gallery'),
                            description = _(u"Select gallery."),
                            source = GallerySourceBinder())       

class Assignment(base.Assignment):
    
    implements(IGalleryPortlet)

    def __init__(self, gallery=()):
        self.gallery = gallery

    @property
    def title(self):
        return "Gallery Portlet"


class Renderer(base.Renderer):        

    @property
    def available(self):
        return self.first_image() is not None
    
    @memoize 
    def gallery(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        galleries = catalog(UID = self.data.gallery, 
                            object_provides = IGalleryContainerMarker.__identifier__)
        if galleries:
            return galleries[0]
        
        return None
        
    @memoize 
    def first_image(self):
        gallery = self.gallery()
        if gallery:
            context = aq_inner(self.context)
            catalog = getToolByName(context, 'portal_catalog')
            gallery_obj = gallery.getObject()
            path = gallery_obj.getPhysicalPath()
            path = "/".join(path)
            images = catalog.searchResults(path = {'query':path, 'depth':1},
                                           portal_type = 'Image',
                                           sort_on = "getObjPositionInParent")
            if images:
                image = images[0]
                return image.getObject()
            
        return None
    
    render = ViewPageTemplateFile("gallery.pt")
    
    
class AddForm(base.AddForm):

    form_fields = form.Fields(IGalleryPortlet)
    label = _(u"gallery-portlet_add_label",
              default=u"Add gallery portlet")
    description = _(u"gallery-portlet_add_desc",
                    default=u"A portlet which can display selected Young Lives \
gallery first image.")
    
    def create(self, data):
        return Assignment(**data)

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
        self.form_fields['gallery'].custom_widget = RadioWidget
    

class EditForm(base.EditForm):

    form_fields = form.Fields(IGalleryPortlet)
    label = _(u"gallery-portlet_edit_label",
              default=u"Edit gallery portlet")
    description = _(u"gallery-portlet_edit_desc",
                    default=u"A portlet which can display selected Young Lives \
gallery image.")
    
    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.form_fields['gallery'].custom_widget = RadioWidget
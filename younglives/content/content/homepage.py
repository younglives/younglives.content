""" Definition of the HomePage content type. """


# Zope
from zope.interface import implements

# Plone
from Products.Archetypes import atapi
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

# ext
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.OrderableReferenceField import \
     OrderableReferenceField, OrderableReferenceWidget

# local
from younglives.policy.i18n import younglivesMessageFactory as _
from younglives.content.interfaces import IHomePage
from younglives.content.interfaces import IHomepageBoxMarker, IHomepageHeroMarker
from younglives.content.config import *


HomePageSchema = ATDocument.schema.copy() + atapi.Schema((
                                                          
    atapi.TextField("homeQuote",
        required = 0,
        searchable = 1,
        languageIndependent = 1,
        storage = atapi.AnnotationStorage(),
        widget = atapi.TextAreaWidget(
            label = _(u"homepage_quote_label",
                      default = u"Quote"),
            description = _(u"subsite_quote_desc",
                            default = u"Enter homepage quote."),
            rows = 2)),
            
    OrderableReferenceField('homeRotatorImages',
        required = 1,
        multiValued = 1,
        relationship = 'relatedHomepageRotatorImages',
        widget = ReferenceBrowserWidget(
            allow_sorting = 1,          
            hide_inaccessible = 1,
            force_close_on_insert = 0,
            allow_search = 0, 
            allow_browse = 0,
            show_review_state = 1,
            image_portal_types = ('Page','Publication'),
            image_method = 'homepageHeroImage_thumb', 
            base_query = {'object_provides' : IHomepageHeroMarker.__identifier__},
            show_results_without_query = 1,             
            label = _(u"Rotator images"),
            description = _(u"Choose images for rotator."),)),
    
    #===========================================================================
    # Box 1 
    #===========================================================================
    atapi.TextField("box1Title",
                    required = 0,
                    schemata = 'Box1',
                    searchable = 1,
                    languageIndependent = 1,
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.StringWidget(
                        label = _(u"homepage_box1-title_label",
                          default = u"Box 1 title"),
                        description = _(u"homepage_box1-title_desc",
                          default = u"Enter title for first homepage box."),)), 

    atapi.TextField("box1Description",
                         required = 0,
                         schemata = 'Box1',
                         languageIndependent = 0,
                         storage = atapi.AnnotationStorage(),
                         widget = atapi.TextAreaWidget(
                           label = _(u"homepage_box1-desc_label",
                             default = u"Box 1 description"),
                           description = _(u"homepage_box1-desc_desc",
                             default = u"Enter description for this box."),)),

    atapi.ImageField("box1Image",
                    required = 0,
                    schemata = 'Box1',
                    languageIndependent = 1,
                    pil_quality = 100,
                    original_size = (222, 87),
                    validsizes = (222, 87),
                    validators = ("checkImageSize",),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.ImageWidget(
                        label = _(u"homepage_box1-image_label",
                          default = u"Box 1 image"),
                        description = _(u"homepage_box1-image_desc",
                          default = u"Upload image for first homepage box. \
Required size is 222x87px."),)),                          

    OrderableReferenceField("box1Links",
                         required = 0,
                         schemata = 'Box1',
                         multiValued = 1,
                         languageIndependent = 0,
                         storage = atapi.AnnotationStorage(),
                         relationship = "homepageRelatedBox1Links",
                         widget = ReferenceBrowserWidget(
                           allow_sorting = 1,
                           hide_inaccessible = 1,
                           force_close_on_insert = 0,             
                           label = _(u"homepage_box1-links_label",
                             default = u"Box 1 links"),
                           description = _(u"homepage_box1-links_desc",
                             default = u"Select featured links for this box."),)),
                             

    #===========================================================================
    # Box 2 
    #===========================================================================
    atapi.TextField("box2Title",
                    required = 0,
                    schemata = 'Box2',
                    searchable = 1,
                    languageIndependent = 1,
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.StringWidget(
                        label = _(u"homepage_box2-title_label",
                          default = u"Box 2 title"),
                        description = _(u"homepage_box2-title_desc",
                          default = u"Enter title for first homepage box."),)), 

    atapi.TextField("box2Description",
                         required = 0,
                         schemata = 'Box2',
                         languageIndependent = 0,
                         storage = atapi.AnnotationStorage(),
                         widget = atapi.TextAreaWidget(
                           label = _(u"homepage_box2-desc_label",
                             default = u"Box 2 description"),
                           description = _(u"homepage_box2-desc_desc",
                             default = u"Enter description for this box."),)),

    atapi.ImageField("box2Image",
                    required = 0,
                    schemata = 'Box2',
                    languageIndependent = 2,
                    pil_quality = 100,
                    original_size = (222, 87),
                    validsizes = (222, 87),
                    validators = ("checkImageSize",),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.ImageWidget(
                        label = _(u"homepage_box2-image_label",
                          default = u"Box 2 image"),
                        description = _(u"homepage_box2-image_desc",
                          default = u"Upload image for first homepage box. \
Required size is 222x87px."),)),                          

    OrderableReferenceField("box2Links",
                         required = 0,
                         schemata = 'Box2',
                         multiValued = 1,
                         languageIndependent = 0,
                         storage = atapi.AnnotationStorage(),
                         relationship = "homepageRelatedBox2Links",
                         widget = ReferenceBrowserWidget(
                           allow_sorting = 1,
                           hide_inaccessible = 1,
                           force_close_on_insert = 0,             
                           label = _(u"homepage_box2-links_label",
                             default = u"Box 2 links"),
                           description = _(u"homepage_box2-links_desc",
                             default = u"Select featured links for this box."),)),

    #===========================================================================
    # Box 3 
    #===========================================================================
    atapi.TextField("box3Title",
                    required = 0,
                    schemata = 'Box3',
                    searchable = 1,
                    languageIndependent = 1,
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.StringWidget(
                        label = _(u"homepage_box3-title_label",
                          default = u"Box 3 title"),
                        description = _(u"homepage_box3-title_desc",
                          default = u"Enter title for first homepage box."),)), 

    atapi.TextField("box3Description",
                         required = 0,
                         schemata = 'Box3',
                         languageIndependent = 0,
                         storage = atapi.AnnotationStorage(),
                         widget = atapi.TextAreaWidget(
                           label = _(u"homepage_box3-desc_label",
                             default = u"Box 3 description"),
                           description = _(u"homepage_box3-desc_desc",
                             default = u"Enter description for this box."),)),

    atapi.ImageField("box3Image",
                    required = 0,
                    schemata = 'Box3',
                    languageIndependent = 1,
                    pil_quality = 100,
                    original_size = (222, 87),
                    validsizes = (222, 87),
                    validators = ("checkImageSize",),
                    storage = atapi.AnnotationStorage(),
                    widget = atapi.ImageWidget(
                        label = _(u"homepage_box3-image_label",
                          default = u"Box 3 image"),
                        description = _(u"homepage_box3-image_desc",
                          default = u"Upload image for first homepage box. \
Required size is 222x87px."),)),                          

    OrderableReferenceField("box3Links",
                         required = 0,
                         schemata = 'Box3',
                         multiValued = 1,
                         languageIndependent = 0,
                         storage = atapi.AnnotationStorage(),
                         relationship = "homepageRelatedBox3Links",
                         widget = ReferenceBrowserWidget(
                           allow_sorting = 1,
                           hide_inaccessible = 1,
                           force_close_on_insert = 0,             
                           label = _(u"homepage_box3-links_label",
                             default = u"Box 3 links"),
                           description = _(u"homepage_box3-links_desc",
                             default = u"Select featured links for this box."),)),

    
    atapi.ReferenceField('homeNews',
        required = 0,
        multiValued = 0,
        relationship = 'relatedHomepageNews',
        allowed_types = ('Topic',),
        widget = ReferenceBrowserWidget(
            hide_inaccessible = 1,
            force_close_on_insert = 0,
            allow_search = 0, 
            allow_browse = 0,
            allow_sorting = 1,
            show_review_state = 1,
            image_portal_types = ('Collection',),
            image_method = '++atfield++homepageBoxImage-thumb', 
            base_query = {'object_provides' : IHomepageBoxMarker.__identifier__},
            show_results_without_query = 1,
            label = _(u"homepage_news_label", 
                      default = u"News"),
            description = _(u"homepage_news_desc", 
                            default = u"Select collection to show its contents \
on homepage news section."),)), 

              
    atapi.ImageField("homeFooterImage",
        required = 0,
        languageIndependent = 1,
        pil_quality = 100,
        original_size = (468, 128),
        validsizes = (468, 128),
        validators = ("checkImageSize",),
        storage = atapi.AnnotationStorage(),
        widget = atapi.ImageWidget(
            label = _(u"homepage-footer-image_label",
                      default = u"Image"),
            description = _(u"homepage-footer-image_desc",
                            default = u"Upload image for homepage footer. \
Required size is 468x128px."),)),
    
    ))

HomePageSchema["title"].storage = atapi.AnnotationStorage()
HomePageSchema["description"].storage = atapi.AnnotationStorage()
HomePageSchema["text"].storage = atapi.AnnotationStorage()
HomePageSchema["text"].widget.visible = {"view":"invisible", 
                                         "edit":"invisible"}

schemata.finalizeATCTSchema(HomePageSchema, moveDiscussion=False)


class HomePage(ATDocument):
    """ YoungLives homepage archetype. """
    implements(IHomePage)

    meta_type = "HomePage"
    schema = HomePageSchema
    

atapi.registerType(HomePage, PROJECTNAME)
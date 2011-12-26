""" A portlet which shows latest items. """
## Thanks to Radim Novotny and his brilliant Plone knowledge


# Zope
from Acquisition import aq_inner
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.schema.vocabulary import SimpleVocabulary
from zope.app.form.browser import RadioWidget as _RadioWidget

# Plone
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.cache import render_cachekey
from plone.app.controlpanel.widgets import MultiCheckBoxColumnsWidget
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.vocabularies.catalog import IContextSourceBinder, \
  SearchableTextSource
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ATContentTypes.interface.document import IATDocument
from Products.ATContentTypes.interface.image import IATImage

# local
from younglives.policy import _

class ILatestItemsPortlet(IPortletDataProvider):
    """ A portlet which shows latest items. """
    
    header = schema.TextLine(title = _(u"Portlet header"),
        description = _(u"Title of the portlet"),
        required = 1,
        default = u"Latest")
                               
    item_types = schema.Tuple(title = _(u"Item types"),
        description = _(u"Choose which items to show."),
        required = 1,
        value_type = schema.Choice(
            vocabulary = "younglives.content.LatestItemsAvailableTypes"))
    
    count = schema.Int(title = _(u'Number of items to display'),
        description = _(u'How many items to list.'),
        required = 1,
        default = 5)


class Assignment(base.Assignment):
    implements(ILatestItemsPortlet)
    
    header = u"Latest"
    item_types = ()
    count = 5
    
    def __init__(self, header=u"Latest", item_types=(), count=5):
        super(Assignment, self).__init__()
        self.header = header
        self.item_types = item_types
        self.count = count 
        
    @property
    def raw_title(self):
        return u"Latest items"
        
    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):
    
    _template = ViewPageTemplateFile('latest.pt')

    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return True

    def items(self):
        return self._data()
        
    def title(self):
        return self.data.title
        
    @memoize
    def _data(self):
        limit = self.data.count
        # If limit set to 0, return an empty list (displaying only image and text)
        if limit < 1:
            return []

        catalog = getMultiAdapter((self.context, self.request), 
                                  name="plone_tools").catalog()
            
        query = dict(portal_type = self.data.item_types,
                     sort_on = 'Date',
                     sort_order = 'reverse',
                     sort_limit = limit)
        
        return  catalog(**query)[:limit]


class AddForm(base.AddForm):
    """ Portlet add form. """
    
    form_fields = form.Fields(ILatestItemsPortlet)

    label = _(u"portlet_latest-items_add_title",
              default = u"Add latest items portlet")
    description = _(u"portlet_latest-items_add_desc",
                    default = u"A portlet which displays latest items")

    def create(self, data):
        return Assignment(**data)
    
    
class EditForm(base.EditForm):
    """ Portlet edit form. """

    form_fields = form.Fields(ILatestItemsPortlet)
    label = _(u"portlet_latest-items_edit_title",
              default = u"Edit latest items portlet")
    description = _(u"portlet_latest-items_edit_desc",
                    default = u"A portlet which displays latest items")

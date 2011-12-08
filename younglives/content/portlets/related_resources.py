""" A portlet which shows current context keywords matching items. """


# Python
import logging

# Zope
from Acquisition import aq_inner
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

# Plone
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from Products.AdvancedQuery import In, And, Not, Eq, Or
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local
from younglives.policy.i18n import younglivesMessageFactory as _


logger = logging.getLogger('younglives.RelatedResourcesPortlet')

class IRelatedResourcesPortlet(IPortletDataProvider):
    """ A portlet which shows current context keywords matching items. """
    
    header = schema.TextLine(title = _(u"Portlet header"),
        description = _(u"Title of the portlet"),
        required = 1,
        default = u"Related resources")
    
    item_type = schema.Tuple(title = _(u"Item types"),
        description = _(u"Choose which items to show."),
        required = 0,
        value_type = schema.Choice( 
            vocabulary = "younglives.content.RelatedResourcesAvailableTypes"))
    
    sort_by = schema.Choice(title = _(u"Sort by"),
        description = _(u"Choose sorting order."),
        required = 0,
            vocabulary = "younglives.content.RelatedResourcesSortIndexes")


class Assignment(base.Assignment):
    
    implements(IRelatedResourcesPortlet)
    
    header = u"Related resources"
    item_type = ()
    sort_by = None
    
    def __init__(self, header=u"Related resources", item_type=(), sort_by=None):
        super(Assignment, self).__init__()
        self.header = header
        self.item_type = item_type
        self.sort_by = sort_by

    @property
    def raw_title(self):
        return u"Related resources"
    
    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('related_resources.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        self.title = self.data.title
        self.item_type = self.data.item_type
        self.sort_by = self.data.sort_by

    @property
    def available(self):
        return self.items() is not None and len(self.items())
    
    @memoize
    def title(self):
        return self.title

    @memoize
    def items(self):
        context = aq_inner(self.context)
        catalog = getMultiAdapter((self.context, self.request), 
                                  name="plone_tools").catalog()
        context_brains = catalog(UID=context.UID())
        if not context_brains:
            return []
        themes = context_brains[0].theme
        topics = context_brains[0].topic
        # matches all items (except current context) 
        # with at least one shared topic or theme 
        query = Or(In('theme',themes), In('topic',topics)) & \
            ~ Eq('UID',context.UID())
        if self.item_type:
            query &= Eq('portal_type', self.data.item_type)
        results =  catalog.evalAdvancedQuery(query)
        # only 3 items with most shared occurrences of topic or theme
        results = sorted(results, 
                         cmp = lambda a,b:cmp(len(set(a.theme) & set(themes)) + 
                                              len(set(a.topic) & set(topics)), 
                                              len(set(b.theme) & set(themes)) + 
                                              len(set(b.topic) & set(topics))),
                         reverse = True)[:3]
        
        # latest first                 
        if self.sort_by:
            index = self.sort_by
            return sorted(results,
                          cmp = lambda a,b:cmp(a[index], b[index]),
                          reverse = True)
        
        return results


class AddForm(base.AddForm):
    """ Portlet add form. """
    
    form_fields = form.Fields(IRelatedResourcesPortlet)

    label = _(u"portlet_related-resources_add_title",
              default = u"Add related resources portlet")
    description = _(u"portlet_related-resources_add_desc",
                    default = u"A portlet which displays related resources")

    def create(self, data):
        return Assignment(**data)
    
    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
    
    
class EditForm(base.EditForm):
    """ Portlet edit form. """

    form_fields = form.Fields(IRelatedResourcesPortlet)

    label = _(u"portlet_related-resources_edit_title",
              default = u"Edit related resources portlet")
    description = _(u"portlet_related-resources_edit_desc",
                    default = u"A portlet which displays related resources")
    
    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        
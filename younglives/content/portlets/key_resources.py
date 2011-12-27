""" A portlet which shows context key resources. """


# Zope
from Acquisition import aq_inner
from zope import schema
from zope.formlib import form
from zope.interface import implements

# Plone
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local
from younglives.content import _

class IKeyResourcesPortlet(IPortletDataProvider):
    """ A portlet which shows context key resources. """
    
    header = schema.TextLine(title = _(u"Portlet header"),
                             description = _(u"Title of the portlet"),
                             required = 1,
                             default = u"Key resources")


class Assignment(base.Assignment):
    
    implements(IKeyResourcesPortlet)
    
    header = u"Key resources"
    
    def __init__(self, header=u"Key resources"):
        super(Assignment, self).__init__()
        self.header = header

    @property
    def raw_title(self):
        return u"Key resources"
    
    @property
    def title(self):
        return self.header


class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('key_resources.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        self.title = self.data.title
        self.data = self._data()

    @property
    def available(self):
        return self._data() is not None and len(self._data())
    
    @memoize
    def title(self):
        return self.title

    @memoize
    def _data(self):
        return self.context.computeRelatedItems()


class AddForm(base.AddForm):
    """ Portlet add form. """
    
    form_fields = form.Fields(IKeyResourcesPortlet)

    label = _(u"portlet_key-resources_add_title",
              default = u"Add key resources portlet")
    description = _(u"portlet_key-resources_add_desc",
                    default = u"A portlet which displays key resources")

    def create(self, data):
        return Assignment(**data)
    
    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
    
    
class EditForm(base.EditForm):
    """ Portlet edit form. """

    form_fields = form.Fields(IKeyResourcesPortlet)

    label = _(u"portlet_key-resources_edit_title",
              default = u"Edit key resources portlet")
    description = _(u"portlet_key-resources_edit_desc",
                    default = u"A portlet which displays key resources")
    
    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
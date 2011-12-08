""" General settings configlet for main site and subsites. """


# Zope
from zope.component import getUtility

# Plone
from z3c.form import button
from plone.z3cform.textlines import TextLinesFieldWidget
from plone.app.registry.browser.controlpanel import RegistryEditForm as \
    PloneRegistryEditForm
from plone.app.z3cform.layout import FormWrapper, wrap_form
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local
from younglives.content.interfaces import IYoungLivesSettings
  
  
# inherited RegistryEditForm to change redirections
class RegistryEditForm(PloneRegistryEditForm):
    schema = None
    label = u"Site settings"
    
    def update(self):
        self.schema = IYoungLivesSettings
        super(RegistryEditForm, self).update()
        
    def updateFields(self):
        super(RegistryEditForm, self).updateFields()

    def updateWidgets(self):
        super(RegistryEditForm, self).updateWidgets()
        
    @button.buttonAndHandler(u'Save', name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        self.status = u"Changes saved"

    @button.buttonAndHandler(u'Cancel', name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(u"Edit cancelled", "info")
        self.request.response.redirect(self.context.absolute_url())
  
    
# overwritten to disable view actions
class RegistryEditFormWrapper(FormWrapper):
    index = ViewPageTemplateFile('sitesettings.pt')
    def __init__(self, context, request):
         super(RegistryEditFormWrapper, self).__init__(context, request)
         self.request.set('disable_border', 1)


SiteSettings = wrap_form(RegistryEditForm,
                         __wrapper_class=RegistryEditFormWrapper)
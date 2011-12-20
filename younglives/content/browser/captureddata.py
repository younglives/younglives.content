""" Captures data from popup displays before file downloading. """


# Python
import time
import string, logging

# Zope
from DateTime import DateTime
from zope import schema
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

# Plone
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

# local
from younglives.policy import _
from younglives.content.config import *
from younglives.content.interfaces import ICapturedData, ICapturedDataStorage


logger = logging.getLogger('younglives.datacapture')

class CapturedDataForm(form.Form):
    template = ViewPageTemplateFile('captureddata_form.pt')
    label = _(u'Please give us some details.')
    formErrorsMessage = _('There were some errors.')
    fields = field.Fields(ICapturedData)
    errors = {}
    uid = None
    ignoreContext = True
  
    
    def __init__(self, context, request):
        super(CapturedDataForm, self).__init__(context, request)
        self.uid = self.request.form.has_key('uid') and self.request.form['uid']


    @button.buttonAndHandler(_('Add'), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
           self.status = self.formErrorsMessage
           return
        self.addData(data)
        self.request.response.redirect(self.nextURL())
            

    @button.buttonAndHandler(_('Skip'), name='skip')
    def handleCancel(self, action):
        self.setCookie(0)
        self.request.response.redirect(self.nextURL())


    def nextURL(self):
        if self.uid:
            logger.info(self.uid)
            catalog = getToolByName(self.context, 'portal_catalog')
            next_brain = catalog(UID=self.uid)
            if next_brain:
                return next_brain[0].getURL()
        portal_state = getMultiAdapter((self.context, self.request), 
                                       name=u'plone_portal_state')
        return portal_state.portal_url()
    
    
    def addData(self, data):
        captured_storage = ICapturedDataStorage(self.context)
        data['id'] = repr(time.time()) #to string
        captured_storage.add(data)
        self.setCookie(1)


    def setCookie(self, value):
        expires = (DateTime()+365*2).toZone('GMT').rfc822()
        self.request.response.setCookie(CAPTURE_DATA_COOKIE_NAME, 
                                        value, 
                                        expires=expires)
        

CapturedDataView = wrap_form(CapturedDataForm)
        
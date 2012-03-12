""" Default browser view for Publication item. """


# Python
import re

# Zope
from zope.interface import implements
from zope.component import getMultiAdapter

# Plone
from Products.ATContentTypes.interfaces import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.memoize import view

# local
from younglives.content.config import *
from younglives.content.interfaces import IPublicationView 

MIME_TYPES= [
        {'title':'Word document',
         'regex':('.*officedocument.word',)},
        {'title':'Excel spreadsheet',
         'regex':('.*officedocument.spreadsheet',)},
        {'title':'PowerPoint presentation',
         'regex':('.*officedocument.presentation',)},
    ]

class PublicationView(BrowserView):
    implements(IPublicationView)
    
    @view.memoize
    def files(self):
        results = []
        files = self.context.getFiles()
        ltool = getToolByName(self.context, 'portal_languages')
        for file in files:
            css = self._show_capture_popup() and 'capturePopup'
            lang = file.Language() or 'en'
            type_field = file.getField('documentType')
            type = type_field and type_field.get(file)
            results.append(dict(title = file.Title(),
                                size = '%s KB' % (file.get_size() / 1024),
                                url = self._get_file_url(file),
                                css = css or '',
                                type = (type and type[0]) or 'file',
                                language = ltool.getNameForLanguageCode(lang),
                                content_type = self._get_file_mimetype(file)))
            
        return results
    
    
    def _get_file_mimetype(self, file):
        mimetype = self.context.lookupMime(file.getContentType())
        for MIME_TYPE in MIME_TYPES:
            regexs = MIME_TYPE['regex']
            for regex in regexs:
                if re.search(regex,mimetype):
                    mimetype = MIME_TYPE['title']
                    break
        return mimetype


    def _get_file_url(self, file):
        if self._show_capture_popup():
            portal= getMultiAdapter((self.context, self.request), 
                                    name=u'plone_portal_state')
            return "%s/capturePopup?uid=%s" % (portal.portal_url(), 
                                               self.context.UID())
        return file.absolute_url()
    
    
    def _show_capture_popup(self):
        pm = getToolByName(self.context, 'portal_membership')
        if pm.isAnonymousUser() and \
            not self.request.cookies.get(CAPTURE_DATA_COOKIE_NAME):
            return 1
        return 0

from Acquisition import aq_parent
from plone.memoize import view
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class DocumentView(BrowserView):

    @view.memoize
    def banner(self):
        ptool = getToolByName(self.context, 'plone_utils')
        parent = getattr(self.context, '__parent__', aq_parent(self.context))
        if ptool.isDefaultPage(self.context):
            try:
                banner_field = parent.getField("bannerImage")
            except AttributeError:
                return None
            if banner_field:
                return banner_field.get(parent)
        return None

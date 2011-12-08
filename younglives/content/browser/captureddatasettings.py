""" Captured data console """ 


# Python
import string, logging

# Zope
from DateTime.DateTime import *
from zope.component import getMultiAdapter

# Plone
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import view

# local
from younglives.content.interfaces import ICapturedDataStorage


logger = logging.getLogger('younglives.captureddatasettings')

class CapturedDataSettingsView(BrowserView):
    
    error_status = None
    info_status = None

    
    def __call__(self):
        
        records = self.request.get("records")
            
        if self.request.has_key("remove") and records:
            self.remove_records(records)
            
        return super(CapturedDataSettingsView, self).__call__()
    
    
    def records(self):
        storage = ICapturedDataStorage(self.context)
        records = storage.captured()
        year = self.request.get('year')
        logger.info(year)
        if not year: 
            year = self.curr_year()
        month = self.request.get('month')
        if not month: 
            month = self.curr_month()
        records = self.filter_data(records, int(year), int(month))
        return sorted(records,reverse=True)
    
    
    def remove_records(self, records):
        storage = ICapturedDataStorage(self.context)
        for record in records:
            storage.remove(record)
            
            
    def filter_data(self, records, year, month):
        results = []
        for id in records:
            date = DateTime(float(id))
            if date.year() == year and date.month() == month:
                results.append(records[id])
        return results
    
    
    def curr_month(self):
        return DateTime().month()
    
    
    def curr_year(self):
        return DateTime().year()
            
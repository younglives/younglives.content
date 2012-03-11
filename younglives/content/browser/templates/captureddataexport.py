""" Export captured data to CVS file. """


#Python
from time import strftime

# Zope
from DateTime.DateTime import *
from zope.schema import getFieldNamesInOrder

# Plone
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

# local
from younglives.policy import _
from younglives.content.interfaces.adapters import ICapturedDataStorage
from younglives.content.interfaces.captureddata import ICapturedData

class CapturedDataExportView(BrowserView):

    def __call__(self):
        """ Exports users to CSV file. """
        
        text = ''
        self.field_names = getFieldNamesInOrder(ICapturedData)
    
        properties = []
        properties.append('date')
        for name in self.field_names:
            properties.append(name)
        
        for p in properties:
            text += p + ','
            
        #remove trailing comma
        text=text[:-1]
        text += chr(13)+chr(10) #first line has been written
        text += self.records()
        
        filename = 'captured_dta_%s.csv' % strftime("%Y%m%d")
        self.context.REQUEST.response.setHeader("Content-type", "text/csv")
        self.request.response.setHeader('Content-Disposition', 'attachment; \
filename="%s"' % filename)
        
        return text
    
    def records(self):
        storage = ICapturedDataStorage(self.context)
        year = self.request.get('year')
        if not year: 
            year = self.curr_year()
        month = self.request.get('month')
        if not month: 
            month = self.curr_month()
        records = self.filter_data(storage.captured(), int(year), int(month))
        text = ''
        for record in records:
            text+='%s,' % DateTime(float(record['id'])).strftime('%m/%d/%Y %H:%M')
            for name in self.field_names:
                text+='%s,' % record[name]
            text=text[:-1]
            text+='\n'
        return text
    
    
    def filter_data(self, records, year, month):
        results = []
        for id in records:
            date = DateTime(float(id))
            if date.year() == year and date.month() == month:
                results.append(records[id])
        return results
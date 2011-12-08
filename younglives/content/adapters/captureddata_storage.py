""" Storage for datacaptured in pop-ups displayed before file downloading. """


# Zope
from zope.interface import implements
from BTrees.OOBTree import OOBTree
from zope.annotation.interfaces import IAnnotations

# local
from younglives.content.interfaces import ICapturedDataStorage


ANN_KEY = "younglives_captured_storage"

class CapturedDataStorage(object):
    implements(ICapturedDataStorage)
    
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.data = annotations.setdefault(ANN_KEY, OOBTree())

    def add(self, data):
        if self.data.has_key(data['id']):
           return False
        self.data[data['id']] = data
        return True
        
    def remove(self, id):
        if self.data.has_key(id):
            del self.data[id]
            
    def get(self, user_id):
        if self.data.has_key(id):
            return self.data[id]
        return None
        
    def captured(self):
        return dict(self.data)
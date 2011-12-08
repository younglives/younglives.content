""" Temporary storage for users waiting for approvement """


# Zope
from zope.interface import implements
from BTrees.OOBTree import OOBTree
from zope.annotation.interfaces import IAnnotations

# local
from younglives.content.interfaces import IUserStorage


ANN_KEY = "younglives_user_storage"

class UserStorage(object):
    implements(IUserStorage)
    
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.data = annotations.setdefault(ANN_KEY, OOBTree())

    def add(self, user):
        if self.data.has_key(user['email']):
           return False
        self.data[user['email']] = user
        return True
        
    def remove(self, user_id):
        if self.data.has_key(user_id):
            del self.data[user_id]
            
    def get(self, user_id):
        if self.data.has_key(user_id):
            return self.data[user_id]
        return None
        
    def users(self):
        return dict(self.data)
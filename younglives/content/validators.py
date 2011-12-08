""" Custom validators for content types fields. """


# Python
from PIL import Image
from types import ListType, TupleType

# Zope
from zope.interface import implements

# Plone
from Products.validation.interfaces.IValidator import IValidator

# local
from younglives.policy.i18n import younglivesMessageFactory as _


def validateImageSize(imageWidth, imageHeight, validSizes):
    """ Validate images size and return boolean value.
    
    Keyword arguments:
    imageWidth -- image width
    imageHeight -- image height
    validSizes -- tuple/list of valid image sizes
        If multiple sizes are given image size has to fit at least one of them.
        Valid sizes dimensions can be both numeric or string values 
        (in this case they must be the whole comparision expression) 
    
    validSizes examples:
    - numeric values: (100,200)
    - string values: ('==100','<300>200')
    - mixed values: ('==100',200)
    - multiple mixed values: (('==100','==200'),(100,200))
    """
    
    ListTypes = (ListType, TupleType)
    
    def _validate(isize, vsize):
        res = False
        for x in range(0,len(vsize)):
            if isinstance(vsize[x], basestring):
                res = eval(str(isize[x])+vsize[x])
            else:
                res = isize[x] == vsize[x]
            if not res: return res
        return True
    
    # only a few simple checkings
    if not validSizes:
        raise ValueError('validSizes cannot be empty')
    if not isinstance(validSizes, ListTypes):
        raise ValueError('validSizes must be tuple or list')
    
    if isinstance(validSizes[0], ListTypes):
        for vsize in validSizes:
            if _validate((imageWidth, imageHeight), vsize):
                return True
    else:
        return _validate((imageWidth, imageHeight), validSizes)
    
    return False
    

class ImageSizeValidator:
    """ Exact image size validator for archetypes ImageField. """
    
    implements(IValidator)
    
    err_msg = _("Validation failed - image size is invalid.")

    def __init__(self, name, title='', description='', validsizes=(0,0)):
        self.name = name
        self.title = title or name
        self.description = description
        self.validsizes = validsizes
        
    def __call__(self, value, *args, **kwargs):
        field    = kwargs.get('field')
        
        if not value:
            return True # nothing to validate
        
        if kwargs.has_key('validsizes'):
            validsizes = kwargs.get('validsizes')
        elif hasattr(field, 'validsizes'):
            validsizes = field.validsizes
        else:
            # set to given default value
            validsizes = self.validsizes
            
        try:
            value.seek(0) # rewind
            image = Image.open(value)
            w = image.size[0]
            h = image.size[1]
            if not validateImageSize(w, h, validsizes):
                return self.err_msg
        except:
            # hmm, what am'I suppose to do here?
            pass
        
        return True
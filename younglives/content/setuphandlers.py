""" Generic setup profiles setuphandlers. """


# Python
import string, logging

# Plone
from Products.CMFCore.utils import getToolByName


INDEXES = {'exclude_from_nav' : 'FieldIndex',
           'theme' : 'KeywordIndex',
           'topic' : 'KeywordIndex',
           'publication_date' : 'FieldIndex'}
METADATA = ['theme','topic']

logger = logging.getLogger('younglives.content-setup')


def defaultSteps(context):
    if not context.readDataFile('younglives.content-default.txt'):
        return

    site = context.getSite()
    
    fixSkinLayers(site)
    changeHTMLFiltering(site)
    setupCatalog(site)
            
            
def fixSkinLayers(portal):
    skinsTool = getToolByName(portal, 'portal_skins')
    path = skinsTool.getSkinPath('Sunburst Theme')
    path = map(string.strip, string.split(path,','))  # list of skin layers
    new_list = []
    idx = 1
    for layer in path:
        if layer.startswith('younglives-'):
            # insert layer after custom
            new_list.insert(new_list.index('custom')+idx, layer)
            idx += 1
            logger.info("fixSkinLayers: inserts %s" % layer)
        else:
            new_list.append(layer)
    path = string.join(new_list, ', ')
    skinsTool.addSkinSelection('Plone Default', path)
  
    
def changeHTMLFiltering(portal):
    pt = getToolByName(portal,'portal_transforms')
    safe_html = pt['safe_html']
    
    toAllow = ('embed', 'object', 'param', 'iframe') 
    for tag in toAllow: 
        safe_html._config['valid_tags'][tag] = 1 
        try: 
            del safe_html._config['nasty_tags'][tag] 
        except KeyError: 
            pass 
        try: 
            del safe_html._config['stripped_tags'][tag] 
        except KeyError: 
            pass 

    safe_html._p_changed = True
    logger.info("changeHTMLFiltering: adds embed, object, param to valid tags %s" %
                "listed in safe_html tranformation")
    

def setupCatalog(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    idxs = catalog.indexes()
    mtds = catalog.schema()

    indexables = []
    for index in INDEXES.keys():
        if index not in idxs:
            catalog.addIndex(index, INDEXES[index])
            indexables.append(index)
            logger.info("setupCatalog: added '%s' index" % index)
            
    if len(indexables) > 0:
        logger.info("setupCatalog: indexing new indexes [%s]" % 
                    ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)

    for mt in METADATA:
        if mt not in mtds:
            catalog.addColumn(mt)
            logger.info("setupCatalog: added '%s' column" % mt)
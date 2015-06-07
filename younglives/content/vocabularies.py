from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements

from younglives.content import _


EVENTS = "Event"
NEWS = "News Item"
PUBLICATIONS = "YLPublication"
ARTICLE = "Document"


# =============================================================================
# Latest items portlet
# =============================================================================

ALLOWED_TYPES_FOR_LATEST_ITEMS_PORTLET = (
    SimpleTerm(EVENTS, EVENTS, _(u'Latest events')),
    SimpleTerm(NEWS, NEWS, _(u'Latest news')),
    SimpleTerm(PUBLICATIONS, PUBLICATIONS, _(u'Latest publications')),
    SimpleTerm(ARTICLE, ARTICLE, _(u"Latest articles")),
)


class LatestItemsAvailableTypes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(terms=ALLOWED_TYPES_FOR_LATEST_ITEMS_PORTLET)


# =============================================================================
# Related resources portlets
# =============================================================================

ALLOWED_TYPES_FOR_RELATED_RESOURCES_PORTLET = (
    SimpleTerm(EVENTS, EVENTS, _(u'Events')),
    SimpleTerm(NEWS, NEWS, _(u'News')),
    SimpleTerm(PUBLICATIONS, PUBLICATIONS, _(u'Publications')),
)


class RelatedResourcesAvailableTypes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(
            terms=ALLOWED_TYPES_FOR_RELATED_RESOURCES_PORTLET)


SORT_INDEXES_FOR_RELATED_RESOURCES_PORTLET = (
    SimpleTerm('Date', 'Date', _(u'Latest first')),
)


class RelatedResourcesSortIndexes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(
            terms=SORT_INDEXES_FOR_RELATED_RESOURCES_PORTLET)


def ploneCategoriesVocabulary(context):
    ctool = getToolByName(context, 'portal_catalog')
    items = ctool.uniqueValuesFor('Subject')
    return SimpleVocabulary.fromValues(items)

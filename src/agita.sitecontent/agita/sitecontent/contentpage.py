from Acquisition import aq_inner
from five import grok
from plone import api

from plone.indexer import indexer
from plone.dexterity.content import Container
from plone.app.textfield import RichText

from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable

from ade25.panelpage import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    A modular ppage with panel layout
    """
    toc = RichText(
        title=_(u"Table of contents"),
        description=_(u"Please enter hero quicklinks here"),
        required=False,
    )


@indexer(IContentPage)
def childNodeIndexer(obj):
    searchable_text = obj.SearchableText()
    for item in obj.getFolderContents(
        {'portal_type': 'ade25.panelpage.panel'},
    ):
        searchable_text += item.SearchableText()
    return searchable_text
grok.global_adapter(childNodeIndexer, name="SearchableText")


class ContentPage(Container):
    grok.implements(IContentPage)
    pass


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_images = len(self.lead_images()) > 0

    def lead_images(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(portal_type=['Image'],
                        path=dict(query='/'.join(context.getPhysicalPath()),
                                  depth=1),
                        limit=3)[:3]
        return items

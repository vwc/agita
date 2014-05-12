from five import grok

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

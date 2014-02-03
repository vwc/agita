from zope import schema
from zope.interface import Interface

from vwcollective.simplecontact import simplecontactMessageFactory as _

class IPreviewTagProvider(Interface):
    """A component which can provide an HTML tag for a preview image
    """

    tag = schema.TextLine(title=_(u"A HTML tag to render to show the banner image"))
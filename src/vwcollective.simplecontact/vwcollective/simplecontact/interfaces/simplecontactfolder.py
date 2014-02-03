from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from vwcollective.simplecontact import simplecontactMessageFactory as _

class ISimpleContactFolder(Interface):
    """A Folder holding SimpleContact information"""
    
    # -*- schema definition goes here -*-
    image = schema.Bytes(
        title=_(u"Preview Image"), 
        required=False,
        description=_(u"Upload a preview image that will be shown in content listings"),
    )


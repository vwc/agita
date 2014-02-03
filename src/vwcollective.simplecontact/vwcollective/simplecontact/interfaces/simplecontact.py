from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from vwcollective.simplecontact import simplecontactMessageFactory as _

class ISimpleContact(Interface):
    """A simple type holding contact information"""
    
    # -*- schema definition goes here -*-

    profession = schema.TextLine(
        title=_(u"Profession"), 
        required=False,
        description=_(u"Enter profession or accademic title"),
    )

    position = schema.TextLine(
        title=_(u"Position"), 
        required=False,
        description=_(u"Enter position in the company"),
    )

    vita = schema.Bytes(
        title=_(u"Curriculum vitae"), 
        required=False,
        description=_(u"Upload vita as pdf"),
    )

    image = schema.Bytes(
        title=_(u"Portait"), 
        required=False,
        description=_(u"Upload a portrait image that will be displayed in overview pages and listings"),
    )

    email = schema.TextLine(
        title=_(u"Email"), 
        required=False,
        description=_(u"Enter a valid email address."),
    )

    phone = schema.TextLine(
        title=_(u"Phone"), 
        required=False,
        description=_(u"Field description"),
    )




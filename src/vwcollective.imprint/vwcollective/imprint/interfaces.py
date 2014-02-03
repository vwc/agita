from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from vwcollective.imprint import imprintMessageFactory as _

# -*- extra stuff goes here -*-

class IImprint(Interface):
    """Imprint content type"""
    
    title = schema.TextLine(title=_(u"Title"),
                            required=True)
    
    description = schema.TextLine(title=_(u"Description"),
                                  required=False)
    
    company = schema.TextLine(title=_("Company"),
                              description=_("The company name will be inserted in the disclaimers."),
                              required=True)
    
    street = schema.TextLine(title=_("Street"),
                             required=True)
    
    city = schema.TextLine(title=_(u"City"),
                            required=True)
    
    phone = schema.TextLine(title=_(u"Phone"))
    
    fax = schema.TextLine(title=_(u"Fax"))
    
    email = schema.TextLine(title=_(u"Email"),
                            description=_(u"Enter a valid email address. The email address will automatically be spam protected."),
                            required=True)
    
    web = schema.TextLine(title=_(u"Web"))
    
    jurisdiction = schema.TextLine(title=_(u"Jurisdiction"),
                                    description=_(u"The legal venue responsible for this company."))
    
    commercial_register = schema.TextLine(title=_(u"Commercial Register Number"),
                                    description=_(u"Optional commercial register number, if available."))
    
    tax_id = schema.TextLine(title=_(u"Value Added Tax Identification Number"))
    
    head_office = schema.TextLine(title=_(u"Head Office"),
                                 description=_(u"Enter potentially necessary registered office or company headquarter."))
    
    responsible_person = schema.TextLine(title=_(u"Responsible Person"),
                                description=_(u"Enter the names of the responsible individuals or executive directors."))

   

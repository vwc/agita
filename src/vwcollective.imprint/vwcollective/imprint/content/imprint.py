"""Definition of the Imprint content type
"""

from zope.interface import implements, directlyProvides
from zope.component import adapts

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.CMFCore.utils import getToolByName

from vwcollective.imprint import imprintMessageFactory as _
from vwcollective.imprint.interfaces import IImprint
from vwcollective.imprint.config import PROJECTNAME

ImprintSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField(
        name='company',
        widget=atapi.StringWidget(
            label=_(u"Company"),
            description=_(u"The company name will be inserted in the disclaimers."),
        ),
        required=True,
    ),
    
    atapi.StringField(
        name='street',
        widget=atapi.StringWidget(
            label=_(u"Street"),
        ),
        required=True,
    ),
    
    atapi.StringField(
        name='city',
        widget=atapi.StringWidget(
            label=_(u"City"),
        ),
        required=True,
    ),
    
    atapi.StringField(
        name='phone',
        widget=atapi.StringWidget(
            label=_(u"Phone"),
        ),
        required=True,
        validators=('isInternationalPhoneNumber',),
    ),
    
    atapi.StringField(
        name='fax',
        widget=atapi.StringWidget(
            label=_(u"Fax"),
        ),
    ),
    
    atapi.StringField(
        name='email',
        widget=atapi.StringWidget(
            label=_(u"Email"),
            description=_(u"Enter a valid email address. The email address will automatically be spam protected."),
        ),
        required=True,
        validators=('isEmail',),
    ),
    
    atapi.StringField(
        name='web',
        widget=atapi.StringWidget(
            label=_(u"Web"),
        ),
        required=True,
        validators=('isURL',),
    ),
    
    atapi.StringField(
        name='jurisdiction',
        widget=atapi.StringWidget(
            label=_(u"Jurisdiction"),
            description=_(u"The legal venue responsible for this company.")
        ),
    ),
    
    atapi.StringField(
        name='commercialRegister',
        widget=atapi.StringWidget(
            label=_(u"Commercial Register Number"),
            description=_(u"Optional commercial register number, if available."),
        ),
    ),
    
    atapi.StringField(
        name='taxId',
        widget=atapi.StringWidget(
            label=_(u"Value Added Tax Identification Number"),
        ),
    ),
    
   atapi.StringField(
       name='headquarter',
       widget=atapi.StringWidget(
           label=_(u"Head Office"),
           description=_(u"Enter potentially necessary registered office or company headquarter."),
       ),
   ),
   
    atapi.StringField(
       name='responsiblePerson',
       widget=atapi.StringWidget(
           label=_(u"Responsible Person"),
           description=_(u"Enter the names of the responsible individuals or executive directors."),
       ),
   ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ImprintSchema['title'].storage = atapi.AnnotationStorage()
ImprintSchema['description'].storage = atapi.AnnotationStorage()
ImprintSchema['company'].storage = atapi.AnnotationStorage()
ImprintSchema['street'].storage = atapi.AnnotationStorage()
ImprintSchema['city'].storage = atapi.AnnotationStorage()
ImprintSchema['phone'].storage = atapi.AnnotationStorage()
ImprintSchema['fax'].storage = atapi.AnnotationStorage()
ImprintSchema['email'].storage = atapi.AnnotationStorage()
ImprintSchema['web'].storage = atapi.AnnotationStorage()
ImprintSchema['jurisdiction'].storage = atapi.AnnotationStorage()
ImprintSchema['commercialRegister'].storage = atapi.AnnotationStorage()
ImprintSchema['taxId'].storage = atapi.AnnotationStorage()
ImprintSchema['headquarter'].storage = atapi.AnnotationStorage()
ImprintSchema['responsiblePerson'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ImprintSchema, moveDiscussion=False)

class Imprint(base.ATCTContent):
    """Imprint content type"""
    implements(IImprint)

    portal_type = "Imprint"
    schema = ImprintSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    company = atapi.ATFieldProperty('company')
    street = atapi.ATFieldProperty('street')
    city = atapi.ATFieldProperty('city')
    phone = atapi.ATFieldProperty('phone')
    fax = atapi.ATFieldProperty('fax')
    email = atapi.ATFieldProperty('email')
    web = atapi.ATFieldProperty('web')
    jurisdiction = atapi.ATFieldProperty('jurisdiction')
    commercial_register = atapi.ATFieldProperty('commercialRegister')
    tax_id = atapi.ATFieldProperty('taxId')
    head_office = atapi.ATFieldProperty('headquarter')
    responsible_person = atapi.ATFieldProperty('responsiblePerson')

atapi.registerType(Imprint, PROJECTNAME)

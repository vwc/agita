"""Definition of the SimpleContact content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from vwcollective.simplecontact import simplecontactMessageFactory as _
from vwcollective.simplecontact.interfaces import ISimpleContact
from vwcollective.simplecontact.config import PROJECTNAME

SimpleContactSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'profession',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Profession"),
            description=_(u"Enter profession or accademic title"),
        ),
    ),


    atapi.StringField(
        'position',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Position"),
            description=_(u"Enter position in the company"),
        ),
    ),


    atapi.FileField(
        'vita',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Curriculum vitae"),
            description=_(u"Upload vita as pdf"),
        ),
        validators=('isNonEmptyFile'),
    ),


    atapi.ImageField(
        'image',
        storage=atapi.AnnotationStorage(),
		swallowResizeExceptions=True,
		max_size='no',
		sizes={'large'	: (768, 768),
			   'preview': (400, 400),
			   'mini'	: (200, 200),
			   'thumb'	: (128, 128),
			   'tile'	: (64, 64),
			   'icon'	: (32, 32),
			   'listing': (16, 16),
			   },
        widget=atapi.ImageWidget(
            label=_(u"Portait"),
            description=_(u"Upload a portrait image that will be displayed in overview pages and listings"),
        ),
        validators=('isNonEmptyFile'),
    ),


    atapi.StringField(
        'email',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Email"),
            description=_(u"Enter a valid email address."),
        ),
        validators=('isEmail'),
    ),


    atapi.StringField(
        'phone',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Phone"),
            description=_(u"Field description"),
        ),
    ),





))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SimpleContactSchema['title'].storage = atapi.AnnotationStorage()
SimpleContactSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SimpleContactSchema, moveDiscussion=False)

class SimpleContact(base.ATCTContent):
    """A simple type holding contact information"""
    implements(ISimpleContact)

    meta_type = "SimpleContact"
    schema = SimpleContactSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    vita = atapi.ATFieldProperty('vita')

    image = atapi.ATFieldProperty('image')

    email = atapi.ATFieldProperty('email')

    phone = atapi.ATFieldProperty('phone')

    position = atapi.ATFieldProperty('position')

    profession = atapi.ATFieldProperty('profession')
    
    def tag(self, **kargs):
        """Generate image tag"""
        return self.getField('image').tag(self, **kargs)
    
    def __bobo_traverse__(self, REQUEST, name):
        """Make image scales accessible and return the appropriate image content"""
        if name.startswith('image'):
            field = selg.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        return super(SimpleContact, self).__bobo_traverse__(REQUEST, name)


atapi.registerType(SimpleContact, PROJECTNAME)

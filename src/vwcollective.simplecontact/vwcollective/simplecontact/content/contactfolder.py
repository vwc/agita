"""Definition of the ContactFolder content type
"""

from zope.interface import implements, directlyProvides
from zope.component import adapts

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from vwcollective.simplecontact import simplecontactMessageFactory as _
from vwcollective.simplecontact.interfaces import IContactFolder
from vwcollective.simplecontact.interfaces import IPreviewTagProvider
from vwcollective.simplecontact.config import PROJECTNAME

ContactFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
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
            label=_(u"Preview Image"),
            description=_(u"Upload a preview image that will be shown in content listings"),
        ),
        validators=('isNonEmptyFile'),
    ),
    
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ContactFolderSchema['title'].storage = atapi.AnnotationStorage()
ContactFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ContactFolderSchema,
    folderish=True,
    moveDiscussion=False
)

class ContactFolder(folder.ATFolder):
    """A folder holding contact information"""
    implements(IContactFolder)

    meta_type = "ContactFolder"
    schema = ContactFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    image = atapi.ATFieldProperty('image')

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)

    def __bobo_traverse__(self, REQUEST, name):
        """Give transparent access to image scales. This hooks into the
        low-level traversal machinery, checking to see if we are trying to
        traverse to /path/to/object/image_<scalename>, and if so, returns
        the appropriate image content.
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image

        return super(ContactFolder, self).__bobo_traverse__(REQUEST, name)

atapi.registerType(ContactFolder, PROJECTNAME)

# This simple adapter uses Archetypes' ImageField to extract an HTML tag
# for the banner image. This is used in the portlets to avoid
# having a hard dependency on the AT ImageField implementation.

# Note that we adapt a class, not an interface. This means that we will only
# match adapter lookups for this class (or a subclass), which is correct in
# this case, because we are relying on internal implementation details.

class PreviewTagProvider(object):
    implements(IPreviewTagProvider)
    adapts(ContactFolder)

    def __init__(self, context):
        self.context = context

    @property
    def tag(self):
        return self.context.getField('image').tag(self.context, scale='tile')




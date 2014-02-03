from Acquisition import aq_base, aq_inner, aq_parent
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.portlets.portlets import base

from zope.formlib import form

from z3c.relationfield.schema import RelationChoice

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.blob.interfaces import IATBlobImage
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.CMFDynamicViewFTI.interface import IBrowserDefault

from agita.portlet.gallery import AgitaGalleryPortletMessageFactory as _


class IAgitaGalleryPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    gallery = RelationChoice(title=_(u"Gallery Source"),
                            description=_(u"Please select the target folder where the images for this gallery reside."),
                            source=SearchableTextSourceBinder({'is_folderish': True},
                                                              default_query='path:'),
                            required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IAgitaGalleryPortlet)
    
    gallery = None
    
    def __init__(self, gallery=None):
       self.gallery = gallery

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Agita Gallery Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('agitagalleryportlet.pt')
    
    def gallery_images(self):
        """Get the gallery images form the target folder"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        urltool = getToolByName(context, 'portal_url')
        selection = self.data.gallery
        portal_path = urltool.getPortalPath()
        target_path = portal_path + selection
        images = catalog(object_provides=IATBlobImage.__identifier__,
                         path=dict(query=target_path, depth=1),)
        return images


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IAgitaGalleryPortlet)
    form_fields['gallery'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IAgitaGalleryPortlet)

def getRootPath(context, root):
    """Helper function to calculate the real root path
    """
    context = aq_inner(context)

    rootPath = getNavigationRoot(context, relativeRoot=root)
    contextPath = '/'.join(context.getPhysicalPath())
    import pdb; pdb.set_trace( )
    if not contextPath.startswith(rootPath):
        return None
    contextSubPathElements = contextPath[len(rootPath)+1:]
    if contextSubPathElements:
        contextSubPathElements = contextSubPathElements.split('/')
        rootPath = rootPath + '/' + '/'.join(contextSubPathElements)
    else:
        return None

    return rootPath

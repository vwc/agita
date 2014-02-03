from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

from Acquisition import aq_parent, aq_inner, aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from vwcollective.simplecontact.interfaces import IPreviewTagProvider
from vwcollective.simplecontact import simplecontactMessageFactory as _

class IContactsPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    name = schema.TextLine (title=_(u"Title"),
                            description=_(u"The title of the selection portlet."),
                            default=u"",
                            required=True)
    
    root = schema.Choice(title=_(u"Selection"),
                         description=_(u"You may search for and choose a folder "
                                        "to act as the root of the selection."),
                         required=True,
                         source=SearchableTextSourceBinder({'is_folderish' : True},
                                                            default_query='path:'))


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IContactsPortlet)

    title = _(u'Contacts Portlet')
    name = u""
    root = None

    def __init__(self, name=u"", root=None):
        self.name = name
        self.root = root


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('contactsportlet.pt')

    def Title(self):
        return self.data.name
    
    def has_contactfolders(self):
        return len(self.contactfolders()) > 0
    
    def root_data(self):
        return self.data.root
    
    def selection_root(self):
        return self.getSelectionRoot()
    
    def selection_root_url(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url')
        selection_path = self.data.root
        root_url = portal.getPortalPath() + selection_path
        return root_url
    
    def contactfolders(self):
        """Contact Folders in the selected section of the site"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal = getToolByName(context, 'portal_url')
        pathfilter = self.data.root
        path = portal.getPortalPath() + pathfilter
        portaltypes = 'ContactFolder'
        wfstate = 'published'
        query = {}
        query['path'] = path
        query['portal_type'] = portaltypes
        query['review_state'] = wfstate
        results = [dict(url=cf.getURL(),
                        title=cf.Title,
                        preview_tag=IPreviewTagProvider(cf.getObject()).tag,
                        )
                    for cf in catalog.searchResults(query)
                    ]
        
        folders = list(results)
        #folders.sort(lambda x,y: cmp(random.randint(0,200),100))
        folders = folders[:3]
        return folders

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(IContactsPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Add Contacts Portlet")
    description = _(u"This portlet displays contact folders from a selected section.")

    def create(self, data):
        return Assignment(name=data.get('name', u""),
                          root=data.get('root', u""))


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IContactsPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Edit Contacts Portlet")
    description = _(u"This portlet displays contact folders from a selected section.")

def getRootPath(context, root):
    """helper function to get the root path"""
    context = aq_inner(context)
    rootPath = getNavigationRoot(context, relativeRoot=root)
    return rootPath

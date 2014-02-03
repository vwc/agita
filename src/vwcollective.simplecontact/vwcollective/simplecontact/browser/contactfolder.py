from zope.interface import implements, Interface
from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from vwcollective.simplecontact.interfaces import ISimpleContactFolder
from vwcollective.simplecontact.interfaces import ISimpleContact
from vwcollective.simplecontact.interfaces import IPreviewTagProvider
from vwcollective.simplecontact import simplecontactMessageFactory as _


class ContactFolderView(BrowserView):
    """
    ContactFolder browser view
    """
    template = ViewPageTemplateFile('contactfolder.pt')

    def __call__(self):
        return self.template()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
    
    def has_subfolders(self):
        """Test if we have subfolders"""
        return len(self.contained_contactfolders()) > 0
    
    def contained_contactfolders(self):
        """Query the catalog for contained ContactFolders in order to decide
        wether to show a catagory preview or the simplecontacts directly"""
        context = aq_inner(self.context)
        return [dict(title=cf.Title,
                     description=cf.Description,
                     url=cf.getURL(),
                     preview_tag=IPreviewTagProvider(cf.getObject()).tag,
					 image=cf.getObject().image,
                    )
                for cf in self.portal_catalog(object_provides=ISimpleContactFolder.__identifier__,
                                              path=dict(query='/'.join(context.getPhysicalPath()),
                                                        depth=1),
                                              review_state='published',)
                    ]
    def contained_contacts(self):
        """List objects of type SimpleContact"""
        context = aq_inner(self.context)
        return [dict(title=c.Title,
                     url=c.getURL(),
                     profession=c.getObject().profession,
                     position=c.getObject().position,
                     email=c.getObject().email,
                     phone=c.getObject().phone,
                     image=c.getObject().image,
                     file=c.getObject().vita,
                    )
                for c in self.portal_catalog(object_provides=ISimpleContact.__identifier__,
                                            path=dict(query='/'.join(context.getPhysicalPath()),
                                                      depth=1),
                                            review_state='published',)
                ]


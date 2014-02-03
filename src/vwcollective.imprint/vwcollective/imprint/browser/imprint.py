from zope.interface import implements, Interface

from Acquisition import aq_inner, aq_parent, aq_base
from AccessControl import Unauthorized

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from vwcollective.imprint.interfaces import IImprint
from vwcollective.imprint import imprintMessageFactory as _


class ImprintView(BrowserView):
    """
    imprint browser view
    """
    template = ViewPageTemplateFile('imprint.pt')

    def __call__(self):
        return self.template()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

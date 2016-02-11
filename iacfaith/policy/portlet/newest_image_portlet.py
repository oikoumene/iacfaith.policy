from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from lxml.html import parse

#grok.templatedir('templates')

class INewestImagePortlet(IPortletDataProvider):
    
    site_url = schema.TextLine(
            title = u"URL to get the newest image"    
        )
    
class Assignment(base.Assignment):
    implements(INewestImagePortlet)
    
    def __init__(self,site_url=None):
        self.site_url = site_url
        
    title = u"Portlet for Newest Image"
    
class Renderer(base.Renderer):
    render = ViewPageTemplateFile('newest_image_portlet.pt')
    
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
        
    
    def results(self):
        data = {'img_src':'#', 'title':'', 'img_url':'#'}
        
        obj_url = parse(self.data.site_url).getroot()
        elem = obj_url.cssselect('div.ResourcePanelShell')
        if elem:
            
            elem1 = elem[0].cssselect('div.ResourcePanel')[0]
            curr_path = elem1.base_url.split('/')
            base_path = curr_path[0]+'//'+curr_path[2]
            data['img_src'] = elem1.cssselect('img')[0].attrib['src']
            data['title'] = elem1.cssselect('img')[0].attrib['alt']
            data['img_url'] = base_path+elem1.cssselect('a')[0].attrib['href']
        return data

class AddForm(base.AddForm):
    form_fields = form.Fields(INewestImagePortlet)
    label = u"Add Newest Image Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment
        
class EditForm(base.EditForm):
    form_fields = form.Fields(INewestImagePortlet)
    label = u"Edit Newest Image Portlet"
    description = ''
            
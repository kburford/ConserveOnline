from base import XMLViewBase
from Products.COL3.etree import Element, SubElement, tostring

class ResourceView(XMLViewBase):

    def elem(self):
        ctx = self.context
        resource = Element('resource', href=ctx.absolute_url())

        # Do not shadow builtin
        _type = SubElement(resource, 'type', title=ctx.title_or_id())
        _type.text=ctx.title_or_id()

        desc = SubElement(resource, 'description')
        desc.text=ctx.Description()
        logo = SubElement(resource, 'logo')
        meth = getattr(ctx, 'getLogo', None)
        if meth is not None:
            obj = meth()
            logo.attrib['src']=obj.absolute_url()
            logo.text = obj.title_or_id()
        loc = getattr(ctx, 'location', None)
        if loc is not None:
            loc.text = loc
        created = SubElement(resource, 'created')
        created.text = ctx.created().HTML4()
        modified = SubElement(resource, 'modified')
        modified.text = ctx.modified().HTML4()

        return resource

    def renderXML(self):
        return tostring(self.elem())

    tostring = renderXML

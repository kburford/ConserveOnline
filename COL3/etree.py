from elementtree.ElementTree import * #@UnusedWildImport
from elementtree.ElementTree import _ElementInterface as _BaseElement, __all__

from Products.COL3.config import CHARSET

def _to_unicode(text):
    if isinstance(text, str):
        text = unicode(text, CHARSET)
    return text

class _ElementInterface(_BaseElement):
    """ Subclass of elementtree.ElementTree._ElementInterface that coerces
    values set into '.text' to unicode """

    ##
    # Creates a new element object of the same type as this element.
    #
    # @param tag Element tag.
    # @param attrib Element attributes, given as a dictionary.
    # @return A new element instance.

    def makeelement(self, tag, attrib):
        return Element(tag, attrib)

    def __old_setattr(self, name, value):
        self.__dict__[name] = value
    # use the superclass __setattr__ instead of the above if it exists
    if hasattr(_BaseElement, '__setattr__'):
        __old_setattr = getattr(_BaseElement, '__setattr__').im_func

    def __setattr__(self, name, value):
        """ coerce all text to unicode """
        if name == 'text':
            value = _to_unicode(value)
        self.__old_setattr(name, value)

    def items(self):
        # return items of the attrib dictionary, but convert the values to unicode first.
        return [(key, _to_unicode(value)) for key, value in self.attrib.items()]

def Element(tag, attrib={}, **extra):
    attrib = attrib.copy()
    attrib.update(extra)
    return _ElementInterface(tag, attrib)

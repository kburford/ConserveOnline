## Script (Python) "getObjSizeAsInt"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None, size=None
##title=
##
from Products.CMFPlone.utils import base_hasattr

if obj is None:
    obj = context

const = 1024

# allow arbitrary sizes to be passed through,
# if there is no size, but there is an object
# look up the object, this maintains backwards 
# compatibility
if size is None and base_hasattr(obj, 'get_size'):
    size=obj.get_size()

# if the size is a float, then make it an int
# happens for large files
try:
    size = int(size)
except (ValueError, TypeError):
    pass

if not size:
    return 0

if same_type(size, 0) or same_type(size, 0L):
    if size < const:
        return 1
    return int(float(size/float(const)))

if not size:
    return 1
else:
    return size


## Script (Python) "search"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Search
##

view = context.restrictedTraverse('@@search')
return view()

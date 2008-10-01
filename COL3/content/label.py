# COL3
# Copyright(C), 2007, Enfold Systems, Inc. - ALL RIGHTS RESERVED
# 
# This software is licensed under the Terms and Conditions
# contained within the "license.txt" file that accompanied 
# this software.  Any inquiries concerning the scope or 
# enforceability of the license should be addressed to:
#
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

import logging
from zope.interface import implements
from Acquisition import aq_chain, aq_inner, aq_parent
from zExceptions import Unauthorized

from Products.ATContentTypes.content.document import ATDocument

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import sortable_title as ct_sortable_title

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import registerType, Schema
from Products.Archetypes.public import TextField, ReferenceField
from Products.COL3.interfaces.workspace import IWorkspace
from Products.COL3.content.base import idFromTitle
from Products.COL3.interfaces.label import ILabel
from Products.COL3.content.base import Taxonomy

class _ICanHazTitle(object):
    def __init__(self, title):
        self.Title = title

def sortable_title(title):
    return ct_sortable_title(_ICanHazTitle(title), None)
        
class Labeller(object):
    """ Utility that does most of the labeling work """
    def __init__(self, context):
        for ob in aq_chain(aq_inner(context)):
            if IWorkspace.providedBy(ob):
                self.context = ob['documents']
                break
        else:
            raise TypeError('no workspace in context')
        self.context_path = '/'.join(self.context.getPhysicalPath())
        self.ct = getToolByName(context, 'portal_catalog')

    def createLabel(self, label):
        label_metadata = {}
        workspace_fields = set('''country biogeographic_realm habitat conservation
                           conservation directthreat organization monitoring
                           description license language'''.split())
        try:
            label_id = idFromTitle(title=label, container=self.context)
        except:
            try:
                # retry
                label_id = idFromTitle(title=label.encode('ascii'), container=self.context)
            except:
                # give up
                return None 
        self.context.invokeFactory('Label', label_id, title=label)
        workspace = aq_parent(aq_inner(self.context))
        for field in workspace.Schema().fields():
            name = field.__name__ 
            if name in workspace_fields:
                accessor = field.getAccessor(workspace)
                value = accessor()
                if value:
                    label_metadata[name] = value
        self.context[label_id].update(**label_metadata)
        return self.context[label_id]

    def maybeCreateLabel(self, label):
        labelInstance = self.getLabelInstance(label)
        if labelInstance is None:
            return self.createLabel(label)
        return labelInstance

    def sortablesFromLabels(self, labels):
        sortable_map = {}
        sortable_order = {}
        for order, label in enumerate(labels):
            sortable = sortable_title(label)
            # the line below remove "duplicates" from the labels even if the
            # duplicates have trivial differences, like case differences
            # or any other differences that sortable_title() masks over
            sortable_map.setdefault(sortable, label)
            sortable_order.setdefault(sortable, order)
        # figure out which labels need to bu'Mye created
        all_sortables = sortable_map.keys()
        records = self.getLabelRecords(sortable_title=all_sortables)
        existing_sortables = set(sortable_title(record.Title)
                                 for record in records)
        new_sortables = set(sortable_map.keys()) - existing_sortables
        # create new labels
        for sortable in new_sortables:
            label = sortable_map[sortable]
            self.createLabel(label)
        # return the sortables in the original order
        sortables_order = [(order, sortable) 
                           for sortable, order in sortable_order.items()]
        sortables_order.sort()
        #query by sortable title one by one and get the uid's
        sorted_list = [sortable for order, sortable in sortables_order]
        retlist = []
        for labeltitle in sorted_list:
            label = self.ct.searchResults(portal_type='Label',
                                          path=self.context_path,
                                          sortable_title=labeltitle)
            retlist.append(label[0].UID)
        return retlist

    def setLabelsForContent(self, content, labels):
        sortables = self.sortablesFromLabels(labels)
        content.deleteReferences(relationship='LabelsThatReferenceThisContent')
        for uid in sortables:
            content.addReference(uid, relationship='LabelsThatReferenceThisContent')

    def getLabelsForContent(self, content):
        records = self.getLabelRecordsForContent(content)
        return (record.Title() for record in records)

    def getLabelRecordsForContent(self, content):
        """ This is used in common.py for the labels fragment """
        return content.getRefs(relationship='LabelsThatReferenceThisContent')

    def getLabelInstancesForContent(self, content):
        """Used in getLabelInstance in library.py, line 738"""
        for record in self.getLabelRecordsForContent(content):
            yield record
    
    def getLabelRecords(self, **kw):
        """ Will take into consideration the current users security
            used heavily in content/label.py and common.py CurrentKeywordsFragment
        """
        return self.ct.searchResults(portal_type='Label',
                                     path=self.context_path,
                                     sort_on='sortable_title',
                                     **kw)

    def getLabelRecordBySortableTitle(self, sortable):
        """ Used in browser/file.py and browser/wsdocumenttool.py"""
        __traceback_info__ = sortable
        try:
            return self.getLabelRecords(sortable_title=sortable)[0]
        except IndexError: #label was not found in the catalog
            pass
            #logger = logging.getLogger('Products.COL3.content.label')
            #logger.error('***** No label was found for the value '+sortable+' *****')

    def getLabelRecord(self, label):
        """ Used in browser/common.py, file.py, wsdocumenttool.py"""
        sortable = sortable_title(label)
        return self.getLabelRecordBySortableTitle(sortable)

    def getLabelInstance(self, label):
        """ used in browser/library.py, wsdocumenttool.py"""
        record = self.getLabelRecord(label)
        if record is not None:
            return record.getObject()
        return None

    def listLabelObjects(self):
        labelsList = []
        labels = self.getLabelRecords()
        for label in labels:
            labelsList.append({'sortable_title':sortable_title(label.Title),
                               'label':aq_inner(label.getObject())})
        return labelsList
    
    def listLabels(self):
        """ used in common.py KeywordsFragment """
        return (label.Title for label in self.getLabelRecords())
    
    def listLabelInfo(self):
        """ used in wsdocumenttool.py"""
        return [dict(label=label, 
                     search_parameter=sortable_title(label))
                for label in self.listLabels()]
        
    def listContentByLabel(self, label_id):
        cat = self.context.ws_catalog
        documents = cat.searchResults(labels=label_id)
        return documents
    
class LabelledMixin:
    
    schema = Schema((
        ReferenceField('labels',
                       multiValued=True,
                       relationship='LabelsThatReferenceThisContent',
                       allowed_types=('Label',)),
        ))
    def getLabels(self, **kw):
        return list(Labeller(self).getLabelsForContent(self))

    def setLabels(self, labels, **kw):
        Labeller(self).setLabelsForContent(self, labels)

class Label(ATDocument, Taxonomy):
    """ Labels are used to 'tag' pages and files and to hold metadata for use
    in library documents
    """
    implements(ILabel)
    labelschema = Schema((
        TextField('footer'),
                 ))

    meta_type = portal_type = archetype_name = 'Label'
    security = ClassSecurityInfo()
    schema = (ATDocument.schema.copy() + #@UndefinedVariable
              Taxonomy.schema.copy() + #@UndefinedVariable
              labelschema)

    def getTraversableBRefs(self, context):
        brefs = []
        for bref in self.getBRefs():
            try:
                brefs.append(context.restrictedTraverse("/".join(bref.getPhysicalPath())))
            except Unauthorized:
                pass
        return brefs

registerType(Label)

def addLabel(self, id, **kw):
    """ Create a new document
    """
    wg = Label(id)
    self._setObject(id, wg)
    self._getOb(id).update(**kw)


# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# Module written by Paul Everitt

"""
Validate a document agains a Relax NG schema.  Then convert the 
low-level, document-oriented error information from RNG into 
an XML structure reporting the errors.  In particular, make 
an attempt to grab the element name of the error (via the 
line number) instead of just the line number.
"""

import os.path
from lxml import etree

# Location of COL XML schema
# "Products/COL3/tests/schemas/tnc.rng"
XMLschema=os.path.join(os.path.dirname(__file__), "schemas", "tnc.rng")
FORMschema=os.path.join(os.path.dirname(__file__), "schemas", "jsboxes.rng")

def wrapFragmentWithTNCResponse(xmlstring):
    prolog = '<response><view name="validator" type="dummy" title="validator" section="dummy"/><breadcrumbs/>'
    wrapup = '</response>'
    return prolog + xmlstring + wrapup

class XMLValidator:
    
    def __init__(self, rngfn=XMLschema):
        f = open(rngfn)
        self.rngdoc = etree.parse(f)
        self.rng = etree.RelaxNG(self.rngdoc)
        f.close()
        del(f)

    def _getFieldName(self, linenum, node):
        """Given the line of an error, return the node name"""

        for el in node:
            if el.sourceline == linenum:
                return el.tag

        return None

    def __call__(self, xmldoc):
        
        if not self.rng(xmldoc):
            # Make a root element called "validation" to shove 
            # validation error information into.  Absence of this 
            # element under a <response> means the document was 
            # not validated.
            validation = etree.Element('validation')
            
            try:
                node = xmldoc.getroot()
            except AttributeError:
                # already a node?
                node = xmldoc
            # Unpack the error info
            for errormsg in self.rng.error_log:

                # Get the name of the field with the error
                fieldname = self._getFieldName(errormsg.line, node)

                # Make an <error> child under <validation> with 
                # the error information
                etree.SubElement(validation, "error",
                    line=str(errormsg.line),
                    level=str(errormsg.level_name),
                    message=str(errormsg.message),
                    typename=str(errormsg.type_name),
                    type=str(errormsg.type),
                    fieldname=str(fieldname),
                )
        else:
            # If the document as valid, return None to indicate no
            # validation errors
            validation = None
                    
        return validation
    
    def validate(self, xmldoc):
        errors = self(xmldoc)
        if errors is not None:
            print etree.tostring(errors, pretty_print=True)
            print etree.tostring(xmldoc, pretty_print=True)

    def validateString(self, xmlstring):
        xmldoc = etree.fromstring(xmlstring)
        return self.validate(xmldoc)


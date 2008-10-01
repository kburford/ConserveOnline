"""
Validate a document agains a Relax NG schema.  Then convert the 
low-level, document-oriented error information from RNG into 
an XML structure reporting the errors.  In particular, make 
an attempt to grab the element name of the error (via the 
line number) instead of just the line number.
"""

from lxml import etree
from StringIO import StringIO

class Validator:
    
    def __init__(self, rngfn):
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
            
            # Unpack the error info
            for errormsg in self.rng.error_log:

                # Get the name of the field with the error
                node = xmldoc.getroot()
                fieldname = self._getFieldName(errormsg.line, node)

                # Make an <error> child under <validation> with 
                # the error information
                error = etree.SubElement(validation, "error", 
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


def main():
    
    # Document to validate
    samplef1 = open("../types/workspace/manage-members.xml")
    sampledoc1 = etree.parse(samplef1)
    sampledoc1.xinclude()
    
    # lxml gets confused on line numbers for XInclude-based docs
    # Won't be a problem in the BE, for this demo, reparse
    samplef = StringIO(etree.tostring(sampledoc1))
    sampledoc = etree.parse(samplef)

    # Validator for a certain schema
    validator = Validator("tnc.rng")
    errors = validator(sampledoc)
    
    # Print the Error info
    if errors:
        print "Errors\n========="
        print etree.tostring(errors, pretty_print=True)
    else:
        print "No errors"

if __name__ == "__main__":
    main()

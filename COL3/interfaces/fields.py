# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: fields.py 12669 2007-05-21 22:26:17Z jens $

from zope.schema.interfaces import IASCIILine
from zope.schema.interfaces import IBool
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IPassword
from zope.schema.interfaces import IText
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import IField

class IFile(IField):
    """ Field object for handling file uploads on schemas
    """

class ICOL3ASCIILine(IASCIILine):
    """ ASCIILine field for COL3
    """

class ICOL3Bool(IBool):
    """ Bool field for COL3
    """

class ICOL3Captcha(IASCIILine):
    """ Captcha field for COL3
    """

class ICOL3Choice(IChoice):
    """ Choice field for COL3
    """

class ICOL3Password(IPassword):
    """ Password field for COL3
    """

class ICOL3Text(IText):
    """ Text field for COL3
    """

class ICOL3TextLine(ITextLine):
    """ TextLine field for COL3
    """

# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id: fields.py 20307 2007-08-29 14:20:57Z bschreiber $

from zope.interface import implements
from zope.schema import ASCIILine
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Password
from zope.schema import Text
from zope.schema import TextLine

from Products.COL3.interfaces.fields import ICOL3ASCIILine
from Products.COL3.interfaces.fields import ICOL3Bool
from Products.COL3.interfaces.fields import ICOL3Captcha
from Products.COL3.interfaces.fields import ICOL3Choice
from Products.COL3.interfaces.fields import ICOL3Password
from Products.COL3.interfaces.fields import ICOL3Text
from Products.COL3.interfaces.fields import ICOL3TextLine


class COL3ASCIILine(ASCIILine):
    """ ASCIILine field for COL3
    """
    implements(ICOL3ASCIILine)

class COL3Bool(Bool):
    """ Bool field for COL3
    """
    implements(ICOL3Bool)

class COL3Captcha(ASCIILine):
    """ Captcha field for COL3
    """
    implements(ICOL3Captcha)

class COL3Choice(Choice):
    """ Choice field for COL3
    """
    implements(ICOL3Choice)

class COL3Password(Password):
    """ Password field for COL3
    """
    implements(ICOL3Password)

class COL3Text(Text):
    """ Text field for COL3
    """
    implements(ICOL3Text)

class COL3TextLine(TextLine):
    """ TextLine field for COL3
    """
    implements(ICOL3TextLine)


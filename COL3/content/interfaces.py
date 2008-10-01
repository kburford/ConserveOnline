# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

# $Id$

from zope.interface import Interface, Attribute

class IIndexable(Interface):
    """ Interface for indexable adapters.  Different content types have
        different representations of themselves to GSA.  This is the interface
        registered for adaptionn.
    """


# The Nature Conservacy
# Copyright(C), 2006, Enfold Systems, Inc. - ALL RIGHTS RESERVED

# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com

from zope.interface import Interface
from zope.schema import TextLine
from Products.COL3.formlib.schema import RichText, ZDateTime
from zope.interface.interface import invariant
from Products.COL3.formlib.schema import EmailField
from Products.COL3.formlib.schema import TextLinesTuple
from Products.COL3.exceptions import InvariantError
from Products.COL3.validators import validateEmail

class IEventSchema(Interface):
    """ Schema that was found to be common to most discussion related types """

    title = TextLine(title=u'Title',
                     required=True)

    startDate = ZDateTime(title=u'Starts',
                          description=u'Select  Year : Month : Day and time that this event starts.',
                          required=True)

    endDate = ZDateTime(title=u'Ends',
                        description=u'Select  Year : Month : Day and time that this event finishes.',
                        required=True)

    location = TextLine(title=u'Location',
                        description=u'Short information about the location of the event.',
                        required=False)

    text = RichText(title=u'Content',
                    description=u'Rich text describing the information about the event.',
                    required=False)

    attendees = TextLinesTuple(title=u'Attendees',
                               description=u'Provide a list of attendee information, one per line.',
                               default=(),
                               missing_value=(),
                               required=False)

    contactName = TextLine(title=u'Contact Name',
                           description=u"The full name of this event's point of contact.",
                           required=True)

    contactEmail = EmailField(title=u'Contact Email',
                              description=u"Email address for this event's point of contact.",
                              required=True,
                              constraint=validateEmail)
    
    @invariant
    def validateDateRange(obj): #@NoSelf
        if obj.startDate > obj.endDate:
            raise InvariantError(u'Start date must come before end date.',
                                 fields=('startDate', 'endDate'))
        return True

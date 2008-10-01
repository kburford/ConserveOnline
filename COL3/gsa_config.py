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

# These configuration entries are only used for initial configuration of the
# gsa_tool or for tests. Once the portal is installed, please adjust these
# settings directly on the tool or re-run the 'gsatool' import step on
# GenericSetup

GSA_HOST = '10.1.36.13'
GSA_FEED_PORT = 19900
GSA_FEED = 'col3'

# Set this to True to enable tests that connect to the GSA server
# notice that these tests require that the above settings be correct and
# the server reachable, that they make the tests take longer since the tests
# have to wait for GSA to actually index the content, and that they may still
# fail, since the time the tests wait might not be enough for GSA to actually
# index the tested content.
TESTS_ENABLE = False 

# The time in minutes to wait before testing whether content has been indexed.
TEST_ASYNCH_WAIT_TIME = 5

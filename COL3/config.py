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

from zope.schema import vocabulary
from lxml.etree import XMLParser, parse
from lxml.objectify import ObjectifyElementClassLookup
import os.path
from sets import Set

parser = XMLParser(remove_blank_text=True)
parser.setElementClassLookup(ObjectifyElementClassLookup())

PROJECT_NAME           = 'COL3'
SKINS_DIR              = 'skins'
GLOBALS                = globals()

# this is hardcoded in a number of places in this product, so let's at least
# have it hardcoded in a single place.
CHARSET = 'utf-8'

DEFAULT_QUERY_COLLECTION = 'ConserveOnline'
GSA_COLLECTIONS = (DEFAULT_QUERY_COLLECTION, 'ConservationWebsites', 'GIS')
GSA_SEARCH_FOLDERS = ('library', 'workspace')

# Roles and groups names
COMMUNITY_MEMBER_ROLE = 'Community Member'
WORKGROUP_MEMBER_ROLE = 'Workspace Member'
WORKGROUP_ADMINISTRATOR_ROLE = 'Workspace Administrator'
WORKSPACE_MEMBER_GROUP_SUFFIX = 'members'
WORKSPACE_ADMIN_GROUP_SUFFIX = 'admins'

FAILED_LOGIN_PARAMETER = 'login_failed'

COL_ADMIN = 'col_admin'
TNC_ADMIN = 'conserveonline@tnc.org'
TNC_DEV_ADMIN = 'conserveonline-dev@tnc.org'

STOP_WORDS = ['A ', 'An ', 'The ']

def titleWithoutStopword(title):
    if [title[len(r):] for r in STOP_WORDS if title.startswith(r)]:
        return [title[len(r):] for r in STOP_WORDS if title.startswith(r)][0]
    else:
        return title

# list of AT fields from COL3 COLMember archetypes that will be queried for
# completness in the profile percentage in the top-right corner of the pages
PROFILE_PERCENTAGE_FIELDS = """
fullname
email
type_of_organization
organization
country
description
""".strip().split('\n')

WORKSPACE_TYPE = 'Workspace'

def vocabularyFromTuples(t):
    return vocabulary.SimpleVocabulary([
        vocabulary.SimpleTerm(value, title=label)
        for value, label in t
    ])

def termFromXML(term_tag):
    # SimpleTerm does the right thing when the token is None
    title = unicode(term_tag.text, CHARSET)
    value = term_tag.attrib.get('id', title)
    token = term_tag.attrib.get('id', term_tag.text)
    return vocabulary.SimpleTerm(value=value,
                                 token=token,
                                 title=title)

def vocabularyFromXML(vocabulary_tag):
    terms = [termFromXML(term_tag)
             for term_tag in vocabulary_tag.term]
    vocab = vocabulary.SimpleVocabulary(terms)
    vocab.id = vocabulary_tag.attrib['id']
    return vocab

cref_schema_path = os.path.join(os.path.dirname(__file__), 'shared', 'crossref4.3.0.xsd')
crossref_schema = open(cref_schema_path)
vocab_file = open(os.path.join(os.path.dirname(__file__), 'shared', 'vocabularies.xml'))
vocab_xml = parse(vocab_file, parser).getroot()
del vocab_file

def vocabularyById(vocab_id):
    vocab_tag, = [tag for tag in vocab_xml.vocabulary
                  if tag.attrib['id'] == vocab_id]
    return vocabularyFromXML(vocab_tag)

ORGANIZATIONS_TYPES = vocabularyById('organizationtypes')
ORGANIZATIONS_TYPES_DEFAULT = "other"
assert ORGANIZATIONS_TYPES_DEFAULT in ORGANIZATIONS_TYPES.by_value

PROFILE_BACKGROUNDS = vocabularyById('backgrounds')
PROFILE_BACKGROUNDS_DEFAULT = "other"
assert PROFILE_BACKGROUNDS_DEFAULT in PROFILE_BACKGROUNDS.by_value

NATIONS = vocabularyById('countries')
NATIONS_DEFAULT = 'USA'
assert NATIONS_DEFAULT in NATIONS.by_value

nation_terms = NATIONS._terms
nation_terms.append(vocabulary.SimpleTerm(value='', token='', title=u'No Value'))
nation_vocab = vocabulary.SimpleVocabulary(nation_terms)
nation_vocab.id = 'countries'

LANGUAGES = vocabularyById('languages')
LANGUAGES_DEFAULT = 'en'
assert LANGUAGES_DEFAULT in LANGUAGES.by_value

LICENSES_VOCABULARY = vocabularyById('licenses')
LICENCES_DEFAULT = 'a-nc'
assert LICENCES_DEFAULT in LICENSES_VOCABULARY.by_value

BIOGEOGRAPHIC_REALMS = vocabularyById('biogeographic_realms')
BIO_REALMS_DEFAULT = 'nearctic'
assert BIO_REALMS_DEFAULT in BIOGEOGRAPHIC_REALMS.by_value

bio_terms = BIOGEOGRAPHIC_REALMS._terms
bio_terms.append(vocabulary.SimpleTerm(value='', token='', title=u'No Value'))
bio_vocab = vocabulary.SimpleVocabulary(bio_terms)
bio_vocab.id = 'biogeographic_realms'

DOCUMENT_TYPE_VOCABULARY = vocabularyById('documenttypes')

HABITAT_VOCABULARY = vocabularyById('habitats')

DELIVERY_CHOICE = vocabularyFromTuples([('email', u'Email'),
                                       ('rss', u'RSS')])

CONSERVATION_VOCABULARY = vocabularyById('conservation')

DIRECT_THREAT_VOCABULARY = vocabularyById('directthreat')

MONITORING_VOCABULARY = vocabularyById('monitoring')

LANGUAGES_VOCABULARY = vocabularyById('languages')

WORKGROUP_FEATURES = vocabularyFromTuples([
("discussion", u"""Discussions: <span class="fieldHelp">Explanation of this feature goes here.</span>"""),

("calendar", u"""Calendar: <span class="fieldHelp">Explanation of this feature goes here.</span>"""),
])
WORKGROUP_FEATURES_DEFAULT = Set()
# make sure all elements of the default are in the vocabulary
assert not WORKGROUP_FEATURES_DEFAULT - Set([term.value for term in WORKGROUP_FEATURES])

WORKGROUP_CUSTOMIZATION_LEVEL_OPTIONS = vocabularyFromTuples([
("basic", u"""Basic customization options."""),
("advanced", u"""Advanced customization options."""),
])
WORKGROUP_CUSTOMIZATION_LEVEL_DEFAULT = list(WORKGROUP_CUSTOMIZATION_LEVEL_OPTIONS)[0].value

biorealm_vocab_file = open(os.path.join(os.path.dirname(__file__),
                                        'shared',
                                        'vocabularies.xml'))
biorealm_vocab_tag, = [tag for
                       tag in parse(biorealm_vocab_file,
                                    parser).getroot().vocabulary
                       if tag.attrib['id'] == "biogeographic_realms"]

BIOGEOGRAPHIC_REALMS = vocabularyFromXML(biorealm_vocab_tag)

WORKGROUP_WORKAREAS = u"""
Conservation Planning
Conservation Action
Direct Threats
Specific Geography
Specific BioGeography
Other
""".strip().split('\n')

WORKGROUP_ISPRIVATE_OPTIONS = vocabularyFromTuples([
(False, u"""Public, everyone can see content not made private."""),

(True, u"""Private, only workspace members can see content."""),
])

WORKGROUP_ISPRIVATE_DEFAULT = list(WORKGROUP_ISPRIVATE_OPTIONS)[0].value

WORKGROUP_REMOVELOGO_OPTIONS = vocabularyFromTuples([
("no", u"""No, keep using my images."""),

("yes", u"""Yes, discard my images and return to defaults."""),
])

WORKGROUP_REMOVELOGO_DEFAULT = list(WORKGROUP_REMOVELOGO_OPTIONS)[0].value

GENERATE_DOI_OPTIONS = vocabularyFromTuples([
("yes", u"""Yes, do create a DOI"""),
("no", u"""No, do NOT create a DOI"""),
])

GENERATE_DOI_OPTIONS_DEFAULT = list(GENERATE_DOI_OPTIONS)[0].value

WORKGROUP_SECURITY_UPDATE_OPTIONS = vocabularyFromTuples([
("open", u"""All members of the workgroup can add, update, and delete documents and help manage the group. <span><a href="javascript:;" class="tooltip"><img src="/static/images/bulletInfo.gif" border="0"/><span>This works best for very small groups where all members are equal</span></a></span>"""),

("protected", u"""All members of the workgroup can add and update documents, and delete their own documents if necessary. Only a select few can manage the group. <span><a href="javascript:;" class="tooltip"><img src="/static/images/bulletInfo.gif" border="0"/><span>This works best for most groups</span></a></span>"""),

("approval", u"""All members can add documents, but they must be reviewed and approved before others can see them. Only a select few can manage the group. <span><a href="javascript:;" class="tooltip"><img src="/static/images/bulletInfo.gif" border="0"/><span>Not recommended for most groups, because this makes document sharing more complicated</span></a></span>"""),
])
WORKGROUP_SECURITY_UPDATE_DEFAULT = list(WORKGROUP_SECURITY_UPDATE_OPTIONS)[0].value

WORKGROUP_SECURITY_VISIBILITY_OPTIONS = vocabularyFromTuples([
("open", u"""The public can view everything in the workgroup."""),

("closed", u"""The public can see a description of the workgroup, but everything in it is private for workgroup members only."""),
])
WORKGROUP_SECURITY_VISIBILITY_DEFAULT = list(WORKGROUP_SECURITY_VISIBILITY_OPTIONS)[0].value

CONTENT_ISPRIVATE_OPTIONS = vocabularyFromTuples([
(False, u"""No"""),
(True, u"""Yes (only workspace members can see the file)"""),
])
CONTENT_ISPRIVATE_DEFAULT = list(CONTENT_ISPRIVATE_OPTIONS)[0].value

RATING_FLAGGED_OPTIONS = vocabularyFromTuples([
(False, u"""No"""),
(True, u"""Yes"""),
])
RATING_FLAGGED_DEFAULT = list(RATING_FLAGGED_OPTIONS)[0].value

RATING_OPTIONS = vocabularyFromTuples([
(0, u""""""),
(1, u"""*"""),
(2, u"""**"""),
(3, u"""***"""),
(4, u"""****"""),
(5, u"""*****"""),
])

NOREPLY_SENDER_ADDRESS = 'donotreply@tnc.org'

RESET_PASSWORD_SUBJECT = """
ConserveOnline Password Reset Request
""".strip()

RESET_PASSWORD_EMAIL_BODY = """
Please go to the following url to reset the password for your ConserveOnline account.

%s
""".strip()

INVITATION_EMAIL_SUBJECT = """
Join the "%(workspace_name)s" Workspace on ConserveOnline
""".strip()

INVITATION_EMAIL_BODY = """
Welcome.

As a manager of %(workspace_name)s workspace, I invite you to join
this online collaboration space within the ConserveOnline community. By joining, you will
be able to participate in discussions, share documents, and work collaboratively
with others who are also members of this workspace.

About the %(workspace_name)s workspace:

%(workspace_overview)s

ConserveOnline is an international online community dedicated to connecting
conservation practitioners and sharing conservation knowledge. In addition to
many public workspsaces, it contains a library of articles, case studies,
plans, and other resources related to environmental conservation, as well as
useful information about options for publishing your work. Participation in
ConserveOnline is completely free. Registered users can upload documents,
create or participate in workspaces to support any type of conservation project
or research, and create personal profiles.

Please click the following link to accept your invitation and start participating
in %(workspace_name)s.

%(invitation_url)s

To reject the invitation, please click on the same link and then choose 'Reject Invitation' at the bottom of the page.

Sincerely,
%(workspace_manager)s
""".strip()

WORKSPACE_ACCEPT_SUBJECT = "Your Request to Join the %s Workspace Has Been Accepted"

WORKSPACE_ACCEPT_TEMPLATE = """
You have now been added to the %s workspace.

What is ConserveOnline?
ConserveOnline is an online community intended to foster learning and
collaboration, and provide information and support to anyone making
conservation-related decisions. Learn more:
http://conserveonline.org/about/aboutus
""".strip()

WORKSPACE_REJECT_SUBJECT = "Your Request to Join the %s Workspace Has Been Rejected"

WORKSPACE_REJECT_TEMPLATE = """
Unfortunately, your request to join the %s workspace can not be accepted at
this time.

What is ConserveOnline?
ConserveOnline is an online community intended to foster learning and
collaboration, and provide information and support to anyone making
conservation-related decisions. Learn more:
http://conserveonline.org/about/aboutus
"""

WORKSPACE_INVITEREJECTED_SUBJECT = "Workspace Invitation Rejected"

WORKSPACE_INVITEREJECTED_TEMPLATE = """
The user, %s, has chosen to reject your invitation to join the %s workspace.

What is ConserveOnline?
ConserveOnline is an online community intended to foster learning and
collaboration, and provide information and support to anyone making
conservation-related decisions. Learn more:
http://conserveonline.org/about/aboutus
"""

WORKSPACE_JOINREQUEST_SUBJECT = "New Request to Join the %s Workspace"

WORKSPACE_JOINREQUEST_TEMPLATE = """
A new user has requested to join the %s workspace, of which you're a manager.
Please visit the Workspace Member Management area at:
%s/wsmembers/workspace-members.html

What is ConserveOnline?
ConserveOnline is an online community intended to foster learning and
collaboration, and provide information and support to anyone making
conservation-related decisions. Learn more:
http://conserveonline.org/about/aboutus
"""

WORKSPACE_REMOVED_SUBJECT = "You Have Been Removed From the %s Workspace"

WORKSPACE_REMOVED_TEMPLATE = """
You have been removed from the %s workspace.  If this removal was in error
please contact your workspace administrator.

What is ConserveOnline?
ConserveOnline is an online community intended to foster learning and
collaboration, and provide information and support to anyone making
conservation-related decisions. Learn more:
http://conserveonline.org/about/aboutus
"""

ERROR_EMAIL_SUBJECT = 'COL3 Error Occurred'
ERROR_EMAIL_BODY = """
COL3 Exception was caught with the following message:
...
%s
"""

RECOMMENDATION_REPORT_SUBJECT = 'Inappropriate Content Submission'
RECOMMENDATION_REPORT_BODY = """
Rating info:

  - Rating Author: %(author)s
  - Rating Date..: %(timestamp)s
  - Content Title: %(title)s
  - Content URL..: %(url)s

Reported by %(username)s, with the following comment:

%(comment)s
"""

RECOMMENDATION_BAD_CONTENT_SUBJECT = 'Profanity - Rating Post'
RECOMMENDATION_BAD_CONTENT_BODY = """
Bad content detected in a rating post:

  - Rating Author: %(author)s
  - Rating Date..: %(timestamp)s
  - Content......: %(content)s
  - Comment Title: %(title)s
  - Comment URL..: %(url)s

The comment body has this content:

%(comment)s
"""

# define the maximum number of links that will be sent in a subscription digest email
MAX_SUBSCRIPTION_LINKS = 50

SUBSCRIPTION_EMAIL_SUBJECT = 'Thank You For Subscribing To ConserveOnline'
SUBSCRIPTION_EMAIL_BODY = """
You've just subscribed to receive content from ConserveOnline.

These are the 10 most recently added items that match your filter criteria:

%s

To unsubscribe, click in the link below:
%s
""".strip()

SUBSCRIPTION_DIGEST_EMAIL_SUBJECT = 'ConserveOnline Update'
SUBSCRIPTION_DIGEST_EMAIL_BODY = """
You're receiving an update containing the new items that have been posted to
ConserveOnline since the previous notification:

%s

To unsubscribe, click in the link below:
%s
""".strip()

CROSSREF_EMAIL_SUBJECT = 'ConserveOnline Submission Error - #%s'
CROSSREF_EMAIL_BODY = """
There was an error with a cross reference record submitted by ConserveOnline.

Submission ID - %s
Batch Id      - %s
DOI           - %s

Message:
%s
"""

CROSS_REF_ERRORS_TNC = ('Record not processed because submitted version',
                        'previously submitted version',
                        'Added with conflict',
                        'All prefixes in a submission must match',
                        'not a valid integer',
                        'Invalid content starting with',
                        'previously deleted by a CrossRef admin',
                        'org.jdom.input.JDOMParseException',
                        'java.io.UTFDataFormatException',
                        'Content is not allowed in prolog',
                        'Report elements are currently allowed in live area only')
CROSS_REF_ERRORS_CROSSREF = ('User with ID',
                             'not allowed to add records',
                             'user not allowed',)

WS_MEMBER_MANAGE = 'WS_MEMBER_MANAGE'
WS_JOIN = 'WS_JOIN'

viewattribs = {WS_MEMBER_MANAGE:{'type':'workspace','name':'manage-members.html','section':'workspaces', 'titlexpath':'titlexpath'},
               WS_JOIN:{'type':'workspace','name':'add-joinrequest.html','section':'workspaces', 'titlexpath':'titlexpath'}}

# List of products that should be installed by quickinstaller and are not
# installed directly by other import steps
QUICKINSTALLER_DEPENDENCIES = """
""".strip().split('\n')

MIMETYPES = {'application/msword':'doc',
             'application/vnd.ms-excel':'xls',
             'application/octet-stream':'exe',
             'application/zip':'zip',
             'application/vnd.ms-powerpoint':'ppt',
             'application/pdf':'pdf',
             'text/html':'html',
             'image/jpeg':'image',
             'image/gif':'image',
             'image/x-icon':'image',
             'image/tiff':'image',
             'image/bmp':'image',
             'image/png':'image',
             'image/x-portable-anymap':'image',
             'image/x-portable-bitmap':'image',
             'image/x-portable-graymap':'image',
             'image/x-portable-pixmap':'image',
             'image/svg+xml':'image',
             'video/x-msvideo':'avi',
             'video/mpeg':'video',
             'video/quicktime':'video',
             'video/x-sgi-movie':'video',
             'video/x-msvideo': 'video',
             'video/x-ms-asf':'video',
             'text/plain':'text',
             'text/richtext':'text',
             'text/css':'text',
             'text/xml':'text',
             'text/xsl':'text',
             'audio/x-wav':'wav',
             'audio/basic':'audio',
             'audio/basic':'audio',
             'audio/mid':'audio',
             'audio/mid':'audio',
             'audio/mpeg':'audio',
             'audio/x-aiff':'audio',
             'audio/x-mpegurl':'audio',
             'audio/x-pn-realaudio':'audio',
             }

DOCUMENT_TYPES = {"documenttypes":"Document Types",
                  "casestudies":"Case Studies",
                  "datasets":"Data Sets &amp; Statistics",
                  "ecoregionalplans":"Ecoregional Plans",
                  "factsheet":"Fact Sheets",
                  "graphics":"Graphics &amp; Images",
                  "laws":"Laws &amp; Policies",
                  "maps":"Maps",
                  "practicemethods":"Practice / Methods",
                  "presentations":"Presentations",
                  "publications":"Publications",
                  "reports":"Reports / Analysis",
                  "siteconservation":"Site Conservation Plans",
                  "siteprofiles":"Site Profiles",
                  "standards":"Standards / Guidelines",
                  "tools":"Tools &amp; Software",
                  "unpublished":"Unpublished Documents",
                  "websites":"Web Sites",
                  "other":"Other",}

WS_DOCTOOL_INTERFACES = ('Products.COL3.interfaces.page.IPage',
                         'Products.COL3.interfaces.file.IFile',)

TIMEZONE = "US/Eastern"

INDEXABLE_TYPES="""
COLFile
COLPage
Label
LibraryFile
PloneboardConversation
PloneboardComment
""".strip().split()

SCAN_TYPES="""
COLFile
LibraryFile
""".strip().split()

THUMBNAIL_TYPES = ('image/gif', 'image/jpeg', 'image/png')

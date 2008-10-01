tncfe provides the front-end for COL 3.0.  XML files from the Plone back-end are intercepted by the Apache mod_python
extension and turned into HTML using tncfe's XSL templates, CSS, JS, and static images.

REQUIREMENTS
    
    Apache config must point DocumentRoot at the tncfe folder.
    Apache must include the mod_python extension, and Python must include the lxml and enfold.lxml extensions.

INSTALLATION
    
    simply store in any folder reachable by Apache.

FOLDER STRUCTURE

docs -- contains pdf outlining this method of providing XSLT front-end for Plone; also contains a tutorial.
rendered -- sample html pages as rendered by Apache-mod_python-lxml.
schemas -- contains tnc.rng, the Relaxed NG schema that comprises the contract between front-end and back-end.
shared -- XSL templates used in rendering all COL3.0 pages.
static -- repository of css, images (glyphs, etc), and js.  js includes tinyMCE and ext libraries.
types -- contains XSL templates for specific COL3.0 content types as well as sample XML files to expect from back-end.

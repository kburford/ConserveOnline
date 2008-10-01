
This folder contains the Python codebase that extends Plone 3.0 for COL 3.0.

REQUIREMENTS
    
    Plone 3.0; Zope 2.10.5; Python 2.4.4; enfold.gsa; CachedGSAIndexer

INSTALLATION
    
    see installation doc in COL3.0/docs/trunk

FOLDER STRUCTURE

browser -- contains Python code to construct COL3.0 views
content -- contains Python code to manage COL3.0 content types
conf -- Apache, EZProxy, and zope configs; also initial content for the about folder
docs -- misc docs.  Overall COL3.0 installation docs are in COL3.0/docs
Extensions -- Python scripts for zopectl or external methods
formlib -- form layouts and widgets
interfaces -- contains Python code to define view layouts
profiles -- content, setup, and workflow definitions and defaults
search -- Google search components (Google proper, not GSA)
shared -- copy of tncfe/shared; created by EXTERNALS.txt
skins -- required for col3member addition [?]
tests -- overall regression tests
tools -- Python code for workspace member management widgets
www -- COL3MultiPlugin for PlonePAS user authentication

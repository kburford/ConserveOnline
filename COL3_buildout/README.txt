COL3_buildout creates the Zope-Plone-COL3 back-end.


REQUIREMENTS
    
    for a tagged build, exact version numbers are given in buildout.cfg

    The backend buildout assumes this folder structure and that the files shown have been downloaded:

    ConserveOnline
    -- COL3_buildout
    -- downloads
            AdvancedQuery.tgz
            Archetypes-1.5.6.tgz
            Archetypes-1.5.8-2.tar.gz
            ATContentTypes-1.2.4.tgz
            ATContentTypes-1.2.5.tgz
            ATReferenceBrowserWidget-2.0.1.tar.gz
            CMF-2.1.1.tar.gz
            CMFDiffTool-0.3.5.tgz
            CMFDiffTool-0.3.6.tgz
            CMFDynamicViewFTI-3.0.1.tar.gz
            CMFDynamicViewFTI-3.0.2.tar.gz
            CMFEditions-1.1.4.tgz
            CMFEditions-1.1.6.tgz
            CMFFormController-2.1.1.tar.gz
            CMFFormController-2.1.2.tar.gz
            cmfplacefulworkflow-1-2-1.tgz
            cmfplacefulworkflow-1-3-1.tgz
            CMFQuickInstallerTool-2.0.4.tar.gz
            CMFQuickInstallerTool-2.1.4.tar.gz
            CMFTestCase-0.9.7.tar.gz
            ExtendedPathIndex-2.4.tgz
            ExternalEditor-0.9.3-src.tgz
            GenericSetup-1.4.0.tar.gz
            groupuserfolder-3-55-1.tgz
            kupu-1-4-8.tgz
            kupu-1-4-9.tgz
            NuPlone-0.9.3.tgz
            NuPlone-1.0b2.tar.gz
            PasswordResetTool-1.0.tar.gz
            PasswordResetTool-1.1.tar.gz
            PlacelessTranslationService-1.4.11.tar.gz
            PlacelessTranslationService-1.4.8.tar.gz
            PloneBase-3.0.6.tar.gz
            PloneBase-3.1.1.tar.gz
            PloneLanguageTool-2.0.2.tar.gz
            PloneLanguageTool-2.0.3.tar.gz
            PlonePAS-3.2.tar.gz
            PlonePAS-3.4.tar.gz
            PloneTestCase-0.9.7.tar.gz
            PloneTranslations-3.0.11.tar.gz
            PloneTranslations-3.1.1.tar.gz
            PluggableAuthService-1.5.3.tar.gz
            PluginRegistry-1.1.2.tar.gz
            resourceregistries-1-4-1.tgz
            resourceregistries-1-4-2.tgz
            SecureMailHost-1.1.tar.gz
            statusmessages-3.0.3-tar.gz
            Zope-2.10.5-final.tgz
            ZopeVersionControl-0.3.4.tar.gz
    -- eggs
            4Suite_XML-1.0.2-py2.4-linux-i686.egg
            archetypes.kss-1.2.5-py2.4.egg
            archetypes.kss-1.2.6-py2.4.egg
            archetypes.schemaextender-1.0b1-py2.4.egg
            BeautifulSoup-3.0.5-py2.4.egg
            elementtidy-1.0_20050212-py2.4-linux-i686.egg
            elementtree-1.2.6_20050316-py2.4.egg
            five.customerize-0.2-py2.4.egg
            five.localsitemanager-0.3-py2.4.egg
            ipython-0.8.2-py2.4.egg
            kss.core-1.2.4-py2.4.egg
            lxml-1.3.6-py2.4-linux-i686.egg
            PILwoTk-1.1.6.3-py2.4-linux-i686.egg
            plone.app.content-1.0.1-py2.4.egg
            plone.app.contentmenu-1.0.6-py2.4.egg
            plone.app.contentrules-1.0.5-py2.4.egg
            plone.app.controlpanel-1.0.4-py2.4.egg
            plone.app.customerize-1.0.1-py2.4.egg
            plone.app.form-1.0.4-py2.4.egg
            plone.app.i18n-1.0.3-py2.4.egg
            plone.app.iterate-1.0-py2.4.egg
            plone.app.kss-1.2.5-py2.4.egg
            plone.app.layout-1.0.5-py2.4.egg
            plone.app.linkintegrity-1.0.5-py2.4.egg
            plone.app.openid-1.0.1-py2.4.egg
            plone.app.portlets-1.0.6-py2.4.egg
            plone.app.redirector-1.0.5-py2.4.egg
            plone.app.viewletmanager-1.0-py2.4.egg
            plone.app.vocabularies-1.0.3-py2.4.egg
            plone.app.workflow-1.0.1.1-py2.4.egg
            plone.contentratings-1.0_beta1-py2.4.egg
            plone.contentrules-1.0.5-py2.4.egg
            plone.fieldsets-1.0-py2.4.egg
            plone.i18n-1.0.3-py2.4.egg
            plone.intelligenttext-1.0.1-py2.4.egg
            plone.locking-1.0.5-py2.4.egg
            plone.memoize-1.0.3-py2.4.egg
            plone.openid-1.0.1-py2.4.egg
            plone.portlets-1.0.5-py2.4.egg
            plone.recipe.command-1.0-py2.4.egg
            plone.recipe.distros-1.3-py2.4.egg
            plone.recipe.plone-3.0.6-py2.4.egg
            plone.recipe.zope2install-1.2-py2.4.egg
            plone.recipe.zope2instance-1.3-py2.4.egg
            plone.recipe.zope2instance-1.8-py2.4.egg
            plone.recipe.zope2zeoserver-0.10-py2.4.egg
            plone.recipe.zope2zeoserver-0.13-py2.4.egg
            plone.session-1.2-py2.4.egg
            plone.theme-1.0-py2.4.egg
            Products.contentmigration-1.0b4-py2.4.egg
            Products.Ploneboard-2.0.1-py2.4.egg
            Products.Ploneboard-2.0rc1-py2.4.egg
            Products.SimpleAttachment-3.0.2-py2.4.egg
            python_openid-2.0.1-py2.4.egg
            setuptools-0.6c8-py2.4.egg
            wicked-1.1.6-py2.4.egg
            zc.buildout-1.0.0-py2.4.egg
            zc.buildout-1.0.1-py2.4.egg
            zc.recipe.egg-1.0.0-py2.4.egg
            ZConfig-2.4a6-py2.4.egg
            zdaemon-1.4a2-py2.4.egg
            ZODB3-3.8.0-py2.4-linux-i686.egg
            zodbcode-3.4.0-py2.4.egg
            zope.interface-3.3.0.1-py2.4-linux-i686.egg
            zope.proxy-3.4.0-py2.4-linux-i686.egg
            zope.testing-3.0-py2.4.egg
    -- python-extensions
            lxml-1.3.6.tgz
            mod_python-3.3.1.tgz
            python-dateutil-1.4.tar
    -- setup
            ez_setup.py
            setuptools-0.6c8-py2.4.egg    
    -- src
       -- enfold.lxml
       -- plone.app.blob
       -- plone.contentratings-1.0-beta1
       -- z3c.etree
       -- Products
          -- COL3
          -- qPloneCaptchas
    -- tncfe

INSTALLATION
    
    See details in docs/COL3 installation instructions.doc

CONFIGURATION FILES
    
    buildout.cfg - generic configuration, creating a single zope instance under zeo

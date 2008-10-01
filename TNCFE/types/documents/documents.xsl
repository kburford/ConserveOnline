<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY copy   "&#169;">
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    <xsl:output indent="yes"/>
    <xsl:template match="view[@name='view.html' and @type='page']">
        
        <xsl:apply-templates select="/response/currentkeywords"/>
        
        <!-- Hack for Gateway stuff -->
        <xsl:variable name="currurl" select="/response/breadcrumbs/entry/@href"/>
        <xsl:if
            test="(/response/workspace/@href=concat($currurl, '/workspaces/cbdgateway')) and (/response/view[@name!='gsa.html'])">
            <div style="margin-top: 10px;">
                <script language="JavaScript1.2" type="text/javascript"> writeGatewayNav();
                </script>
            </div>
            
            <xsl:variable name="baseurl" select="/response/breadcrumbs/base"/>
            <xsl:if test = "contains($baseurl, '-era')" >
                <span>
                    <script language="JavaScript1.2" type="text/javascript">
                        writeERANav();
                    </script>
                </span> 
            </xsl:if>
            
            <xsl:if test = "contains($baseurl, '-cap')" >
                <span>
                    <script language="JavaScript1.2" type="text/javascript">
                        writeCAPNav();
                    </script>
                </span> 
            </xsl:if>
            
            <xsl:if test = "contains($baseurl, '-net')" >
                <span>
                    <script language="JavaScript1.2" type="text/javascript">
                        writeConsNetNav();
                    </script>
                </span> 
            </xsl:if>
            
            <xsl:if test = "contains($baseurl, '-top')" >
                <span>
                    <script language="JavaScript1.2" type="text/javascript">
                        writeTopicsNav();
                    </script>
                </span> 
            </xsl:if>
            
        </xsl:if>
        
        <xsl:if test="(/response/breadcrumbs/entry[4]/@href=concat($currurl, '/workspaces/cbdgateway/era/')) and (/response/view[@name!='gsa.html'])">					
            <span>
                <script language="JavaScript1.2" type="text/javascript">
                    writeERANav();
                </script>
            </span>
        </xsl:if>
        
        <xsl:if test="(/response/breadcrumbs/entry[4]/@href=concat($currurl, '/workspaces/cbdgateway/cap/')) and (/response/view[@name!='gsa.html'])">					
            <span>
                <script language="JavaScript1.2" type="text/javascript">
                    writeCAPNav();
                </script>
            </span>
        </xsl:if>
        
        <xsl:if test="(/response/breadcrumbs/entry[4]/@href=concat($currurl, '/workspaces/cbdgateway/networks/')) and (/response/view[@name!='gsa.html'])">					
            <span>
                <script language="JavaScript1.2" type="text/javascript">
                    writeConsNetNav();
                </script>
            </span>
        </xsl:if>
        
        <xsl:if test="(/response/breadcrumbs/entry[4]/@href=concat($currurl, '/workspaces/cbdgateway/topics/')) and (/response/view[@name!='gsa.html'])">					
            <span>
                <script language="JavaScript1.2" type="text/javascript">
                    writeTopicsNav();
                </script>
            </span>
        </xsl:if>
        
        <xsl:if test="(/response/breadcrumbs/base=concat($currurl, '/workspaces/cbdgateway/documents/conservation-measures/')) and (/response/view[@name!='gsa.html'])">					
            <span>
                <script language="JavaScript1.2" type="text/javascript">
                    writeTopicsNav();
                </script>
            </span>
        </xsl:if>
        
        <xsl:if test="(/response/breadcrumbs/base=concat($currurl, '/workspaces/cbdgateway/documents/marine-resources/')) and (/response/view[@name!='gsa.html'])">					
            <span>
                <script language="JavaScript1.2" type="text/javascript">
                    writeTopicsNav();
                </script>
            </span>
        </xsl:if>
        
        <div style="margin-top: 20px">
            <xsl:apply-templates select="../resource/text/*" mode="copy"/>
        </div>
    </xsl:template>
    <xsl:template match="currentkeywords">
        By <a href="{/response/resource/author/@href}"><xsl:apply-templates select="/response/resource/author" mode="byline"/></a> on <xsl:apply-templates select="/response/resource/creation_date" mode="griddate"/> |  
        Keyword(s): <xsl:for-each select="item">
            <a href="{@href}">
                <xsl:value-of select="."/>
            </a>
            <xsl:if test="position() != last()">; </xsl:if>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="view[@name='view.html' and @type='file']">
        <xsl:apply-templates select="/response/currentkeywords"/>
        <xsl:apply-templates select="../resource/attachments/attachment"/>
        <xsl:apply-templates select="../resource/gisdata"/>
        <xsl:if test="../resource/description">
            <p>
                <xsl:apply-templates select="../resource/description" mode="copy" />
            </p>
        </xsl:if>
        <xsl:apply-templates select="../resource[libraryreference]" mode="taxonomytable"/>
        <xsl:apply-templates select="../resource/abstract"/>
        <xsl:if test="not(../resource/abstract)">
            <div class="clearBox clearBoth"/>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="inlibrary">
        <div class="profileHeader textCenter"> ** This document has been added to the library. **
        </div>
    </xsl:template>
    <xsl:template match="is_private[.='1']">
        <div class="profileHeader textCenter"> ** This document is private. ** </div>
    </xsl:template>
    
    <xsl:template
        match="formcontroller[../view/@name='addtolibrary-file.html' and ../view/@type='file']"
        mode="formhelp">
        <p class="formHelp">The ConserveOnline library is the place to put your finished products when you want to give them the broadest possible distribution. 
            The library is intended to be a more formal and permanent archive than the ConserveOnline workspaces. 
            All documents in ConserveOnline are available for full-text searches; the library documents have additional features that 
            make them even easier for search engines to find.</p>
    </xsl:template>
    
    <xsl:template match="formcontroller[../view/@name='add.html' and ../view/@type='file']"
        mode="formhelp">
        <p class="formHelp">This allows you to upload a document, image, or any type of file to your
            workspace.</p>
    </xsl:template>
    <xsl:template match="view[(@name='withkeyword.html' or @name='bykeyword.html') and @type='documents']">
        <p class="formHelp"><b>Keywords are used to describe and (similarly) organize files and
            pages in a workspace. </b> In migrated workspaces, they are initially set to the
            foldername in which a file or page was previously located. <a
                href="{$staticprefix}html/keyword_popup.html"
                onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
                return false;"
                >More</a></p>
        <div style="margin-top: 20px">
            <xsl:apply-templates select="/response/currentlabel/text/*" mode="copy"/>
            <p>
                <xsl:apply-templates select="/response/currentlabel/description/*" mode="copy"/>
            </p>
        </div>
        <xsl:apply-templates select="../batch"/>
        <div class="tncFooter">
            <xsl:apply-templates select="../currentlabel/footer/*" mode="copy"/>
        </div>
    </xsl:template>
    
    

    
</xsl:stylesheet>

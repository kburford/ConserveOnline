<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY copy   "&#169;">
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    <xsl:output indent="yes"/>
    
    <xsl:template match="view[@name='view.html' and @type='libraryfile']">
        
        <xsl:variable name="star-img">
            <xsl:value-of select="/response/ratings/score"/>
        </xsl:variable>
        
        <xsl:variable name="star-count">
            <xsl:choose>
                <xsl:when test="/response/ratings/score='05'">
                    <span>A Half Star</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='10'">
                    <span>One Star</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='15'">
                    <span>One And A Half Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='20'">
                    <span>Two Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='25'">
                    <span>Two And A Half Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='30'">
                    <span>Three Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='35'">
                    <span>Three And A Half Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='40'">
                    <span>Four Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='45'">
                    <span>Four And A Half Stars</span>
                </xsl:when>
                <xsl:when test="/response/ratings/score='50'">
                    <span>Five Stars</span>
                </xsl:when>
                <xsl:otherwise>
                    <span>No Stars</span>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <xsl:apply-templates select="../resource/attachments/attachment"/>

        
        <xsl:apply-templates select="../resource" mode="taxonomytable"/>
        <xsl:apply-templates select="../resource/gisdata"/>
        <xsl:apply-templates select="../resource/description"/>
    </xsl:template>
    
    <xsl:template match="view[@type='libraryfile'][@name='view-recommendations.html']">
        <xsl:for-each select="/response/reviews/review">
            <xsl:variable name="star-img">
                <xsl:value-of select="rating"/>
            </xsl:variable>
            <xsl:variable name="posItem">
                <xsl:value-of select="position()"/>
            </xsl:variable>
	    <xsl:variable name="rec-user">
	       <xsl:value-of select="username"/>
	   </xsl:variable>
            
            <xsl:variable name="star-count">
                <xsl:choose>
                    <xsl:when test="/response/reviews/review/rating='05'">
                        <span>A Half Star</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='10'">
                        <span>One Star</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='15'">
                        <span>One And A Half Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='20'">
                        <span>Two Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='25'">
                        <span>Two And A Half Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='30'">
                        <span>Three Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='35'">
                        <span>Three And A Half Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='40'">
                        <span>Four Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='45'">
                        <span>Four And A Half Stars</span>
                    </xsl:when>
                    <xsl:when test="/response/reviews/review/rating='50'">
                        <span>Five Stars</span>
                    </xsl:when>
                    <xsl:otherwise>
                        <span>No Stars</span>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <div class="ratingsView">
                <p> <img src="{$staticprefix}images/stars_{$star-img}.gif" alt="{$star-count}"></img> 
                    <xsl:if test="title">
                        &nbsp; <strong><xsl:value-of select="title"/></strong> 
                    </xsl:if><br/> 
                    Submitted By <a href="{bio/@href}"><xsl:value-of select="reviewer"/></a>  on <xsl:apply-templates select="modified" mode="bloglongform"/>  <xsl:if test="username=/response/user/username">&nbsp;(<a href="recommendation.html">edit</a>)</xsl:if> 
                    <xsl:if test="/response/user/username='admin'">&nbsp; (<a href="delete-recommendation.html">delete</a>)</xsl:if></p>
                
                <xsl:if test="comment[.!='']">
                    <div id="text{$posItem}trigger" onclick="switchMenu('text{$posItem}', 'arrow{$posItem}');" style="cursor: pointer;"><img id="arrow{$posItem}" src="{$staticprefix}images/arrowright.gif"/> <strong>View Comments</strong> </div><div id="text{$posItem}" style="display: none;" class="textSwitch">
                        <p><xsl:apply-templates select="comment" mode="copy"/>
                            <br/> <a href="report-recommendation.html?username={$rec-user}">Flag This Comment As Inappropriate</a></p>
                    </div>
                </xsl:if>
            </div>
        </xsl:for-each>
        
    </xsl:template>
    
    <xsl:template match="view[@type='recommendation'][@name='report-recommendation.html']" mode="formhelp">
        <p class="formhelp">To report this rating as inappropriate, please provide reasons in the box below as to why you believe it is inappropriate and should be removed. Thank you.</p>
        
        
    </xsl:template>
    
    <!-- Per Kyle, put some help on the Library grid screens -->
    <xsl:template
        match="view[@type='library'][@name='bysearchterms.html' or @name='byauthors.html' or @name='recentadded.html' or @name='byall.html']"
        mode="formhelp">
        <p class="formHelp">The ConserveOnline library is the place to put your finished products 
            when you want to give them the broadest possible distribution. The library is intended to be a 
            more formal and permanent archive than the ConserveOnline workspaces. All documents in 
            ConserveOnline are available for full-text searches; the library documents have additional 
            features that make them even easier for search engines to find. </p>
    </xsl:template>
    
    <xsl:template
        match="view[@type='libraryfile'][@name='add.html' or @name='edit.html']"
        mode="formhelp">
        <p class="formHelp">The ConserveOnline library is the place to put your finished products when you want to give them the broadest possible distribution. 
            The library is intended to be a more formal and permanent archive than the ConserveOnline workspaces. 
            All documents in ConserveOnline are available for full-text searches; the library documents have additional features that 
            make them even easier for search engines to find.</p>
        
    </xsl:template>  
</xsl:stylesheet>

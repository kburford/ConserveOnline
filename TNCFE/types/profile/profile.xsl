<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    <xsl:output indent="yes"/>
    <xsl:template match="view[@name='profile.html' and @type='profile']">
        <xsl:variable name="gv" select="document('../../shared/vocabularies.xml')/vocabularies"/>
        <xsl:variable name="countries" select="$gv/vocabulary[@id='countries']"/>
        <xsl:variable name="backgrounds" select="$gv/vocabulary[@id='backgrounds']"/>
        <xsl:variable name="organizationtypes" select="$gv/vocabulary[@id='organizationtypes']"/>
        <xsl:variable name="about" select="../profile/about"/>
        <div class="profileAboutContent">
            
            <div class="profileAboutLeft">
                <div class="profilePortrait">
                    <xsl:choose>
                        <xsl:when test="$about/portrait">
                            <img width="75px" height="99px" src="{$about/portrait/@href}"
                                alt="Profile Portrait"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <div id="profileNoPhoto">No photo provided</div>
                        </xsl:otherwise>
                    </xsl:choose>
                </div>
                <dl class="profileAboutListing">
                    <dt>Name :</dt>
                    <dd>
                        <xsl:value-of select="$about/firstname"/>&nbsp;<xsl:value-of
                            select="$about/lastname"/>
                        <xsl:if test="not($about/firstname) and not($about/lastname)"> &nbsp;
                        </xsl:if>
                    </dd>
                    <xsl:if test="$about/email">
                        <dt> E-mail :</dt>
                        <dd>
                            <xsl:value-of select="$about/email"/> &nbsp; </dd>
                    </xsl:if>
                    <dt>Region/Country :</dt>
                    <dd>
                        <xsl:value-of select="$countries/term[@id=$about/country]"/> &nbsp; </dd>
                    <dt>Background :</dt>
                    <dd>
                        <xsl:value-of select="$backgrounds/term[@id=$about/background]"/> &nbsp; </dd>
                    <dt>Organization :</dt>
                    <dd>
                        <xsl:value-of select="$about/organization"/> &nbsp; </dd>
                    <dt>Organization type:</dt>
                    <dd>
                        <xsl:value-of select="$organizationtypes/term[@id=$about/organizationtype]"
                        /> &nbsp; </dd>
                </dl> Member of Conserve Online since <xsl:apply-templates select="$about/joined"
                mode="monthdate"/><br/>
            </div>
        </div>
       

        <div id="profileBioText">
            <xsl:apply-templates select="../profile/about/bio/*" mode="copy"/>
            <xsl:if test="../profile/about/bio='' ">
                <span class="bioTextEmpty">*** Provide bio ***</span>
            </xsl:if>
        </div>

    </xsl:template>

    <xsl:template match="portlets[/response/view/@type='profile']">
        <div id="right">
            <xsl:for-each select="portlet">
                <div>
                    <xsl:apply-templates select="." mode="profileportlets"/>
                </div>
            </xsl:for-each>
        </div>
    </xsl:template>
    <!-- Another users profile -->
    <xsl:template match="portlet[1]" mode="profileportlets">
        <xsl:attribute name="class">box1 profilePortlet</xsl:attribute>
        <div class="header">
            <xsl:value-of select="@title"/>
        </div>
        <div class="content">
            <xsl:if test="not(resource)"> You have no invitations. </xsl:if>
            <ul class="resourceItems">
                <xsl:for-each select="resource">
                    <li>
                        <div>
                            <a>
                                <xsl:attribute name="href">
                                    <xsl:value-of select="@href"/>
                                </xsl:attribute><xsl:value-of select="title"/>
                            </a>
                        </div>
                        <div>
                            <xsl:apply-templates select="created"
                                mode="griddate"/>
                        </div>
                    </li>
                </xsl:for-each>
            </ul>
        </div>
    </xsl:template>
    
    <xsl:template match="portlet[2]" mode="profileportlets">
        <xsl:attribute name="class">box2 profilePortlet lastPortlet</xsl:attribute>
        <div class="header">
            <h1>
                <xsl:value-of select="@title"/>
            </h1>
        </div>
        <div class="content">
            <xsl:if test="@type='workspaces' ">
                <div id="workspaceKey">
                    <div id="managerIcon">Manager</div>
                    <div id="memberIcon">Member</div> &nbsp; </div>
            </xsl:if>
            <ul class="resourceItems">
                <xsl:for-each select="resource">
                    <li>
                        <xsl:attribute name="class">
                            <xsl:choose>
                                <xsl:when test="status='Manager'">managerItem</xsl:when>
                                <xsl:when test="status='Member'">memberItem</xsl:when>
                            </xsl:choose>
                        </xsl:attribute>
                        <div>
                            <a>
                                <xsl:attribute name="href">
                                    <xsl:value-of select="@href"/>
                                </xsl:attribute>
                                <xsl:value-of select="title"/>
                            </a>
                        </div>
                        <div> (Created <xsl:apply-templates select="created" mode="griddate"/>)
                        </div>
                    </li>
                </xsl:for-each>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="portlet/resource" mode="profileportlets">
        <ul class="resourceItems">
            <li>
                <xsl:attribute name="class">
                    <xsl:choose>
                        <xsl:when test="status='Manager'">managerItem</xsl:when>
                        <xsl:when test="status='Member'">memberItem</xsl:when>
                    </xsl:choose>
                </xsl:attribute>

                <xsl:if test="../@type='invitations' ">
                    <div>
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of select="@href"/>
                            </xsl:attribute> [<xsl:value-of select="title"/>]
                        </a>
                    </div>
                    <div>
                        <xsl:value-of select="manager"/>
                    </div>
                    <div>
                        <xsl:value-of select="created"/>
                    </div>
                </xsl:if>
                <xsl:if test="../@type='workspaces' ">
                    <div>
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of select="@href"/>
                            </xsl:attribute>
                            <xsl:value-of select="title"/>
                        </a>
                    </div>
                    <div> (Created <xsl:value-of select="created"/>) </div>
                </xsl:if>
            </li>
        </ul>
    </xsl:template>
</xsl:stylesheet>

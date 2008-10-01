<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    <xsl:output indent="yes"/>
    <xsl:template match="view[@name='view.html' and @type='topics']">
<p>Discussion board postings appear below and are available in two categories: <b>Most Popular Topics</b> displays the top 5 topics with the most posted replies while <b>All Topics</b> displays all topics alphabetically by topic title.</p>
        <table class="messageBoard content-listing" summary="" id="most-popular-topics">
            <thead>
                <tr>
                    <th colspan="3" class="mostPopularBoardHeader"> <b>Most Popular Topics</b></th>
                </tr>
                <tr>
                    <th style="width: 46%">Topic</th>
                    <th style="text-align:center">Replies</th>
                    <th style="width: 40%">Last Post</th>
                </tr>
            </thead>
            <tbody>
                <xsl:for-each select="../discussion/mostpopular/topic">
                    <tr>
                        <td>
                            <a href="{@href}">
                                <xsl:value-of select="title"/>
                            </a><br/>by <a href="{authorhref}">
                                <xsl:value-of select="author"/>
                            </a>
                        </td>
                        <td style="text-align:center">
                            <xsl:value-of select="replies"/>
                        </td>
                        <td>
                            <xsl:apply-templates select="lastcomment"/>
                        </td>
                    </tr>
                </xsl:for-each>
            </tbody>
        </table>

        <xsl:apply-templates select="../discussion/batch/pages"/>

        <table class="messageBoard content-listing" summary="" id="all-topics" >
            <thead>
                <tr>
                    <th colspan="3" class="boardHeader"> <b>All Topics</b> </th>
                </tr>
                <tr>
                    <th style="width: 46%">Topic</th>
                    <th style="text-align:center">Replies</th>
                    <th style="width: 40%">Last Post</th>
                </tr>
            </thead>
            <tbody>
                <xsl:for-each select="../discussion/batch/items/item">
                    <tr>
                        <td>
                            <a href="{@href}">
                                <xsl:value-of select="title"/>
                            </a><br/>by <a href="{authorhref}">
                                <xsl:value-of select="author"/>
                            </a>
                        </td>
                        <td style="text-align:center">
                            <xsl:value-of select="replies"/>
                        </td>
                        <td>
                            <xsl:apply-templates select="lastcomment"/>
                        </td>
                    </tr>
                </xsl:for-each>
                <xsl:if test="batch/pages">
                    <tr id="batch-row">
                        <td colspan="3">
                            <div class="pagination_box">
                                <xsl:apply-templates select="batch/pages"/>
                            </div>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>

        <xsl:apply-templates select="../discussion/batch/pages"/>

    </xsl:template>
    <xsl:template match="lastcomment">
        <xsl:apply-templates select="created" mode="bloglongform"/> by <a href="{author/@href}">
            <xsl:value-of select="author"/>
        </a>
    </xsl:template>

    <xsl:template name="split" match="@*" mode="split">
        <xsl:param name="string" select="string()"/>
        <xsl:variable name="break">
            <xsl:text>/</xsl:text>
        </xsl:variable>
        <xsl:variable name="cansplit" select="contains($string, $break)"/>
        <xsl:variable name="line">
            <xsl:value-of select="normalize-space($string)"/>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="$cansplit">
                <xsl:call-template name="split">
                    <xsl:with-param name="string" select="substring-after($string, $break)"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$line"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="view[@name='view.html' and @type='topic']">
        <div class="contentWrapper" id="topiv-view-wrapper">
	<xsl:choose>          
<xsl:when test="/response/user">
            <div class="reply">
                <a href="#reply">Reply</a>
            </div>
         </xsl:when>
         <xsl:otherwise>
		<div class="textCenter bold">
			You must <a href="{$urlprefix}login.html?came_from={/response/resource/@href}">log in</a> to post a comment.	    
		</div>
	</xsl:otherwise>
	</xsl:choose>
            <div class="topic_box">
                <strong>Posted by <a href="{../resource/author/@href}">
                        <xsl:value-of select="../resource/author"/>
                    </a> on <xsl:apply-templates select="../resource/modified" mode="bloglongform"/></strong>
                <xsl:apply-templates select="../resource/text" mode="copy"/>
            </div>
            <xsl:apply-templates select="../batch/pages"/>

            <xsl:for-each select="../batch/items/item">
                <xsl:variable name="id">
                    <xsl:apply-templates select="@href" mode="split"/>
                </xsl:variable>
                <div class="reply_box">
                    <xsl:if test="position() = last()">
                        <xsl:attribute name="style">border-bottom:none;</xsl:attribute>
                    </xsl:if>
                    <strong>Posted by <a href="{authorhref}">
                            <xsl:value-of select="author"/>
                        </a> on <xsl:apply-templates select="modified" mode="bloglongform"/></strong>
                    <div class="body">
                        <div class="reply">
                            <div>
                                <a href="{@href}">View</a>
                            </div>
                            <div>
                                <a href="{/response/resource/@href}?quoted={$id}#reply">Quote</a>
                            </div>
                        </div>
                        <p>
                            <xsl:apply-templates select="text" mode="copy"/>
                        </p>

                    </div>
                </div>
            </xsl:for-each>

            <xsl:apply-templates select="../batch/pages"/>
            <xsl:choose>
                <xsl:when test="/response/user">
                    <a name="reply"/>
                    <xsl:for-each select="quoted_reply">
                        <input type="hidden" name="quotedauthor" value="{author}"/>
                        <!--<input type="hidden" name="quotedtext" value="{rawbody/html:div}"/>-->
                        <div class="quotedreplyauthor">
                            <xsl:value-of select="author"/> wrote: </div>
                        <div class="quotedreplytext">
                            <xsl:apply-templates select="text" mode="copy"/>
                        </div>
                    </xsl:for-each>

                    <xsl:apply-templates select="../formcontroller">
                        <xsl:with-param name="layout">stacked</xsl:with-param>
                    </xsl:apply-templates>
                </xsl:when>
                <xsl:otherwise> 
                    <div class="textCenter bold">
                        You must <a href="{$urlprefix}login.html?came_from={/response/resource/@href}">log in</a> to post a comment. 
                    </div>                    
                </xsl:otherwise>
            </xsl:choose>



        </div>
    </xsl:template>

    <xsl:template match="view[@name='view.html' and @type='comment']">
        <div class="contentWrapper">
            <dl id="event-view-listing">
                <dt>Body</dt>
                <dd>
                    <xsl:apply-templates select="/response/resource/text/*" mode="copy"/>
                </dd>
            </dl>
        </div>
    </xsl:template>
</xsl:stylesheet>

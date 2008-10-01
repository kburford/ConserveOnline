<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:date="http://exslt.org/dates-and-times"
	exclude-result-prefixes="date" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:param name="staticprefix">/static/</xsl:param>
	<xsl:param name="urlprefix">/</xsl:param>
	<!-- 
	
	Common variables used in this XSLT and others
	
	-->
	<xsl:variable name="response" select="/response"/>
	<xsl:variable name="view" select="/response/view"/>
	<xsl:variable name="viewname" select="/response/view/@name"/>
	<xsl:variable name="viewtype" select="/response/view/@type"/>
	<!--     ****   End common variables   ****      -->
	<xsl:template match="*" mode="copy">
		<xsl:element name="{local-name()}">
			<!-- go process attributes and children -->
			<xsl:apply-templates select="@*|node()" mode="copy"/>
		</xsl:element>
	</xsl:template>
	<xsl:template match="@*" mode="copy">
		<xsl:attribute name="{local-name()}">
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>
	<xsl:template name="searchform">
		<form method="get">
			<xsl:choose>
				<xsl:when test="/response/workspace/@href">
					<xsl:attribute name="action">
						<xsl:value-of select="/response/workspace/@href"/>/search </xsl:attribute>
				</xsl:when>
				<xsl:when test="/response/searchquery/url">
					<xsl:attribute name="action">
						<xsl:value-of select="/response/searchquery/url"/>
					</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="action">/search</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<div class="boxSearch">
				<div id="title">
					<span class="searchLeft">Search</span>
				</div>
				<div id="searchForm">
					<select name="site">
						<optgroup label="ConserveOnline">
							<option value="ConserveOnline">All Sites</option>
							<option value="library">
								<xsl:if test="/response/searchquery/loclabel = 'Library' ">
									<xsl:attribute name="selected">selected</xsl:attribute>
								</xsl:if> Library </option>
							<option value="workspace">
								<xsl:if test="/response/searchquery/loclabel = 'All Workspaces' ">
									<xsl:attribute name="selected">selected</xsl:attribute>
								</xsl:if> All Workspaces </option>
							<xsl:if test="workspace">
								<option value="{/response/workspace/title}">
									<xsl:if
										test="/response/searchquery/loclabel = 'This Workspace' ">
										<xsl:attribute name="selected">selected</xsl:attribute>
									</xsl:if> This Workspace </option>
							</xsl:if>
						</optgroup>
						<optgroup label="External Sites">
							<option value="ConservationWebsites">
								<xsl:if
									test="/response/searchquery/loclabel = 'ConservationWebsites' ">
									<xsl:attribute name="selected">selected</xsl:attribute>
								</xsl:if> Conservation Sites </option>
							<option value="GIS">
								<xsl:if
									test="/response/searchquery/loclabel = 'GIS' ">
									<xsl:attribute name="selected">selected</xsl:attribute>
								</xsl:if> GIS Portal Content </option>
						</optgroup>
					</select>
					<input type="text" name="q" value="{/response/searchquery/terms}"/>
					<input type="image" src="{$staticprefix}images/btnGoGreen.gif" name="image"
						class="button"/>
				</div>
			</div>
		</form>
	</xsl:template>
	<!--	
	XXX This looks like it is no longer used.
	<xsl:template match="@type" mode="icon">
		<xsl:variable name="icon">
			<xsl:choose>
				<xsl:when test=". = 'pdf'">pdf</xsl:when>
				<xsl:otherwise>unknown</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<img src="{$urlprefix}images/{$icon}.png" alt="." height="16" width="16"/>
	</xsl:template>
-->
	<xsl:template match="menu[@id='section']">
		<div id="navigation">
			<ul id="tabs">
				<xsl:apply-templates select="item"/>
			</ul>
		</div>
	</xsl:template>
	<xsl:template match="response/messages">
		<div>
			<xsl:choose>
				<xsl:when test="/response/view/@name = 'manage-members.html'">
					<xsl:attribute name="class">displayNone</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="class">formError</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<!-- Might be multiple message values, iterate and 
			show them all.
			-->
			<xsl:for-each select="message">
				<div>
					<xsl:value-of select="."/>
				</div>
			</xsl:for-each>
		</div>
	</xsl:template>
	<xsl:template match="view/@titlexpath">
		<h2 class="documentFirstHeading">
			<xsl:value-of select="."/>
		</h2>
	</xsl:template>
	<xsl:template match="batch">
		<!--  Top pagination -->
		<xsl:apply-templates select="letters"/>
		<xsl:apply-templates select="pages"/>
		<table class="content-listing">
			<xsl:if test="count(cols/col) &lt; 4">
				<xsl:attribute name="id">narrow-table</xsl:attribute>
			</xsl:if>
			<thead>
				<xsl:apply-templates select="cols"/>
			</thead>
			<tbody>
				<xsl:apply-templates select="items"/>
				<xsl:if test="not(items)">
					<tr class="odd">
						<xsl:for-each select="cols/col">
							<xsl:choose>
								<xsl:when test="position() = 1">
									<td>
										<em>No values found.</em>
									</td>
								</xsl:when>
								<xsl:otherwise>
									<td>&nbsp;</td>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:for-each>
					</tr>
				</xsl:if>
			</tbody>
		</table>

		<!--  Bottom pagination -->
		<xsl:apply-templates select="pages"/>
		

	</xsl:template>
	<xsl:template match="pages">
		<xsl:variable name="currentPage" select="page[@current]"/>
		<xsl:variable name="lastPage" select="page[last()]"/>
		<xsl:variable name="lastViewablePage">
			<xsl:value-of select="$currentPage - 3"/>
		</xsl:variable>
		<xsl:variable name="firstViewablePage">
			<xsl:value-of select="$currentPage + 3"/>
		</xsl:variable>
		<xsl:if test="count(page) > 1">
			<div class="kpagination_frame">
				<div class="kpagination_pages">
					<!-- Display previous link if current page is not the first-->
					<a href="{descendant::page[1]/@href}">First Page</a> | 
					<xsl:for-each select="page[$currentPage - 1]">
						<xsl:if test="$currentPage > 1">
							<a href="{@href}" class="arrowRight">
								<img src="{$staticprefix}images/arrow_back.gif" alt="Previous"
									title="Previous"/> Previous </a> | </xsl:if>
					</xsl:for-each>
					<xsl:apply-templates
						select="page[ position() >= $lastViewablePage and position() &lt;= $firstViewablePage]"/>
					<!-- Display next link if current page is not the last-->
					<xsl:for-each select="page[$currentPage + 1]">
						<xsl:if test="$lastPage > $currentPage"> | <a href="{@href}"
								class="arrowRight"> Next <img src="{$staticprefix}images/arrow.gif"
									alt="Next" title="Next"/>
							</a>
						</xsl:if>
					</xsl:for-each> | 
					<a href="{descendant::page[last()]/@href}">Last Page</a>
				</div>
				
				<div class="kpagination_totals"> 
					<xsl:apply-templates select="/response/batch/pagesize"/> |
					Showing <xsl:value-of select="../@start"/> -
						<xsl:value-of select="../@end"/> of <xsl:value-of select="../@total"/>
					listings
				
				</div> 
			</div>
		</xsl:if>
		
	</xsl:template>

	<xsl:template match="page">
		<xsl:choose>
			<xsl:when test="@current">
				<strong>
					<xsl:value-of select="."/>
				</strong>
			</xsl:when>
			<xsl:otherwise>
				<a href="{@href}" title="">
					<span>
						<xsl:value-of select="."/>
					</span>
				</a>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="position() != last()"> | </xsl:if>
	</xsl:template>
	<xsl:template match="cols">
		<tr>
			<!-- Make columns in THEAD -->
			<xsl:apply-templates select="col"/>
		</tr>
	</xsl:template>
	<xsl:template match="col">
		<th>
			<xsl:attribute name="class">cl<xsl:value-of select="@id"/></xsl:attribute>
			<a href="" title="">
				<xsl:attribute name="href">
					<xsl:value-of select="@href"/>
				</xsl:attribute>
				<xsl:attribute name="title">
					<!-- We need to have appropriate title attr, explaining what can be done with this link -->
					<xsl:choose>
						<xsl:when test="@dir = 'asc'"> Sort descending on <xsl:value-of select="."/></xsl:when>
						<xsl:otherwise> Sort ascending on <xsl:value-of select="."/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:value-of select="."/>
				<xsl:choose>
					<xsl:when test="@dir = 'asc'">
						<!-- Show arrow up in case of ascending sorting on this column -->
						<span class="arrowUp">&#x25BC;</span>
					</xsl:when>
					<xsl:when test="@dir = 'desc'">
						<!-- Show arrow down in case of descending sorting on this column -->
						<span class="arrowDown">&#x25B2;</span>
					</xsl:when>
				</xsl:choose>
			</a>
		</th>
	</xsl:template>
	<xsl:template match="items">
		<xsl:variable name="gv" select="document('../shared/vocabularies.xml')/vocabularies"/>
		<xsl:for-each select="item">
			<tr>
				<xsl:attribute name="class">
					<xsl:choose>
						<xsl:when test="position() mod 2 = 1">odd</xsl:when>
						<xsl:otherwise>even</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>

				<!-- Make row for each item -->
				<xsl:apply-templates select=".">
					<xsl:with-param name="gv" select="$gv"/>
				</xsl:apply-templates>
			</tr>
		</xsl:for-each>
	</xsl:template>


	<xsl:template match="letters">
		<p align="center">
			<xsl:for-each select="letter">
				<xsl:choose>
					<xsl:when test="@current">
						<span class="alpha-menu-select">
							<xsl:value-of select="."/>
						</span>
					</xsl:when>
					<xsl:otherwise>
						<a href="{@href}">
							<xsl:value-of select="."/>
						</a>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:if test="position() != last()"> | </xsl:if>
			</xsl:for-each>
		</p>
	</xsl:template>
	
	<xsl:template match="pagesize">
		<span>
			Items per page: 
			<xsl:for-each select="size">
				<xsl:choose>
					<xsl:when test="@current">
						<strong>
							<xsl:value-of select="."/>
						</strong>
					</xsl:when>
					<xsl:otherwise>
						<a href="{@href}">
							<xsl:value-of select="."/>
						</a>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:if test="position() != last()">, </xsl:if>
			</xsl:for-each>
		</span>
	</xsl:template>

	<xsl:template match="items/item">
		<xsl:param name="gv"/>
		<xsl:variable name="thisitem" select="."/>
		<!-- We get item and iterate over columns to show only information that is needed accordig to columns -->
		<xsl:for-each select="../../cols/col/@id">
			<xsl:variable name="thischild" select="$thisitem/*[name()=current()]"/>
			<td>
				<xsl:attribute name="class">cl<xsl:value-of select="."/></xsl:attribute>
				<xsl:choose>
					<xsl:when test=". = 'title'">
						<!-- Show an icon when available -->
						<xsl:apply-templates select="$thisitem/mimetype"/>
						<a href="{$thisitem/@href}" title="{$thischild}">
							<xsl:apply-templates select="$thischild"/>
						</a>
					</xsl:when>
					<xsl:when test=". = 'type'">
						<a href="{$thisitem/@href}" title="{$thischild}">
							<xsl:apply-templates select="$thischild"/>
						</a>
					</xsl:when>
					<xsl:when test=". = 'date' or . = 'dateupdated'">
						<xsl:apply-templates select="$thischild" mode="griddate"/>
					</xsl:when>
					<xsl:when test="position() = 1">
						<a href="{$thisitem/@href}" title="{$thischild}">
							<xsl:value-of select="$thischild"/>
						</a>
					</xsl:when>
					<xsl:when test=". = 'size'">
						<xsl:apply-templates select="$thischild"/>
					</xsl:when>
					<xsl:when test=". = 'count'">
						<xsl:apply-templates select="$thischild"/>
					</xsl:when>
					<xsl:when test=". = 'mimetype'">
						<xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
						<xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
						<xsl:value-of select="translate($thischild,$lcletters,$ucletters)"/>
					</xsl:when>
					<xsl:when test=". = 'country'">
						<xsl:variable name="countries" select="$gv/vocabulary[@id='countries']"/>
						<xsl:value-of select="$countries/term[@id=$thischild]"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$thischild"/>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="mimetype">
		<xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
		<xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
		<img class="fileIcon" src="{$staticprefix}images/{translate(.,$ucletters,$lcletters)}.png"
			alt="" height="16" width="16"/>
	</xsl:template>
	<xsl:template match="mimetype" mode="viewFile">
		<xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
		<xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>
		<img src="{$staticprefix}images/{translate(.,$ucletters,$lcletters)}.png" alt="" height="16"
			width="16"/>
	</xsl:template>

	<xsl:template match="breadcrumbs">
		<div id="breadcrumbs">
			<span>You are here:</span>&nbsp; <xsl:apply-templates select="entry"/>
		</div>
	</xsl:template>
	<xsl:template match="breadcrumbs/entry[not(@href)]">
		<strong>
			<xsl:value-of select="."/>
		</strong>
	</xsl:template>
	<xsl:template match="breadcrumbs/entry[@href]">
		<a href="{@href}">
			<xsl:value-of select="."/>
		</a> &#x2192; </xsl:template>
	<xsl:template match="addmenu|actionmenu" mode="menus">
		<!-- Actions menu at the top right corner of the content area -->
		<div class="chactions">
			<ul class="actionsbar">
				<xsl:attribute name="class">
					<xsl:choose>
						<!-- we need additional class if there are not enough actions to show dropdown menu, dropping to the right -->
						<xsl:when test="count(menu[@id='actionmenu']/item) &lt; 2">actionsbar
							lastDropdown</xsl:when>
						<xsl:otherwise>actionsbar</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<!-- Menu items. We should avoid 'Folder' item in case current workspace doesn't contain any folders (@hasfolders on workspace does not exist) -->
				<xsl:apply-templates select="entry" mode="menus"/>
			</ul>
		</div>
	</xsl:template>
	<xsl:template match="utilitymenu" mode="menus">
		<ul class="utilityLinks">
			<li>
				<xsl:apply-templates select="@label"/>
			</li>
			<!-- Menu items. We should avoid 'Folder' item in case current 
				workspace doesn't contain any folders (@hasfolders on workspace does not exist) -->
			<xsl:apply-templates
				select="entry[not(. = 'Folder' and not($response/workspace/@hasfolders))]"
				mode="menus"/>
		</ul>
	</xsl:template>
	<xsl:template match="entry" mode="menus">
		<li class="utilityItem">
			<xsl:attribute name="class">
				<xsl:choose>
					<xsl:when test="position() = last()">utilityItem lastItem</xsl:when>
					<xsl:when test="@label">
						<xsl:if test="$response/view/@section=@label">utilityItem active</xsl:if>
					</xsl:when>
					<xsl:otherwise>utilityItem</xsl:otherwise>
				</xsl:choose>
			</xsl:attribute>
			<xsl:choose>
				<xsl:when test="@current">
					<!-- If this utility link is the current one, then
						don't make it an anchor.
					-->
					<strong>
						<xsl:attribute name="class">
							<xsl:if test="position() = 1 and not(../@label)">firstItem</xsl:if>
						</xsl:attribute>
						<xsl:value-of select="."/>
					</strong>
				</xsl:when>
				<xsl:otherwise>
					<a href="{@href}" title="{.}">
						<xsl:attribute name="class">
							<xsl:if test="position() = 1 and not(../@label)">firstItem</xsl:if>
						</xsl:attribute>
						<xsl:choose>
							<xsl:when test="name(..) = 'utilitymenu'">
								<xsl:value-of select="."/>
							</xsl:when>
							<xsl:otherwise>
								<span>
									<xsl:value-of select="."/>
								</span>
							</xsl:otherwise>
						</xsl:choose>
					</a>
				</xsl:otherwise>
			</xsl:choose>
		</li>
	</xsl:template>
	<xsl:template match="*" mode="monthdate">
		<!-- January 21, 2007 for example -->
		<xsl:value-of select="date:month-name(.)"/>&#160;<xsl:value-of
			select="date:day-in-month(.)"/>, <xsl:value-of select="date:year(.)"/>
	</xsl:template>
	<xsl:template match="*" mode="griddate">
		<!-- 5/22/2007 for example -->
		<xsl:value-of select="date:month-in-year(.)"/>/<xsl:value-of select="date:day-in-month(.)"
			/>/<xsl:value-of select="date:year(.)"/>
	</xsl:template>
	<xsl:template match="created|modified|last_activity|startDate|endDate" mode="bloglongform">
		<xsl:value-of select="date:day-name(.)"/>, <xsl:value-of select="date:month-name(.)"
			/>&#160;<xsl:value-of select="date:day-in-month(.)"/>, <xsl:value-of
			select="date:year(.)"/>
		<span style="padding-left:5px;padding-right:2px">
			<xsl:choose>
				<xsl:when test="date:hour-in-day(.) = 0">0<xsl:value-of select="date:hour-in-day(.)"
					/></xsl:when>
				<xsl:when test="date:hour-in-day(.) > 12">
					<xsl:value-of select="date:hour-in-day(.) - 12"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="date:hour-in-day(.)"/>
				</xsl:otherwise>
			</xsl:choose>:<xsl:choose>
				<xsl:when test="date:minute-in-hour(.) &lt; 10">0<xsl:value-of
						select="date:minute-in-hour(.)"/></xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="date:minute-in-hour(.)"/>
				</xsl:otherwise>
			</xsl:choose>
		</span>
		<xsl:choose>
			<xsl:when test="date:hour-in-day(.)&gt;11">PM</xsl:when>
			<xsl:otherwise>AM</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="resource/attachments/attachment">
		<div class="fileDownload">
			<xsl:apply-templates select="/response/resource/mimetype" mode="viewFile"/> &nbsp;<a
				href="{./@href}">View This File</a> (<xsl:apply-templates
				select="/response/resource/size"/>)  
			<xsl:choose>
				<xsl:when test="(/response/view/@name='view.html' and /response/view/@type='libraryfile')">
					
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
					<span> &nbsp; &nbsp;
						<img src="{$staticprefix}images/stars_{$star-img}.gif" alt="{$star-count}"></img>  (<xsl:value-of select="/response/ratings/count"/> Rating<xsl:if test="/response/ratings/count != '1'">s</xsl:if>) <a href="recommendation.html">Add A Rating</a> 
						<xsl:if test="/response/ratings/count != '0'"> |  <a href="view-recommendations.html">View All Ratings</a></xsl:if>
						
					</span>
					
					<xsl:if test="/response/resource/is_private='true'">
						<span class="textPrivate">** This document is private **</span>
					</xsl:if>			
					
					<br/>
					
					
					<span>		<!-- AddThis Button BEGIN -->
						<script type="text/javascript">addthis_pub  = 'ConserveOnline';</script>
						<a href="http://www.addthis.com/bookmark.php" onmouseover="return addthis_open(this, '', '[URL]', '[TITLE]')" onmouseout="addthis_close()" onclick="return addthis_sendto()"><img src="http://s9.addthis.com/button1-bm.gif" width="125" height="16" border="0" alt="" /></a><script type="text/javascript" src="http://s7.addthis.com/js/152/addthis_widget.js"></script>
						<!-- AddThis Button END -->
						
						(<a
							href="{$staticprefix}html/social_bookmarking.html"
							onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
							return false;">What's This?</a>)
					</span>
				</xsl:when>
				<xsl:otherwise> &nbsp; &nbsp;
					
					<span>		<!-- AddThis Button BEGIN -->
						<script type="text/javascript">addthis_pub  = 'ConserveOnline';</script>
						<a href="http://www.addthis.com/bookmark.php" onmouseover="return addthis_open(this, '', '[URL]', '[TITLE]')" onmouseout="addthis_close()" onclick="return addthis_sendto()"><img src="http://s9.addthis.com/button1-bm.gif" width="125" height="16" border="0" alt="" /></a><script type="text/javascript" src="http://s7.addthis.com/js/152/addthis_widget.js"></script>
						<!-- AddThis Button END -->
						
						(<a
							href="{$staticprefix}html/social_bookmarking.html"
							onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
							return false;">What's This?</a>)
					</span>
					
					<xsl:if test="/response/resource/is_private='true'">
						<span class="textPrivate">** This document is private **</span>
					</xsl:if>			
					
					<br/>
					
					
					
					
				</xsl:otherwise>
				
				
			</xsl:choose>
			
			
		
		</div>
		
	</xsl:template>

	<xsl:template match="size">
		<xsl:choose>
			<xsl:when test="../mimetype = 'Folder'"> N/A </xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/> Kb</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="resource" mode="vocabitemsview">
		<!-- We only match on this when there is no child -->
		<!-- XXX After Nov 28 refactoring, this shouldn't get called -->
		<em>None selected.</em>
	</xsl:template>
	<xsl:template match="resource/*" mode="vocabitemsview">
		<!-- Iterate over the current values and convert to full labels on vocab entries -->
		<xsl:param name="thisvocab"/>
		<xsl:choose>
			<xsl:when test="item">
				<xsl:for-each select="item">
					<span>
						<xsl:value-of select="$thisvocab/term[@id=current()]"/>
					</span>
					<xsl:if test="position() != last()">; </xsl:if>
				</xsl:for-each>
			</xsl:when>
			<xsl:otherwise>
				<em>None selected.</em>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="resource/*" mode="vocabvalueview">
		<!-- Iterate over the current values and convert to full labels on vocab entries -->
		<xsl:param name="thisvocab"/>
		<xsl:choose>
			<xsl:when test="$thisvocab/term[@id=current()]">
				<span>
					<xsl:value-of select="$thisvocab/term[@id=current()]"/>
				</span>
			</xsl:when>
			<xsl:when test="text()">
				<span>
					<xsl:value-of select="."/> (<em>Bad vocab value.</em>) </span>
			</xsl:when>
			<xsl:otherwise>
				<em>None selected.</em>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="resource" mode="taxonomytable">
		<xsl:variable name="gv" select="document('../shared/vocabularies.xml')/vocabularies"/>

		<!-- XXX Kyle -->
		<table class="colTaxonomyTable" border="0" cellspacing="5" cellpadding="5" width="95%"
			align="center">
			<tr>
				<td valign="top" width="50%">
					<!-- This is the left hand column -->
					<table class="colTaxonomyTable" border="0" cellspacing="5" cellpadding="5"
						width="95%">
						<xsl:if test="$viewtype[.='libraryfile' or .='file']">
							<tr>
								<td valign="top" width="30%">Author(s):</td>
								<td>
									<xsl:choose>
										<xsl:when test="authors/item">
											<div class="taxonomy-values">
												<xsl:for-each select="authors/item">
												<span>
												<xsl:value-of select="."/>
												</span>
												<xsl:if test="position() != last()">; </xsl:if>
												</xsl:for-each>
											</div>
										</xsl:when>
										<xsl:otherwise>
											<em>None assigned.</em>
										</xsl:otherwise>
									</xsl:choose>
								</td>
							</tr>
							<tr>
								<td valign="top" width="30%" nowrap="true">Date Authored:</td>
								<td>
									<xsl:choose>
										<xsl:when test="dateauthored/text()">
											<xsl:apply-templates select="dateauthored"
												mode="griddate"/>
										</xsl:when>
										<xsl:otherwise>
											<em>None given.</em>
										</xsl:otherwise>
									</xsl:choose>
								</td>
							</tr>
							<tr>
								<td valign="top" width="30%" nowrap="true">Contribution Date:</td>
								<td>
									<xsl:choose>
										<xsl:when test="/response/resource/creation_date/text()">
											<xsl:apply-templates select="creation_date"
												mode="griddate"/>
										</xsl:when>
										<xsl:otherwise>
											<em>None given.</em>
										</xsl:otherwise>
									</xsl:choose>
								</td>
							</tr>
							<tr>
								<td valign="top" width="30%" nowrap="true">Document Purpose(s):</td>
								<td>
									<xsl:choose>
										<xsl:when test="not(document_type)">
											<em>None selected.</em>
										</xsl:when>
										<xsl:otherwise>
											<div class="taxonomy-values">
												<xsl:apply-templates select="document_type"
												mode="vocabitemsview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='documenttypes']"
												/>
												</xsl:apply-templates>
											</div>
										</xsl:otherwise>
									</xsl:choose>
								</td>
							</tr>
						</xsl:if>

						<tr>
							<td valign="top" width="30%">Language:</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(language)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="language"
												mode="vocabvalueview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='languages']"/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%">Region/Country:</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(country)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="country"
												mode="vocabvalueview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='countries']"/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%">Realm:</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(biogeographic_realm)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="biogeographic_realm"
												mode="vocabvalueview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='biogeographic_realms']"
												/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%">Habitat(s):</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(habitat)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="habitat"
												mode="vocabitemsview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='habitats']"/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%">License:</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(license)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="license"
												mode="vocabvalueview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='licenses']"/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
					</table>
				</td>
				<td valign="top" width="50%">
					<!-- This is the right hand column -->
					<table class="colTaxonomyTable" border="0" cellspacing="5" cellpadding="5"
						width="95%">
						<tr>
							<td valign="top" width="30%" nowrap="true">Conservation Action(s):</td>
							<td>
								<xsl:apply-templates
									select="conservation|../resource[not(conservation)]"
									mode="vocabitemsview">
									<xsl:with-param name="thisvocab"
										select="$gv/vocabulary[@id='conservation']"/>
								</xsl:apply-templates>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%" nowrap="true">Direct Threat(s):</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(directthreat)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="directthreat"
												mode="vocabitemsview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='directthreat']"/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%">Organization:</td>
							<td>
								<xsl:choose>
									<xsl:when test="organization/text()">
										<div class="taxonomy-values">
											<xsl:value-of select="organization"/>
										</div>
									</xsl:when>
									<xsl:otherwise>
										<em>None given.</em>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<tr>
							<td valign="top" width="30%">Monitoring:</td>
							<td>
								<xsl:choose>
									<xsl:when test="not(monitoring)">
										<em>None selected.</em>
									</xsl:when>
									<xsl:otherwise>
										<div class="taxonomy-values">
											<xsl:apply-templates select="monitoring"
												mode="vocabitemsview">
												<xsl:with-param name="thisvocab"
												select="$gv/vocabulary[@id='monitoring']"/>
											</xsl:apply-templates>
										</div>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<!--- keywords/item now refer to Search Terms 01.08.08 -->
						<tr>
							<td valign="top" width="30%" nowrap="true">Other Search Terms(s):</td>
							<td>
								<xsl:choose>
									<xsl:when test="keywords/item">
										<div class="taxonomy-values">
											<xsl:for-each select="keywords/item">
												<xsl:value-of select="."/>
												<xsl:if test="position() != last()">; </xsl:if>
											</xsl:for-each>
										</div>
									</xsl:when>
									<xsl:otherwise>
										<em>None used.</em>
									</xsl:otherwise>
								</xsl:choose>
							</td>
						</tr>
						<xsl:if
							test="/response/view/@type = 'file' or /response/view/@type = 'libraryfile' ">
							<tr>
								<td valign="top" width="30%">DOI:</td>
								<td>
									<xsl:choose>
										<xsl:when test="oid/text()">
											<span>
												<xsl:value-of select="oid"/>
											</span>
										</xsl:when>
										<xsl:otherwise>
											<em>Not assigned.</em>
										</xsl:otherwise>
									</xsl:choose>
								</td>
							</tr>

						</xsl:if>
					</table>
				</td>
			</tr>
		</table>



	</xsl:template>

	<xsl:template match="/response/resource/description">
		<div id="abstract-wrapper">
			<h2>Abstract</h2>
			<xsl:value-of select="."/>
		</div>
	</xsl:template>

	<xsl:template match="resource/gisdata">
		<div class="fileDownload">
			<xsl:apply-templates select="/response/resource/GIS-metadata" mode="viewFile"/>
				&nbsp;<a href="{./@href}" target="_blank">View GIS Metadata</a>
		</div>
	</xsl:template>
	
	<xsl:template name="rss-helper">
		<div>
			
			<p><strong>What Is RSS</strong></p>
			<p><a href="http://en.wikipedia.org/wiki/RSS_(file_format)" target="_blank">RSS</a> stands for  "Really Simple Syndication" , and is an XML format that was created to syndicate news, and be a means to 
				share content on the web. Essentially, RSS is a way online for you to get a quick list of the latest story headlines from all your favorite websites and blogs all in one place.</p>
			<p>Suppose you have 50 sites and blogs that you like to visit regularly. Going to visit each website and blog everyday could take you hours. With RSS, you can “subscribe” to a website or blog, 
			and get “fed” all the new headlines from all of these 50 sites and blogs in one list, and see what’s going on in minutes instead of hours. What a time saver! </p>
			
		<p><strong>How do I subscribe to an RSS feed?</strong></p>
			<p>My web browser is:</p>
			<div class="rss-help">
				<p><div id="text1trigger" onclick="switchMenu('text1', 'arrow1');" style="cursor: pointer;"><img id="arrow1" src="{$staticprefix}images/arrowright.gif"/> Internet Explorer 6 </div></p>
				<div id="text1" style="display: none;" class="textSwitch">
					<p>
						You can not use Internet Explorer 6.0 to view RSS feeds.  You can:
						<ol>
							<li><a href="http://www.microsoft.com/windows/downloads/ie/getitnow.mspx" target="_blank">Download Internet Explorer 7.0</a></li>
							<li> <a
								href="{$staticprefix}html/rss_readers_popup.html"
								onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
								return false;">Download a separate program to view RSS feeds</a></li>
						</ol>
						
					</p>
				</div>
				
				<p><div id="rss-help" onclick="switchMenu('text2', 'arrow2');" style="cursor: pointer;"><img id="arrow2" src="{$staticprefix}images/arrowright.gif"/> Internet Explorer 7</div></p>
				<div id="text2" style="display: none;" class="textSwitch">
					<p>
						<ol>
							<li>Click any link that displays a RSS icon next to it (<img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
							title="Get RSS"/>)</li>
							<li>Click on “Subscribe to this feed” on the page that appears</li>
							<li>A popup will appear.  Name the subscription something you will remember, like “ConserveOnline Feed” and press the Subscribe button. </li>
							<li>You can view your RSS feeds from the little gold star in the upper left-hand corner of the browser window (<a
								href="{$staticprefix}html/rss_ie7.html"
								onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
								return false;">View</a>)</li>
						</ol>
	
						
						
					</p>
				</div>
				
				<p><div id="text3trigger" onclick="switchMenu('text3', 'arrow3');" style="cursor: pointer;"><img id="arrow3" src="{$staticprefix}images/arrowright.gif"/> Firefox 2 / 3</div></p>
				<div id="text3" style="display: none;" class="textSwitch">
					<p>
						<ol>
							<li>Click any link that displays a RSS icon next to it (<img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
								title="Get RSS"/>)</li>
							<li>Click on “Subscribe to this feed” on the page that appears</li>
							<li>A page will appear.  Press the “Subscribe Now” button.  Name the subscription something you will remember like “ConserveOnline Feed” and press the OK button.</li>
							<li>You can view your RSS feed from the browser shortcuts bar or under the Favorites Menu  --> Bookmarks Toolbar Folder (<a
								href="{$staticprefix}html/rss_ff3.html"
								onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
								return false;">View</a>)</li>
						</ol>
						
			
						
					</p>
				</div>
				
				<p><div id="text4trigger" onclick="switchMenu('text4', 'arrow4');" style="cursor: pointer;"><img id="arrow4" src="{$staticprefix}images/arrowright.gif"/> Safari 3</div></p>
				<div id="text4" style="display: none;" class="textSwitch">
					<p>
						<ol>
							<li>Click any link that displays a RSS icon next to it (<img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
								title="Get RSS"/>)</li>
							<li>A reformatted feed page appears that displays all the feeds for that RSS selection</li>
							<li>Click "Add Bookmark" from the Bookmark toolbar option or simply drag the URL in the location window to the Bookmarks Bar.  Name the subscription something you will remember like “ConserveOnline Feed”.</li>
							<li>You can view your RSS feed from the Bookmarks bar or under the Bookmarks Menu --> Bookmarks Bar Folder (<a
								href="{$staticprefix}html/rss_safari3.html"
								onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
								return false;">View</a>)</li>
						</ol>
						
						
						
					</p>
				</div>
			</div>
		</div>
	</xsl:template>



</xsl:stylesheet>

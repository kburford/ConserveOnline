<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet version="1.0" xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:import href="commontemplates.xsl"/>
	<xsl:import href="sitecatalyst.xsl"/>
	<xsl:import href="genericviews.xsl"/>
	<xsl:output method="xml" encoding="utf-8"
		doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
		doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"/>
	<xsl:template match="response">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
				<title>
					ConserveOnline | <xsl:value-of select="view/@title"/>
				</title>
				
				
				<xsl:choose>
					<xsl:when test="not(/response/breadcrumbs/base)">	
						<base href="{breadcrumbs/entry[1]/@href}"/>
					</xsl:when>
					<xsl:otherwise>
						<base href="{breadcrumbs/base}"/>
					</xsl:otherwise>
				</xsl:choose>
				
				
				<!--- Adding meta descriptions  06048-->
				
				<xsl:if test="view/@type='colhome'">
					<meta name="description" content="ConserveOnline is a one-stop online, public library, created and maintained by The Nature Conservancy in partnership with other conservation organizations. The library makes conservation tools, techniques, and experience available to a broad community of conservation practitioners" />
					<meta name="keywords" content="conservation action plan, threats, habitat, ecological community, species, protected, ecoregional, ecotourism, riparian, vegetation, 5 s, cinco s, corridor, connectivity, carbon, extinction, GIS, geographic information system, remote sensing, biodiversity"/>
				</xsl:if>
				
				<xsl:if test="resource/type/@title='Page'">
					<meta name="description" content="ConserveOnline is a one-stop online, public library, created and maintained by The Nature Conservancy in partnership with other conservation organizations. The library makes conservation tools, techniques, and experience available to a broad community of conservation practitioners" />
					<meta name="keywords" content="conservation action plan, threats, habitat, ecological community, species, protected, ecoregional, ecotourism, riparian, vegetation, 5 s, cinco s, corridor, connectivity, carbon, extinction, GIS, geographic information system, remote sensing, biodiversity"/>
				</xsl:if>
				
				<xsl:if test="view/@type='workspace'">
					<xsl:variable name="ws-kw">
						<xsl:choose>
							<xsl:when test="workspacekeywords/keyword">
									<xsl:for-each select="workspacekeywords/keyword/title">
										<span>
											<xsl:value-of select="."/>
										</span>
										<xsl:if test="position() != last()">, </xsl:if>
									</xsl:for-each>
									
							</xsl:when>
							<xsl:otherwise>
								conservation action plan, threats, habitat, ecological community, species, protected, ecoregional, ecotourism, riparian, vegetation, 5 s, cinco s, corridor, connectivity, carbon, extinction, GIS, geographic information system, remote sensing, biodiversity
							</xsl:otherwise>
						</xsl:choose>
					</xsl:variable>
					
					<meta name="description" content="Workspace-ConserveOnline: {view/@title}"/>
					<meta name="keywords" content="{$ws-kw}"/>
					
				</xsl:if>
				
				<xsl:if test="(resource/type/@title='COLFile') or (resource/type/@title='COLPage')">
					
					<xsl:variable name="doc-kw">
						<xsl:choose>
							<xsl:when test="currentkeywords/item">
								<xsl:for-each select="currentkeywords/item">
									<span>
										<xsl:value-of select="."/>
									</span>
									<xsl:if test="position() != last()">, </xsl:if>
								</xsl:for-each>
								
							</xsl:when>
							<xsl:otherwise>
								conservation action plan, threats, habitat, ecological community, species, protected, ecoregional, ecotourism, riparian, vegetation, 5 s, cinco s, corridor, connectivity, carbon, extinction, GIS, geographic information system, remote sensing, biodiversity
							</xsl:otherwise>
						</xsl:choose>
					</xsl:variable>
					
					<meta name="description" content="ConserveOnline: {workspace/title}: {view/@title}"/>
					<meta name="keywords" content="{$doc-kw}"/>
				</xsl:if>
				
				<xsl:if test="resource/type/@title='LibraryFile'">
					<xsl:variable name="lib-kw">
						<xsl:choose>
							<xsl:when test="resource/keywords/item">
								<xsl:for-each select="resource/keywords/item">
									<span>
										<xsl:value-of select="."/>
									</span>
									<xsl:if test="position() != last()">, </xsl:if>
								</xsl:for-each>
								
							</xsl:when>
							<xsl:otherwise>
								conservation action plan, threats, habitat, ecological community, species, protected, ecoregional, ecotourism, riparian, vegetation, 5 s, cinco s, corridor, connectivity, carbon, extinction, GIS, geographic information system, remote sensing, biodiversity
							</xsl:otherwise>
						</xsl:choose>
					</xsl:variable>
					
					<meta name="description" content="ConserveOnline: {resource/title}"/>
					<meta name="keywords" content="{$lib-kw}"/>
				</xsl:if>
				
				
				
				
				<xsl:if test="formcontroller">
					<!-- Help speedup base2 JS scanning by setting a flag that 
					lets widgets know if we're on a form, and if so, for what type. -->
					<meta content="{view/@type}" name="formcontroller"/>
				</xsl:if>
				<link rel="shortcut icon" href="{$staticprefix}images/favicon.ico" type="image/x-icon" />
				
				<link href="{$staticprefix}css/reset.css" rel="stylesheet" type="text/css"
					media="all"/>
				<link href="{$staticprefix}css/tnc.css" rel="stylesheet" type="text/css" media="all"/>
				<link rel="stylesheet" href="{$staticprefix}css/tncStyles.css" type="text/css"
					media="all"/>
				
				<xsl:comment xml:space="preserve">[if IE]>
					&lt;style type="text/css" &gt; @import url("<xsl:value-of select="$staticprefix"/>css/ie_hacks.css"); &lt;/style&gt; 
					&lt;![endif]</xsl:comment>

				<script type="text/javascript" src="{$staticprefix}js/base2.js"
					><!-- Included JS --></script>
				<script type="text/javascript" src="{$staticprefix}js/base2-dom.js"
					><!-- Included JS --></script>
				<script src="{$staticprefix}js/tncglobal.js" type="text/javascript">
					<xsl:comment>General Functions of JavaScript</xsl:comment>
				</script>
				<script type="text/javascript" src="{$staticprefix}js/gateway.js">
					<xsl:comment>Gateway JavaScript</xsl:comment>
				</script>

				<xsl:if test="view/@name= 'manage-members.html' ">
					<script type="text/javascript"
						src="{$staticprefix}js/ext/adapter/yui/yui-utilities.js">
						<xsl:comment>YUI utilities and Ext</xsl:comment>
					</script>
					<script type="text/javascript"
						src="{$staticprefix}js/ext/adapter/yui/ext-yui-adapter.js">
						<xsl:comment>YUI utilities and Ext</xsl:comment>
					</script>
					<script type="text/javascript" src="{$staticprefix}js/ext/ext-all-debug.js">
						<xsl:comment>YUI utilities and Ext</xsl:comment>
					</script>
					<script type="text/javascript" src="{$staticprefix}js/ext/ext-all.js">
						<xsl:comment>YUI utilities and Ext</xsl:comment>
					</script>

					<link rel="stylesheet" type="text/css"
						href="{$staticprefix}js/ext/resources/css/ext-all.css"/>

					<link rel="stylesheet" type="text/css"
						href="{$staticprefix}js/ext/resources/css/ytheme-gray.css"/>
				</xsl:if>
				<xsl:if test="formcontroller/field/@widget='labels'">
					<!-- Load the Javascript for handling comboboxes on labels -->
					<script type="text/javascript" src="{$staticprefix}js/labels.js"
						><!-- Included JS --></script>
				</xsl:if>

				<xsl:if test="formcontroller/field/@widget='calendar'">
					<link rel="stylesheet" href="{$staticprefix}css/calendar.css" type="text/css"
						media="screen"/>
					<script type="text/javascript" src="{$staticprefix}js/calendar.js"
						><!-- Included JS --></script>
					<script type="text/javascript" src="{$staticprefix}js/calendar-en.js"
						><!-- Included JS --></script>
					<script type="text/javascript" src="{$staticprefix}js/calendar-setup.js"
						><!-- Included JS --></script>
					<script type="text/javascript" src="{$staticprefix}js/tnc-calendar-init.js"
						><!-- Included JS --></script>
				</xsl:if>
				<xsl:comment xml:space="preserve">[if lte IE 7.]>
					&lt;script defer type="text/javascript" src="<xsl:value-of select="$staticprefix"/>js/pngfix.js"&gt;  &lt;/script&gt; 
					&lt;![endif]</xsl:comment>

			</head>
			<body>
				<xsl:apply-templates select="." mode="baselayout"/>
				<xsl:if test="formcontroller/field/@widget= 'editor' ">
					<script type="text/javascript" src="{$staticprefix}js/tiny_mce/tiny_mce.js">
						<xsl:comment>TinyMCE for editor</xsl:comment>
					</script>
					<script type="text/javascript" src="{$staticprefix}js/tinymce.js">
						<xsl:comment>TinyMCE Config for editor</xsl:comment>
					</script>
				</xsl:if>
			</body>
		</html>
	</xsl:template>

	<xsl:template match="response[view/@section='unstyled']" mode="baselayout">
		<div class="boxForm">
			<div class="content">
				<xsl:apply-templates select="/response/messages"/>
				<xsl:apply-templates select="view"/>
			</div>
		</div>
	</xsl:template>

	<xsl:template match="response" mode="baselayout">
		<div id="header">
			<div id="banner">&nbsp;</div>
			<a href="/" id="bannerLink">&nbsp;</a>
			<div id="members">
				<xsl:choose>
					<xsl:when test="user">
						<!-- Logged in User -->
						<ul>
							<li>
								<div>
									<strong>Welcome, <xsl:value-of select="user/title"/>!</strong>
									<!--Last visit: <xsl:value-of
										select="user/lastlogin"/>-->
								</div>
								<div>
									<a href="{user/@href}" class="profileLink">My
										Workspaces/Profile/Messages</a>
									<a href="{$urlprefix}signout/">Sign out</a>
								</div>
							</li>
						</ul>
					</xsl:when>
					<xsl:otherwise>
						<!-- Anonymous user and he neds to see login form -->
						<form name="formLogin" method="post" action="{loginbox/@action}">
							<ul>
								<li id="loginBox">
									<div class="memberSignIn loginText"> Member sign in <xsl:if
											test="loginbox/@failed">
											<span class="messageError">Login information is
												incorrect</span>
										</xsl:if>
									</div>
									<div class="loginText">
										<a href="/resetpassword.html">Forgot password?</a>
									</div>
									<div class="usernameBox">
										<input type="text" name="__ac_name" id="username"
											title="Usernames are case SENSITIVE so be careful with your choice."
											value="{loginbox/@username}"
											onfocus="formInputFocus('username', 'Username')"
											onblur="formInputBlur('username', 'Username')"/>
									</div>
									<div class="passwordBox">
										<input type="password" name="__ac_password" id="password"
											value="Password"
											onfocus="formInputFocus('password', 'Password')"
											onblur="formInputBlur('password', 'Password')"
											style="float:left;vertical-align:bottom;margin-top:1px;"/>
										<input type="image"
											src="{$staticprefix}images/btnLoginGray.gif"
											name="image" class="btnLoginGray"/>
									</div>
									<div class="registerBtnBox">
										<a href="{$urlprefix}register.html">
											<img src="{$staticprefix}images/btnRegisterGray.gif"
												alt="Register"/>
										</a>
									</div>
								</li>
								<li>
									<div>
										<a href="{$urlprefix}register.html">Become a member</a>
									</div>
									<div>
										<a href="about/help/#general">Why become a member?</a>
									</div>

								</li>
							</ul>
						</form>
					</xsl:otherwise>
				</xsl:choose>
			</div>
			<div id="navigation">
				<ul id="tabs">
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@section = 'home']">active</xsl:if>
						</xsl:attribute>
						<a href="/">Home</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@section = 'about']">active</xsl:if>
						</xsl:attribute>
						<a href="/about/aboutus">About</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@section = 'people']">active</xsl:if>
						</xsl:attribute>
						<a href="/people/">People</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@section = 'workspaces']">active</xsl:if>
						</xsl:attribute>
						<a href="/workspaces">Workspaces</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@section = 'library']">active</xsl:if>
						</xsl:attribute>
						<a href="/library/">Library</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@section = 'publishing']">active</xsl:if>
						</xsl:attribute>
						<a href="/about/publishing/">Publishing</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="(/response/view[@section = 'subscriptions']) or (/response/view[@section='subscribe'])">active</xsl:if>
						</xsl:attribute>
						<a href="/subscriptions/subscription.html">Subscribe</a>
					</li>
					<li>
						<xsl:attribute name="class">
							<xsl:if test="/response/view[@name = 'help.html']">active</xsl:if>
						</xsl:attribute>
						<a href="/help.html">Help</a>
					</li>
				</ul>
			</div>
			<!-- breadcrumbs -->
			<xsl:variable name="currurl" select="/response/breadcrumbs/entry/@href"/>
			<xsl:choose>
				<xsl:when test="/response/workspace">
					<xsl:if test="/response/workspace/@href !=concat($currurl, '/workspaces/cbdgateway')">		
						<xsl:apply-templates select="breadcrumbs"/>
					</xsl:if>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="breadcrumbs"/>
				</xsl:otherwise>
			</xsl:choose>
			
			
			<xsl:call-template name="sitecatalyst"/>
			<xsl:comment>Omniture Webanalytics</xsl:comment>
		</div>


		<xsl:apply-templates select="portlets"/>
		<div id="left">
			<!-- Left Column -->
			<xsl:call-template name="searchform"/>

			<xsl:apply-templates select="view[../workspace]" mode="workspacemenu"/>

			<xsl:apply-templates select="view[@name = 'view.html' and @type='colhome']"
			mode="leftcolumn"/>
			
			<xsl:apply-templates select="/response/view[@name='help.html']" mode="leftcolumn"/>

		</div>
		<div>
			<!-- Central Column -->
			<xsl:choose>
				<xsl:when test="portlets">
					<xsl:attribute name="id">middle</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="id">middleNoRight</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
				<!-- If we are in a workspace, let's put the workspace from in place -->
				<xsl:when test="workspace">
					<xsl:apply-templates select="view" mode="workspace"/>
				</xsl:when>
				<xsl:otherwise>
					<div class="content">
						<xsl:apply-templates select="/response/messages"/>

						<!--   Actions at the top right  of content area   -->
						<xsl:apply-templates select="/response/menus/actionmenu" mode="menus"/>
						<xsl:apply-templates select="/response/menus/addmenu" mode="menus"/>

						<!--   Page heading     -->
						<xsl:choose>
							<xsl:when test="view[@name = 'view-workspace.html']">
								<!-- Do nothing -->
							</xsl:when>
							<xsl:when test="view[@name = 'view.html' and @type ='colhome']">
								<!-- Do nothing -->
							</xsl:when>
							<xsl:otherwise>
								<h2 class="documentFirstHeading">
									<xsl:value-of select="view/@title"/>
								</h2>
							</xsl:otherwise>
						</xsl:choose>

						<xsl:if test="view[@name != 'view.html' and @type!='colhome']"> </xsl:if>


						<!--   Utility menu under page's title    -->
						<xsl:apply-templates select="/response/menus/utilitymenu" mode="menus"/>

						<xsl:apply-templates select="view"/>

					</div>
				</xsl:otherwise>
			</xsl:choose>
		</div>
		<div id="footer">
			<!-- Footer -->
			<xsl:choose>
				<!-- For the default site home page -->
				<xsl:when test="view[@name = 'view.html' and @type='colhome']">
					<xsl:attribute name="id">footer</xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="id">footerNoRight</xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<div>
				<a href="/about/aboutus">About</a> | <a href="mailto:email@example.com">Contact Us</a>
				| <a href="/about/help">Help/FAQs</a> |
				<a href="/about/partners"
					>Partners</a> | <a href="/about/privacy">Privacy Statement</a> | <a href="/about/disclaimer"
					>Legal Disclosure</a>
				<br/>
				ConserveOnline is a part of the <a href="http://www.conservationcommons.org" target="_blank">Conservation Commons</a>
				<br/>
			</div>
		</div>
	</xsl:template>

	<xsl:template match="view" mode="workspace">
		<div class="boxForm">
			<xsl:apply-templates select="/response/workspace/title"/>
			<div class="content" id="workspace-content">
				<!-- If there is a portal status message in the URL, display it -->
				<xsl:apply-templates select="/response/messages"/>

				<!--   Actions at the top right  of content area   -->
				<xsl:apply-templates select="../menus/actionmenu" mode="menus"/>
				<xsl:apply-templates select="../menus/addmenu" mode="menus"/>

				<!--   Page heading     -->
				
				


				
				<xsl:if test="/response/workspace/section != 'home'">
					<h2 class="documentFirstHeading">
						<xsl:value-of select="@title"/>
					</h2>
				</xsl:if>
				

				<!--   Utility menu under page's title    -->
				<xsl:apply-templates select="../menus/utilitymenu" mode="menus"/>
				
				<!-- Hack for Gateway stuff -->
				
				<xsl:if test="/response/workspace/section = 'home'">
					<xsl:variable name="currurl" select="/response/breadcrumbs/entry/@href"/>
					<xsl:if test="(/response/workspace/@href=concat($currurl, '/workspaces/cbdgateway')) and (/response/view[@name!='gsa.html'])">					
						<span>
							<script language="JavaScript1.2" type="text/javascript">
								writeGatewayNav();
							</script>
						</span>
					</xsl:if>	
				</xsl:if>
				

				<!-- Go look for a screen handler to match this view or 
					use the default in genericviews.xsl if there isn't one -->
				<xsl:apply-templates select="."/>
				
				
			</div>
			<div class="footer">
				<div class="left">
					<div class="right">&nbsp;</div>
				</div>
			</div>
		</div>
	</xsl:template>
	<xsl:template match="workspace/title">
		<div class="header">
			<div class="headerLeft">
				<div class="workspaceTitle">
					<xsl:choose>
						<xsl:when test="/response/workspace/icon">
							<img class="workspaceIcon" src="{/response/workspace/icon/@src}"
								alt="{/response/workspace/icon}"/>
						</xsl:when>
						<xsl:otherwise>
							<img class="workspaceIcon" src="{$staticprefix}images/defaultIcon.png"
								alt="Default Icon"/>
						</xsl:otherwise>
					</xsl:choose>


					<xsl:value-of select="."/>
				</div>
			</div>
		</div>
	</xsl:template>


	<!-- Left Column Content Based on Section (view/@section ) -->

	<xsl:template match="view" mode="workspacemenu">
		<xsl:variable name="toolname" select="/response/workspace/section"/>
		<xsl:variable name="workspaceurl" select="/response/workspace/@href"/>
		<div class="box2">
			<div class="header">
				<a href="{/response/workspace/@href}"> Workspace Home </a>
			</div>
			<div class="content">
				<ul>

					<li class="member">
						<xsl:attribute name="class">
							<xsl:choose>
								<xsl:when test="$toolname='members'">member currentArea</xsl:when>
								<xsl:otherwise>member</xsl:otherwise>
							</xsl:choose>
						</xsl:attribute>
						<a href="{$workspaceurl}/wsmembers/workspace-members.html">Members</a>
					</li>
					<li class="calendarItem">
						<xsl:attribute name="class">
							<xsl:choose>
								<xsl:when test="$toolname='calendar'">calendarItem currentArea</xsl:when>
								<xsl:otherwise>calendarItem</xsl:otherwise>
							</xsl:choose>
						</xsl:attribute>
						<a href="{$workspaceurl}/calendar/">Calendar</a>
					</li>
					<li class="discussions">
						<xsl:attribute name="class">
							<xsl:choose>
								<xsl:when test="$toolname='discussion'">discussions currentArea</xsl:when>
								<xsl:otherwise>discussions</xsl:otherwise>
							</xsl:choose>
						</xsl:attribute>
						<a href="{$workspaceurl}/discussion/">Discussions</a>
					</li>
					
					<!-- Gateway edit -->
					
					<xsl:variable name="gtwcurrurl" select="/response/breadcrumbs/entry/@href"/>
					<xsl:if test="(/response/workspace/@href !=concat($gtwcurrurl, '/workspaces/cbdgateway')) or (/response/user/isadmin[.='true'])">	
						
					<xsl:choose>
						<xsl:when
							test="$toolname='documents' and /response/resource/is_private='1' ">
							<li class="folder openArea">
								<a href="{$workspaceurl}/documents">Files &amp; Pages</a>
								<ul class="workspaceSubmenu ">
									<li class="currentArea">
										<a href="{$workspaceurl}/documents/private/">Private</a>
									</li>
								</ul>
							</li>
						</xsl:when>
						<xsl:when test="$toolname='documents' ">
							<li class="folder currentArea">
								<a href="{$workspaceurl}/documents/">Files &amp; Pages</a>
							</li>
						</xsl:when>
						<xsl:otherwise>
							<li class="folder">
								<a href="{$workspaceurl}/documents/">Files &amp; Pages</a>
							</li>
						</xsl:otherwise>
					</xsl:choose>
					</xsl:if>
					
					<li class="subscribe">
						<xsl:attribute name="class">
							<xsl:choose>
								<xsl:when test="$toolname='subscribe'">subscribe currentArea</xsl:when>
								<xsl:otherwise>subscribe</xsl:otherwise>
							</xsl:choose>
						</xsl:attribute>
						<a href="{$workspaceurl}/subscribe.html">RSS Feed/Updates</a>
					</li>
					
					<xsl:if test="/response/user/isadmin[.='true']">
						<li class="workspaceSetup openArea">
							<xsl:if test="$toolname='setup'">
								<xsl:attribute name="class"> workspaceSetup currentArea
								</xsl:attribute>
							</xsl:if>
							<a href="{/response/workspace/editpropsurl}">Workspace Settings</a>
						</li>
						
						<li class="workspaceMigrationGuide">
							<a href="http://conserveonline.org/about/migrated-workspace-guide">Migrated Workspace Guide</a>
						</li>
				
						<!---li class="workspaceSetup">
							<xsl:attribute name="class">
								<xsl:choose>
									<xsl:when test="$toolname='configuration'">currentArea</xsl:when>
									<xsl:otherwise>setup</xsl:otherwise>
								</xsl:choose>
							</xsl:attribute>

							<a href="{/response/workspace/editpropsurl}">Workspace Settings</a>
						</li> 
						
						<li class="workspaceSetup">
							<xsl:attribute name="class">
								<xsl:choose>
									<xsl:when test="$toolname='properties'">currentArea</xsl:when>
									<xsl:otherwise>setup</xsl:otherwise>
								</xsl:choose>
							</xsl:attribute>

							<a href="{/response/workspace/editpropsurl}">Edit Properties</a>
						</li-->
					</xsl:if>

				</ul>
			</div>
			<div class="footer">&nbsp;</div>
		</div>

		<xsl:if test="/response/workspace/joinlink">
			<a class="joinWorkspaceBtn" href="{/response/workspace/joinlink/@href}">
				<xsl:value-of select="/response/workspace/joinlink"/>
			</a>
		</xsl:if>

	</xsl:template>
	
	

</xsl:stylesheet>

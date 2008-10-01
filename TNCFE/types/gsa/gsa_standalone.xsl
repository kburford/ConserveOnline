<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    
    <!-- *** analytics information *** -->
    <xsl:variable name="analytics_account"></xsl:variable>
    <!-- *** analytics_script_url: http://www.google-analytics.com/urchin.js *** -->
    <xsl:variable
        name="analytics_script_url">http://www.google-analytics.com/urchin.js</xsl:variable>
    
    <!-- **********************************************************************
        Logo setup (can be customized)
        - whether to show logo: 0 for FALSE, 1 (or non-zero) for TRUE
        - logo url
        - logo size: '' for default image size
        ********************************************************************** -->
    <xsl:variable name="show_logo">1</xsl:variable>
    <xsl:variable name="logo_url">images/Title_Left.gif</xsl:variable>
    <xsl:variable name="logo_width">200</xsl:variable>
    <xsl:variable name="logo_height">78</xsl:variable>
    <xsl:variable name="show_top_search_box">1</xsl:variable>
    
    <!-- *** home_url: search? + collection info + &proxycustom=<HOME/> *** -->
    <xsl:variable name="home_url">search?<xsl:value-of select="$base_url"
    />&amp;proxycustom=&lt;HOME/&gt;</xsl:variable>
    
    <!-- *** base_url: collection info *** -->
    <xsl:variable name="base_url">
        <xsl:for-each
            select="/GSP/PARAM[@name = 'client' or
            
            @name = 'site' or
            @name = 'num' or
            @name = 'output' or
            @name = 'proxystylesheet' or
            @name = 'access' or
            @name = 'lr' or
            @name = 'ie']">
            <xsl:value-of select="@name"/>=<xsl:value-of select="@original_value"/>
            <xsl:if test="position() != last()">&amp;</xsl:if>
        </xsl:for-each>
    </xsl:variable>
    
    <xsl:variable name="access">
        <xsl:choose>
            <xsl:when test="/GSP/PARAM[(@name='access') and ((@value='s') or (@value='a'))]">
                <xsl:value-of select="/GSP/PARAM[@name='access']/@original_value"/>
            </xsl:when>
            <xsl:otherwise>p</xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    
    <xsl:variable name="egds_show_search_tabs">1</xsl:variable>
    
    <xsl:variable name="search_box_size">32</xsl:variable>
    <!-- *** choose search button type: 'text' or 'image' *** -->
    <xsl:variable name="choose_search_button">text</xsl:variable>
    <xsl:variable name="search_button_text">Google Search</xsl:variable>
    <xsl:variable name="search_button_image_url"></xsl:variable>
    <xsl:variable name="search_collections_xslt">1</xsl:variable>
    
    <!-- *** customize provided result page header *** -->
    <xsl:variable name="show_swr_link">1</xsl:variable>
    <xsl:variable name="swr_search_anchor_text">Search Within Results</xsl:variable>
    <xsl:variable name="show_result_page_adv_link">1</xsl:variable>
    <xsl:variable name="adv_search_anchor_text">Advanced Search</xsl:variable>
    <xsl:variable name="show_result_page_help_link">1</xsl:variable>
    <xsl:variable name="search_help_anchor_text">Search Tips</xsl:variable>
    <xsl:variable name="show_alerts_link">0</xsl:variable>
    <xsl:variable name="alerts_anchor_text">Alerts</xsl:variable>
    
    <!-- *** swr_search_url: search? + $search_url + as_q=$q *** -->
    <xsl:variable name="swr_search_url">search?<xsl:value-of
    select="$search_url"/>&amp;swrnum=<xsl:value-of select="/GSP/RES/M"/></xsl:variable>
    
    <!-- *** adv_search_url: search? + $search_url + as_q=$q *** -->
    <xsl:variable name="adv_search_url">search?<xsl:value-of
    select="$search_url"/>&amp;proxycustom=&lt;ADVANCED/&gt;</xsl:variable>
    
    <!-- *** search_url *** -->
    <xsl:variable name="search_url">
        <xsl:for-each select="/GSP/PARAM[(@name != 'start') and
            (@name != 'swrnum') and
            (@name != 'epoch' or $is_test_search != '') and
            not(starts-with(@name, 'metabased_'))]">
            <xsl:value-of select="@name"/><xsl:text>=</xsl:text>
            <xsl:value-of select="@original_value"/>
            <xsl:if test="position() != last()">
                <xsl:text disable-output-escaping="yes">&amp;</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:variable>
    
    <!-- *** if this is a test search (help variable)-->
    <xsl:variable name="is_test_search"
    select="/GSP/PARAM[@name='testSearch']/@value"/>
    
    <!-- *** help_url: search tip URL (html file) *** -->
    <xsl:variable name="help_url">/user_help.html</xsl:variable>
    
    <!-- *** alerts_url: Alerts URL (html file) *** -->
    <xsl:variable name="alerts_url">/alerts</xsl:variable>
    
    
    <!-- *** show secure results radio button *** -->
    <xsl:variable name="show_secure_radio">1</xsl:variable>
    <xsl:template name="nbsp4">
        <xsl:call-template name="nbsp3"/>
        <xsl:call-template name="nbsp"/>
    </xsl:template>
    
    <xsl:variable name="egds_appliance_tab_label">Appliance</xsl:variable>

<xsl:template match="GSP">
    <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>
                <xsl:value-of select="view/@title"/>
            </title>
            <link href="{$staticprefix}css/reset.css" rel="stylesheet" type="text/css"
                media="all"/>
            <link href="{$staticprefix}css/tnc.css" rel="stylesheet" type="text/css" media="all"/>
            <link rel="stylesheet" href="{$staticprefix}css/tncStyles.css" type="text/css"
                media="all"/>
            
            <xsl:comment xml:space="preserve">[if IE]>
                &lt;style type="text/css" &gt; @import url("<xsl:value-of select="$staticprefix"/>css/ie_hacks.css "); &lt;/style&gt; 
                &lt;![endif]</xsl:comment>
            
            
            
            <script src="{$staticprefix}js/tncglobal.js" type="text/javascript">
                <xsl:comment>General Functions of JavaScript</xsl:comment>
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
            <xsl:if
                test="formcontroller/field/@widget='labels' or formcontroller/field/@widget='checkboxgroup'">
                <!-- Load the Javascript for handling comboboxes on labels -->
                <script type="text/javascript" src="{$staticprefix}js/base2-dom-fp.js"
                    >//</script>
            </xsl:if>
            <xsl:if test="formcontroller/field/@widget='labels'">
                <!-- Load the Javascript for handling comboboxes on labels -->
                <script type="text/javascript" src="{$staticprefix}js/labels.js">//</script>
            </xsl:if>
            
            <xsl:if test="formcontroller/field/@widget='calendar'">
                <link rel="stylesheet" href="{$staticprefix}css/calendar.css" type="text/css"
                    media="screen"/>
                <script type="text/javascript" src="{$staticprefix}js/calendar.js">//</script>
                <script type="text/javascript" src="{$staticprefix}js/calendar-en.js">//</script>
                <script type="text/javascript" src="{$staticprefix}js/calendar-setup.js">//</script>
                <script type="text/javascript" src="{$staticprefix}js/tnc-calendar-init.js"
                    >//</script>
            </xsl:if>
            
            <xsl:if test="formcontroller/field/@widget= 'editor' ">
                <script type="text/javascript" src="{$staticprefix}js/tinymce.js">
                    <xsl:comment>TinyMCE Config for editor</xsl:comment>
                </script>
                <script type="text/javascript" src="{$staticprefix}js/tiny_mce/tiny_mce.js">
                    <xsl:comment>TinyMCE for editor</xsl:comment>
                </script>
                <script type="text/javascript"> loadTinyMCE(); </script>
            </xsl:if>
            
            
        </head>
        <body>
            <div id="header">
                <div id="banner">&nbsp;</div>
                <div id="members">
                    <xsl:choose>
                        <xsl:when test="user">
                            <!-- Logged in User -->
                            <ul>
                                <li>
                                    <div>
                                        <strong>Welcome, <xsl:choose>
                                            <xsl:when test="contains(user/title, ' ')">
                                                <xsl:value-of
                                                    select="substring-before(user/title, ' ')"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="user/title"/>
                                            </xsl:otherwise>
                                        </xsl:choose>!</strong>
                                        <!--Last visit: <xsl:value-of
                                            select="user/lastlogin"/>-->
                                    </div>
                                    <div>
                                        <a href="{$urlprefix}signout/">Sign out</a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <a href="{user/@href}">My Preferences</a>
                                    </div>
                                    <!--<div>
                                        <a href="{user/@href}">My Profile</a>
                                        </div>-->
                                </li>
                            </ul>
                        </xsl:when>
                        <xsl:otherwise>
                            <!-- Anonymous user and he neds to see login form -->
                            <form name="formLogin" method="post" action="{loginbox/@action}">
                                <ul>
                                    <li>
                                        <div> Member sign in <xsl:if test="loginbox/@failed">
                                            <span class="messageError">Login information is
                                                incorrect</span>
                                        </xsl:if>
                                        </div>
                                        <div>
                                            <input type="text" name="__ac_name" id="username"
                                                value="{loginbox/@username}"
                                                onFocus="formInputFocus('username', 'Username')"
                                                onBlur="formInputBlur('username', 'Username')"/>
                                        </div>
                                    </li>
                                    <li>
                                        <div>
                                            <a href="/resetpassword.html">Forgot password?</a>
                                        </div>
                                        <div>
                                            <input type="password" name="__ac_password" id="password"
                                                value="Password"
                                                onFocus="formInputFocus('password', 'Password')"
                                                onBlur="formInputBlur('password', 'Password')"
                                                style="float:left;vertical-align:bottom;margin-top:1px;"/>
                                            <input type="image"
                                                src="{$staticprefix}images/btnGoGray.gif" name="image"
                                                class="btnGoGray"/>
                                        </div>
                                    </li>
                                    <li>
                                        <div>&nbsp;</div>
                                        <div>
                                            <a href="{$urlprefix}register.html">
                                                <img src="{$staticprefix}images/btnRegisterGray.gif"/>
                                            </a>
                                        </div>
                                    </li>
                                    <li>
                                        <div>
                                            <a href="{$urlprefix}register.html">Not a member?</a>
                                        </div>
                                        <div>
                                            <a href="#">Why become a member?</a>
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
                            <a href="/about/">About</a>
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
                            <a href="/workspaces/">Workspaces</a>
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
                            <a href="/publishing/">Publishing</a>
                        </li>
                    </ul>
                </div>
                <xsl:apply-templates select="breadcrumbs"/>
            </div>
            
            <xsl:call-template name="analytics"/>
            <xsl:call-template name="swr_page_header"/>
            <hr/>
            <xsl:call-template name="copyright"/>\
            
            <div id="footer">
                <!-- Footer -->
                <xsl:choose>
                    <xsl:when test="portlets">
                        <xsl:attribute name="id">footerNoRight</xsl:attribute>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:attribute name="id">footerNoRight</xsl:attribute>
                        
                    </xsl:otherwise>
                </xsl:choose>
                <h1>Footer info goes here</h1>
                <div>Lorem Ipsum is simply dummy text of the printing and typesetting industry. </div>
            </div>
        </body>
    </html>
</xsl:template>

    <xsl:template name="analytics">
        <xsl:if test="string-length($analytics_account) != '0'">
            <script src="{$analytics_script_url}" type="text/javascript"></script>
            <script type="text/javascript">
                <xsl:comment>
                    _uacct = "<xsl:value-of select='$analytics_account'/>";
                    urchinTracker();
                    //</xsl:comment>
            </script>
        </xsl:if>
    </xsl:template>
    
    <!-- **********************************************************************
        Search within results page header (can be customized): logo and search box
        ********************************************************************** -->
    <xsl:template name="swr_page_header">
        <table border="0" cellpadding="0" cellspacing="0">
            <xsl:if test="$show_logo != '0'">
                <tr>
                    <td rowspan="3" valign="top">
                        <xsl:call-template name="logo"/>
                        <xsl:call-template name="nbsp3"/>
                    </td>
                </tr>
            </xsl:if>
            <xsl:if test="$show_top_search_box != '0'">
                <tr>
                    <td valign="middle">
                        <xsl:call-template name="search_box">
                            <xsl:with-param name="type" select="'swr'"/>
                        </xsl:call-template>
                    </td>
                </tr>
            </xsl:if>
        </table>
    </xsl:template>
    
    <!-- **********************************************************************
        Logo template (can be customized)
        ********************************************************************** -->
    <xsl:template name="logo">
        <a href="{$home_url}"><img src="{$logo_url}"
            width="{$logo_width}" height="{$logo_height}"
            alt="Go to Google Home" border="0" /></a>
    </xsl:template>
    
    <!-- **********************************************************************
        Search box input form (Types: std_top, std_bottom, home, swr)
        ********************************************************************** -->
    <xsl:template name="search_box">
        <xsl:param name="type"/>
        
        <form name="gs" method="get" action="search">
            <table border="0" cellpadding="0" cellspacing="0">
                <xsl:if test="($egds_show_search_tabs != '0') and (($type = 'home') or ($type = 'std_top'))">
                    <tr><td>
                        <table cellpadding="4" cellspacing="0">
                            <tr><td>
                                <xsl:call-template name="desktop_tab"/>
                            </td></tr>
                        </table>
                    </td></tr>
                </xsl:if>
                <xsl:if test="($type = 'swr')">
                    <tr><td>
                        <table cellpadding="4" cellspacing="0">
                            <tr><td>
                                There were about <b><xsl:value-of select="RES/M"/></b> results for <b><xsl:value-of select="$space_normalized_query"/></b>.
                                <br/>
                                Use the search box below to search within these results.
                            </td></tr>
                        </table>
                    </td></tr>
                </xsl:if>
                <tr><td>
                    <table cellpadding="0" cellspacing="0">
                        <tr>
                            <td valign="middle">
                                <font size="-1">
                                    <xsl:choose>
                                        <xsl:when test="($type = 'swr')">
                                            <input type="text" name="as_q" size="{$search_box_size}" maxlength="256" value=""/>
                                            <input type="hidden" name="q" value="{$qval}"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <input type="text" name="q" size="{$search_box_size}" maxlength="256" value="{$space_normalized_query}"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </font>
                            </td>
                            <xsl:call-template name="collection_menu"/>
                            <td valign="middle">
                                <font size="-1">
                                    <xsl:call-template name="nbsp"/>
                                    <xsl:choose>
                                        <xsl:when test="$choose_search_button = 'image'">
                                            <input type="image" name="btnG" src="{$search_button_image_url}"
                                                valign="bottom" width="60" height="26"
                                                border="0" value="{$search_button_text}"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <input type="submit" name="btnG" value="{$search_button_text}"/>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </font>
                            </td>
                            <td nowrap="1">
                                <font size="-2">
                                    <xsl:if test="(/GSP/RES/M > 0) and ($show_swr_link != '0') and ($type = 'std_bottom')">
                                        <xsl:call-template name="nbsp"/>
                                        <xsl:call-template name="nbsp"/>
                                        <a href="{$swr_search_url}">
                                            <xsl:value-of select="$swr_search_anchor_text"/>
                                        </a>
                                        <br/>
                                    </xsl:if>
                                    <xsl:if test="$show_result_page_adv_link != '0'">
                                        <xsl:call-template name="nbsp"/>
                                        <xsl:call-template name="nbsp"/>
                                        <a href="{$adv_search_url}">
                                            <xsl:value-of select="$adv_search_anchor_text"/>
                                        </a>
                                        <br/>
                                    </xsl:if>
                                    <xsl:if test="$show_alerts_link != '0'">
                                        <xsl:call-template name="nbsp"/>
                                        <xsl:call-template name="nbsp"/>
                                        <a href="{$alerts_url}">
                                            <xsl:value-of select="$alerts_anchor_text"/>
                                        </a>
                                        <br/>
                                    </xsl:if>
                                    <xsl:if test="$show_result_page_help_link != '0'">
                                        <xsl:call-template name="nbsp"/>
                                        <xsl:call-template name="nbsp"/>
                                        <a href="{$help_url}">
                                            <xsl:value-of select="$search_help_anchor_text"/>
                                        </a>
                                    </xsl:if>
                                    <br/>
                                </font>
                            </td>
                        </tr>
                        <xsl:if test="$show_secure_radio != '0'">
                            <tr>
                                <td colspan="2">
                                    <font size="-1">Search:
                                        <xsl:choose>
                                            <xsl:when test="$access='p'">
                                                <label><input type="radio" name="access" value="p" checked="checked" />public content</label>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <label><input type="radio" name="access" value="p"/>public content</label>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                        <xsl:choose>
                                            <xsl:when test="$access='a'">
                                                <label><input type="radio" name="access" value="a" checked="checked" />public and secure content</label>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <label><input type="radio" name="access" value="a"/>public and secure content</label>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </font>
                                </td>
                            </tr>
                        </xsl:if>
                    </table>
                </td></tr>
            </table>
            <xsl:text>
            </xsl:text>
            <xsl:call-template name="form_params"/>
        </form>
    </xsl:template>   
    
    <!-- **********************************************************************
        Utility functions for generating html entities
        ********************************************************************** -->
    <xsl:template name="nbsp">
        <xsl:text disable-output-escaping="yes">&amp;nbsp;</xsl:text>
    </xsl:template>
    <xsl:template name="nbsp3">
        <xsl:call-template name="nbsp"/>
        <xsl:call-template name="nbsp"/>
        <xsl:call-template name="nbsp"/>
    </xsl:template>
    
    <!-- **********************************************************************
        Utility function for constructing copyright text (do not customize)
        ********************************************************************** -->
    <xsl:template name="copyright">
        <center>
            <br/><br/>
            <p>
                <font face="arial,sans-serif" size="-1" color="#2f2f2f">
                    Powered by Google Search Appliance</font>
            </p>
        </center>
    </xsl:template>
    
    <!-- **********************************************************************
        Google Desktop for Enterprise integration templates
        ********************************************************************** -->
    <xsl:template name="desktop_tab">
        
        <!-- *** Show the Google tabs *** -->
        
        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1" href="http://www.google.com/search?q={$qval}">Web</a>
        </font>
        
        <xsl:call-template name="nbsp4"/>
        
        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1" href="http://images.google.com/images?q={$qval}">Images</a>
        </font>
        
        <xsl:call-template name="nbsp4"/>
        
        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1" href="http://groups.google.com/groups?q={$qval}">Groups</a>
        </font>
        
        <xsl:call-template name="nbsp4"/>
        
        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1" href="http://news.google.com/news?q={$qval}">News</a>
        </font>
        
        <xsl:call-template name="nbsp4"/>
        
        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1" href="http://froogle.google.com/froogle?q={$qval}">Froogle</a>
        </font>
        
        <xsl:call-template name="nbsp4"/>
        
        <font size="-1">
            <a class="q" onClick="return window.qs?qs(this):1" href="http://local.google.com/local?q={$qval}">Local</a>
        </font>
        
        <xsl:call-template name="nbsp4"/>
        
        <!-- *** Show the desktop and web tabs *** -->
        
        <xsl:if test="CUSTOM/HOME">
            <xsl:comment>trh2</xsl:comment>
        </xsl:if>
        <xsl:if test="Q">
            <xsl:comment>trl2</xsl:comment>
        </xsl:if>
        
        <!-- *** Show the appliance tab *** -->
        <font size="-1"><b><xsl:value-of select="$egds_appliance_tab_label"/></b></font>
        
    </xsl:template>
    
    <!-- *** space_normalized_query: q = /GSP/Q *** -->
    <xsl:variable name="qval">
        <xsl:value-of select="/GSP/Q"/>
    </xsl:variable>
    
    <xsl:variable name="space_normalized_query">
        <xsl:value-of select="normalize-space($qval)"
            disable-output-escaping="yes"/>
    </xsl:variable>
    
    <!-- **********************************************************************
        Collection menu beside the search box
        ********************************************************************** -->
    <xsl:template name="collection_menu">
        <xsl:if test="$search_collections_xslt != ''">
            <td valign="middle">
                
                <select name="site">
                    <xsl:choose>
                        <xsl:when test="PARAM[(@name='site') and (@value='ConservationWebsites')]">
                            <option value="ConservationWebsites" selected="selected">ConservationWebsites</option>
                        </xsl:when>
                        <xsl:otherwise>
                            <option value="ConservationWebsites">ConservationWebsites</option>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:choose>
                        <xsl:when test="PARAM[(@name='site') and (@value='ConserveOnline')]">
                            <option value="ConserveOnline" selected="selected">ConserveOnline</option>
                        </xsl:when>
                        <xsl:otherwise>
                            <option value="ConserveOnline">ConserveOnline</option>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:choose>
                        <xsl:when test="PARAM[(@name='site') and (@value='GIS')]">
                            <option value="GIS" selected="selected">GIS</option>
                        </xsl:when>
                        <xsl:otherwise>
                            <option value="GIS">GIS</option>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:choose>
                        <xsl:when test="PARAM[(@name='site') and (@value='NatureOrg')]">
                            <option value="NatureOrg" selected="selected">NatureOrg</option>
                        </xsl:when>
                        <xsl:otherwise>
                            <option value="NatureOrg">NatureOrg</option>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:choose>
                        <xsl:when test="PARAM[(@name='site') and (@value='default_collection')]">
                            <option value="default_collection" selected="selected">default_collection</option>
                        </xsl:when>
                        <xsl:otherwise>
                            <option value="default_collection">default_collection</option>
                        </xsl:otherwise>
                    </xsl:choose>
                </select>
                
            </td>
        </xsl:if>
    </xsl:template>
    
    <!-- *** form_params: parameters carried by the search input form *** -->
    <xsl:template name="form_params">
        <xsl:for-each
            select="PARAM[@name != 'q' and
            @name != 'ie' and
            not(contains(@name, 'as_')) and
            @name != 'btnG' and
            @name != 'btnI' and
            @name != 'site' and
            @name != 'filter' and
            @name != 'swrnum' and
            @name != 'start' and
            @name != 'access' and
            @name != 'ip' and
            (@name != 'epoch' or $is_test_search != '') and
            not(starts-with(@name ,'metabased_'))]">
            <input type="hidden" name="{@name}" value="{@value}" />
            
            <xsl:if test="@name = 'oe'">
                <input type="hidden" name="ie" value="{@value}" />
            </xsl:if>
            <xsl:text>
            </xsl:text>
        </xsl:for-each>
        <xsl:if test="$search_collections_xslt = '' and PARAM[@name='site']">
            <input type="hidden" name="site" value="{PARAM[@name='site']/@value}"/>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>



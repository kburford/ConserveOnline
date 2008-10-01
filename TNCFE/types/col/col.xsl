<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
<!ENTITY ldquo   "&#8220;">
<!ENTITY rdquo   "&#8221;">
<!ENTITY rsquo   "&#8217;">
<!ENTITY sect   "&#167;">
<!ENTITY copy   "&#169;">
<!ENTITY ndash   "&#8211;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    <xsl:output indent="yes"/>

    <xsl:template match="view[@name = 'view.html' and @type='colhome']" mode="leftcolumn">
        <xsl:for-each select="/response/colhome/sideimage">
            <div class="boxImage">
                <a href="{@href}">
                    <img src="{img/@href}" border="0" alt="{img/@title}>"/>
                </a>
            </div>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="/response/view[@name='help.html']" mode="leftcolumn">
        <div class="boxImage">
            <div class="rss-box">
            <h3>Help Menu</h3>
            <div class="rss-box-content">
                <span><div id="text1trigger" onclick="switchMenu('text1', 'arrow1');" style="cursor: pointer;"><img id="arrow1" src="{$staticprefix}images/arrowright.gif"/><strong>General</strong></div></span>
                <div id="text1" style="display: none;">
                    <ul><li><a href="help.html#04" onclick="switchMenu('text4');">What Is ConserveOnline</a></li>
                        <li><a href="help.html#05" onclick="switchMenu('text5');">Why should I join ConserveOnline?</a></li>
                        <li><a href="help.html#06" onclick="switchMenu('text6');">What is Search?</a></li>
                        <li><a href="help.html#21" onclick="switchMenu('text21');">Can I search other Conservation organizations?</a></li>
                        <li><a href="help.html#22" onclick="switchMenu('text22');">Can I recommend other websites to search?</a>  </li>
                        <li><a href="help.html#23" onclick="switchMenu('text23');">What are the Google results?</a></li>
                    </ul>
                </div>
                

                <div id="text2trigger" onclick="switchMenu('text2', 'arrow2');" style="cursor: pointer;"><img id="arrow2" src="{$staticprefix}images/arrowright.gif"/><strong>Library</strong></div>
                <div id="text2" style="display: none;">
                <ul>
                    <li><a href="help.html#24" onclick="switchMenu('text24');">What is the Library?</a></li>
                    <li><a href="help.html#25" onclick="switchMenu('text25');">What are the advantages of using the Library?</a></li>
                    <li><a href="help.html#26" onclick="switchMenu('text26');">What is a Digital Object Identifier (DOI)?</a></li>
                    <li><a href="help.html#27" onclick="switchMenu('text27');">How can I add a file to the Library?</a></li>
                    <li><a href="help.html#28" onclick="switchMenu('text28');">What are Keywords?</a></li>
                    <li><a href="help.html#29" onclick="switchMenu('text29');">What are Search terms?</a></li>
                    <li><a href="help.html#30" onclick="switchMenu('text30');">What is the difference between Keywords and Search Terms?</a></li>
                </ul>
                </div>
                
      
                    <div id="text3trigger" onclick="switchMenu('text3', 'arrow3');" style="cursor: pointer;"><img id="arrow3" src="{$staticprefix}images/arrowright.gif"/><strong>Workspaces</strong></div>
                    <div id="text3" style="display: none;">
                        <ul>
                            <li><a href="help.html#31" onclick="switchMenu('text31');">What is a Workspace?</a></li>
                            <li><a href="help.html#32" onclick="switchMenu('text32');">How do I join a Workspace?</a></li>
                            <li><a href="help.html#33" onclick="switchMenu('text33');">How can I change my Workspace homepage?</a></li>
                            <li><a href="help.html#34" onclick="switchMenu('text34');">How do I edit a page in my Workspace?</a></li>
                            <li><a href="help.html#35" onclick="switchMenu('text35');">What is metadata and where is it entered in COL?</a></li>
                            <li><a href="help.html#36" onclick="switchMenu('text36');">What is searchable in my Workspace?</a></li>
                            <li><a href="help.html#37" onclick="switchMenu('text37');">Can I publish documents in my Workspace?</a></li>
                            <li><a href="help.html#38" onclick="switchMenu('text38');">How do I add new members to Workspaces?</a></li>
                            <li><a href="help.html#39" onclick="switchMenu('text39');">How do I create an event in a calendar?</a></li>
                            <li><a href="help.html#40" onclick="switchMenu('text40');">How do I create a topic in a discussion?</a></li>
                            <li><a href="help.html#41" onclick="switchMenu('text41');">What is the Workspace Settings tab?</a></li>
                            <li><a href="help.html#42" onclick="switchMenu('text42');">What is the difference between searching and browsing in a Workspace?</a></li>
                        </ul>
                    
                    </div>
                <p align="center"><a href="#">Contact COL</a></p>
                
            </div>
            </div>
            </div>
    </xsl:template>

    <!-- middle column content for portal home page - Logan 10/16/07 -->
    <xsl:template match="view[@name = 'view.html' and @type='colhome']">
        <div class="featured">
            
            <div class="col-news">
                <h3>ConserveOnline News</h3>
                <div class="col-news-content">
                  In response to COL member feedback, we've added new features that we believe enhances the user experience including:
                  <ul>
                      <li>RSS Feeds for individual workspaces</li>
                      <li>ConserveOnline daily updates via email or <a href="{$staticprefix}html/rss_popup.html"
                          onclick="window.open(this.href, 'popupwindow', 'width=500,height=300,scrollbars,resizable');
                          return false;">RSS feed</a></li>
                      <li>User ratings for library files</li>
                  </ul>
                    <a href="/about/whatsnew">Read more...</a>
                </div>
            </div>
            <br/>
            
            <div class="box1">
                <div>
                    <img src="{/response/colhome/feature/img/@href}" width="460" alt="Featured Workspace"/>
                </div>
                <div class="content">
                    <div class="title">
                        <h1>Featured Workspace</h1>
                    </div>
                    <div class="details">
                        <h2>
                            <xsl:value-of select="/response/colhome/feature/date"/>
                        </h2>
                        <div>
                            <xsl:apply-templates select="/response/colhome/feature/text/*"
                                mode="copy"/>
                        </div>
                        <div>
                            <a href="{/response/colhome/feature/@href}">Visit Workspace</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="box2">
                <h1>Participate in the International Conservation Community</h1>
                <ul class="portalFastLinks">
                    <li class="left">
                        <div class="library">

                            <a href="/library" style="text-decoration:none"><h2>Library</h2></a>
                            <div>
                                <a href="/library/bysearchterms.html">Browse by search term</a>
                            </div>
                            <div>
                                <a href="/library/byauthor.html">Browse by author</a>
                            </div>

                            <div>
                                <a href="/library/@@add-libraryfile.html">Add a file</a>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="workspaces">
                            <a href="/workspaces" style="text-decoration:none"><h2>Workspaces</h2></a>

                            <div>
                                <a href="/workspaces/all.html">Join a workspace</a>
                            </div>
                            <div>
                                <a href="/workspaces/@@add-workspace.html">Start a workspace</a>
                            </div>
                            <div>
                                <a href="/about/help/#workspaces">Learn About Workspaces</a>
                            </div>

                        </div>
                    </li>
                </ul>
                <ul class="portalFastLinks">
                    <li class="left">
                        <div class="register">
                            
                                <xsl:choose>
                                    <xsl:when test="/response/user">
                                        <!-- Logged in User -->
                                        <h2>My Profile</h2>
                                        <div>
                                            <a href="{/response/user/@href}" class="profileLink">Update Profile</a>
                                        </div>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <a href="/register.html" style="text-decoration:none"><h2>Register</h2></a>
                                        <!-- Anonymous user and he needs to see login form -->
                                        <div>
                                            <a href="/register.html">Become a member</a>
                                        </div>
                                    </xsl:otherwise>
                                </xsl:choose>


                            <div>
                                <a href="/about/help/#general">Member benefits</a>
                            </div>
                        </div>
                    </li>
                    <li>
                        <div class="publishing">
                            <a href="/about/publishing" style="text-decoration:none"><h2>Publishing</h2></a>
                            <div>
                                <a href="/about/publishing">Learn about publishing</a>
                            </div>
                            <div>
                                <a href="/library/byall.html">Add To The Library </a>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </xsl:template>


    <xsl:template match="portlets[/response/view/@type='colhome']">
        <div id="right" class="box1 homeRightPortlets">


            <!-- First portlet. -->
            
            <xsl:for-each select="portlet[@type='mostworkspaces']">
            <div class="box1">
                <div class="header">Current workspaces</div>
                <div class="content">
                    <div>
                        <a href="/workspaces/bycountry.html"><img src="{$staticprefix}images/imgRightBox1Map.gif" border="0" alt="View Workspaces By Country"/></a>
                    </div>
                    <p align="center">Top Regions/Countries By Number of Workspaces</p>
                    <ol class="numberedPortlet">
                    <xsl:for-each select="resource">
                        <li class="numberedPortletItem">
                            <a href="{@href}">
                                <xsl:value-of select="title"/>
                            </a>
                            <span> (<xsl:value-of select="count"/>) </span>
                        </li>
                    </xsl:for-each>
                    </ol>
                    <!-- The following div is only here so that the <div class="list" contains non-floating elements, so it will encapsulate the <ul> - Logan -->  
                    <p align="center"><a href="/workspaces/bycountry.html">View All Workspaces By Region/Country</a></p>
                </div>
            </div>
            </xsl:for-each>   
                

                    
                        
            <!-- Second portlet, New Workspaces -->
            <xsl:for-each select="portlet[@type='newworkspaces']">
                <div class="box2">
                    <div class="header">
                        <div class="headerContainer">
                            <h1 id="newWorkspacesTrigger">
                                <a href="javascript:toggleLayer('newWorkspaces');">+/- New Workspaces </a>
                            </h1>
                        </div>
                    </div>
                    <div class="content" id="newWorkspaces">
                        <ul class="list1">
                            <xsl:for-each select="resource">
                                <li>
                                    <a href="{@href}">
                                        <xsl:value-of select="title"/>
                                    </a>
                                    <span> (Created <xsl:apply-templates select="created"
                                            mode="griddate"/>) </span>
                                </li>
                            </xsl:for-each>
                        </ul>
                    </div>
                </div>
            </xsl:for-each>

            <!-- Third portlet, recently published -->
            <xsl:for-each select="portlet[@type='recentlypublished']">
                <div class="box2">
                    <div class="header">
                        <div class="headerContainer">
                            <h1>
                                <a href="javascript:toggleLayer('recentlyPublishedDocuments');">+/- Recently Published Documents </a>
                            </h1>
                        </div>
                    </div>
                    <div class="content" id="recentlyPublishedDocuments">
                        <ol class="numberedPortlet">
                            <xsl:for-each select="resource">
                                <li class="numberedPortletItem">
                                    <span class="numberedPortletMarker">
                                        <xsl:value-of select="position()"/>
                                    </span>
                                    <a class="numberedPortletAnchor" href="{@href}">
                                        <xsl:value-of select="title"/>
                                    </a>
                                </li>
                            </xsl:for-each>
                        </ol>
                    </div>
                </div>
            </xsl:for-each>
        </div>
    </xsl:template>
    
    
    <xsl:template match="view[@name='subscription.html' and @section='subscribe']" mode="formhelp">
        <div class="subscribe">
        <p><strong>Get notified about updated ConserveOnline content by email or RSS.</strong></p>
            <p>Select your areas of interest below and you will be updated daily (via email or RSS feed) when files (that match your selections) are updated or added to:</p>
<ul><li>ConserveOnline Library</li>
                <li>All public ConserveOnline workspaces</li>
            </ul>  
<p>At this time, we only offer email notification on a daily digest basis.</p>
            
            <xsl:if test="/response/formcontroller/field/@name='form.delivery_method' and /response/formcontroller/field/value/option/@selected='selected'">
                <p>    Click here to <a href="/subscriptions/unsubscription.html">unsubscribe</a>.</p>
            </xsl:if>
            
            <p><div id="text1trigger" onclick="switchMenu('text1', 'arrow1');" style="cursor: pointer;"><img id="arrow1" src="{$staticprefix}images/arrowright.gif"/><strong>How is my search performed if I select more than one item in any given topic-area?</strong></div></p>
                <div id="text1" style="display: none;" class="textSwitch">
                    <p>The content is created by a search query based on your selections which uses an <i>AND</i> operator between the different topics and an <i>OR</i> operator within each topic.  For instance, 
    if you make the following selections: Region/Country = "Africa"; Habitat Type = "Benthic", "Forest", "Wetlands"; Monitoring Type = "Anecdote", the system will generate content based on the following: all library 
    documents and public workspace files where Region = 'Africa' <i>AND</i> Habitat Type = 'Benthic' <i>OR</i> Habitat Type = 'Forest' <i>OR</i> Habitat Type = 'Wetlands' <i>AND</i> Monitoring Type = 'Anecdote'.</p>
                </div>
            
        </div>
    </xsl:template>
    
    <xsl:template match="view[@name='success.html' and @type='site' and @section='subscriptions']">
        
        <div class="rss-box">
            <h3>Looking for Workspace <br/>RSS Feeds and Updates?</h3>
            <div class="rss-box-content">
                If you're looking for updates to specific workspaces, RSS feeds are now available. These feeds include files and pages, events and discussion posts for all individual workspaces. To get started, access your
                favorite workspace and look for the "RSS Feed/Updates" link in the left-hand workspace navigation menu.
                </div>
        </div>
        
        <p>Your subscription information has been saved. </p>
        <xsl:if test="/response/subscribe/email='true'">
            <p>By selecting the email delivery option, you will be receiving updates to the email address in your ConserveOnline profile (<xsl:value-of select="/response/user/email"/>). Email updates will be sent on a daily digest 
            basis or when new content is available that matches your selections. Note: you will not receive more than one email per day from ConserveOnline. </p>
            <p><b>Note: if you are updating your subscription, you will not receive an immediate email and the changes you made to your subscription options will be reflected in your next digest message.</b></p>
        </xsl:if>
        <xsl:if test="/response/subscribe/email='false'">
        <xsl:variable name="rss-url">
            <xsl:value-of select="/response/subscribe/rss"/>
        </xsl:variable>
        <p>Your RSS feed:  <img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS" title="Get RSS"/> &nbsp; <a href="{$rss-url}"><xsl:value-of select="/response/subscribe/rss"/></a> </p>
       
         <xsl:call-template name="rss-helper"/>
            </xsl:if>
    </xsl:template>
    
    
    <xsl:template match="view[@name='help.html' and @type='site']">
        
        <div class="help-menu">
            <h3>Top ConserveOnline FAQs</h3>
            <div class="help-menu-content">
                <ul>
                    <li><b><a href="#" onclick="toggleSub('01'); return false;">I can't remember my username or password</a></b>
                    <div id="01" style="display: none;">
                     If you have your username handy but cannot remember your password, you can reset your COL password by using the "Forgot Password" link in the top navigation bar. Simply follow the directions and your will receive an email allowing to reset your password. If you've forgotten your COL username, send an email to <a href="mailto:conserveonline@example.com">ConserveOnline</a> and COL administrators will followup with instructions on how to retrieve your username. Make sure the email body contains your full name and email address used when creating your COL account.       
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('02'); return false;">What is ConserveOnline?</a></b>
                    <div id="02" style="display: none;">
                        <span>ConserveOnline is a meeting place for the conservation community, open to anyone who wants to find or share information relevant to conservation science and practice. <a href="help.html#04" onclick="switchMenu('text4');">Read more...</a></span>
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('03'); return false;">How Do I Update My Workspace?</a></b>
                    <div id="03" style="display: none;">
                        <span>Go to "Files &amp; Pages" and <a href="help.html#34" onclick="switchMenu('text34');">read more...</a></span>
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('04'); return false;">What is the Difference Between Keywords and Search Terms?</a></b>
                    <div id="04" style="display: none;">
                        <span>A keyword is used to describe the file or page that you're creating in a workspace. A search term is used to describe a workspace or a file in a library. A keyword is not searchable by the search engine; however, search terms are searchable by the search engine.</span>
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('05'); return false;">What is a Keyword?</a></b>
                    <div id="05" style="display: none;">
                        <span>Keywords are used to describe and (similarly) organize files and pages in a workspace. In migrated workspaces, they are initially set to the foldername in which a file or page was previously located. The workspace manager has the freedom to create the most appropriate and relevant keywords for use within each workspace. Keywords are only applicable within your workspace. Keywords are not used to search for information using a search engine. <a href="help.html#28" onclick="switchMenu('text28');">Read more...</a></span>
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('06'); return false;">What happened to the folders in my workspace?</a></b>
                    <div id="06" style="display: none;">
                        They are now workspace keywords. Keywords are used to describe and (similarly) organize files and pages in a workspace.  In migrated workspaces, they are initially set to the foldername in which a file or page was previously located.
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('07'); return false;">How do I add/delete/edit keywords?</a></b>
                    <div id="07" style="display: none;">
                        When in your workspace, go to "Files &amp; Pages" and select the "Browse By Keyword" link. Here you will see a list of keywords for your workspace. Selecting any specific keyword, you'll see all files associated with that keyword as well as a 'Edit Keyword' button in the upper right-hand corner of the screen. Clicking that button gives you the ability to edit that keyword.
                    </div>
                    </li>
                    <li><b><a href="#" onclick="toggleSub('08'); return false;">I am the owner of a migrated workspace and am confused about some of the changes. How I can better understand these workspace changes?</a></b>
                    <div id="08" style="display: none;">
                       We've created a guide for migrated workspace owners and it's accessible here... <a href="http://conserveonline.org/about/migrated-workspace-guide" target="_blank">Migrated Workspace Guide</a>.
                    </div>
                    </li>
                    
                </ul>
            </div>
        </div>
        <div class="help-content">
        <a name="top"></a>
        <p>How may we help you? You can use this page to quickly find answers to common questions about ConserveOnline. Simply browse the topics below to locate the information you are looking for.</p>
        <a name="general"></a>
            <div class="help-content-title">
                <h3>General</h3>
                </div>

            <br/><div id="text4trigger" onclick="switchMenu('text4', 'arrow4');" style="cursor: pointer;" class="help-content-head"><img id="arrow4" src="{$staticprefix}images/arrowright.gif"/> <b>What is ConserveOnline?</b><a name="04"/></div>
            <div class="help-content-sub" id="text4" style="display: none;">
        <span>ConserveOnline is a meeting place for the conservation community, open to anyone who wants to find or share information relevant to conservation science and practice. Using ConserveOnline you can:</span>
        <span><ul><li> Post data, documents, images, maps and other resources in the ConserveOnline library.
        </li><li> Announce upcoming meetings or events and host discussions in your workspace. 
        </li><li> Search for documents within a selected list of conservation organization websites.
        </li></ul></span>
        <span>The Nature Conservancy created and maintains ConserveOnline in collaboration with many partners. ConserveOnline is intended to help improve the practice of conservation across organizations and national boundaries.</span>
            </div>
            
            <div id="text5trigger" onclick="switchMenu('text5', 'arrow5');" style="cursor: pointer;" class="help-content-head"><img id="arrow5" src="{$staticprefix}images/arrowright.gif"/> <b>Why should I join ConserveOnline?</b><a name="05"/></div>
            <div class="help-content-sub" id="text5" style="display: none;">
        <span>You should become a member of the ConserveOnline website if you want to:</span>
        <span><ul><li> Contribute documents, files or other resources to the ConserveOnline library.
        </li><li> Have a workspace, calendar and discussion groups.</li></ul></span>
        <span>However, if you want to browse the library or public workspaces, you do not need to be a member of ConserveOnline.</span>
            </div>
          
            <div id="text6trigger" onclick="switchMenu('text6', 'arrow6');" style="cursor: pointer;" class="help-content-head"><img id="arrow6" src="{$staticprefix}images/arrowright.gif"/> <b>What Is Search?</b><a name="05"/></div>
            <div class="help-content-sub" id="text6" style="display: none;">
        <span><p>When you perform a search, the search engines will perform two types of searches:</p>
        <p><b>Internal Search:</b> If you are searching the site internally, the search engine will search:</p></span>
            <ul><li> The workspace name and the full text of all documents in your workspace. 
            </li><li> All search terms. If you would like to highlight key concepts in your workspace and thus increase the likelihood that interested users will find your content, you can define specific search terms in your workspace by entering words or phrases into the field called Other Search Terms on the Workspace Settings page. 
            </li><li> All metadata. See the frequently asked question for How can I add a file to a Library?</li></ul>
        <span><b>External Search:</b> If you are searching the site externally, the search engine will search:</span>
            <ul><li> The External Conservations Sites and GIS Portal Content.</li></ul>
        <span><p>Below is the collection of authoritative conservation websites that has been made available for searching. The current list is:</p></span>
        
        
                <span><div id="text7trigger" onclick="switchMenu('text7', 'arrow7');" style="cursor: pointer;"><img id="arrow7" src="{$staticprefix}images/arrowright.gif"/> <b>The Nature Conservancy</b></div></span>
                    <div id="text7" style="display: none;" class="textSwitch">
        <ul><li><a href="http://nature.org/"> http://nature.org/</a>
        </li><li><a href="http://sites-conserveonline.org/"> http://sites-conserveonline.org/</a> 
        </li><li><a href="http://www.lastgreatplaces.org/"> http://www.lastgreatplaces.org/</a>
        </li><li><a href="http://www.tnc-ecomanagement.org/"> http://www.tnc-ecomanagement.org/</a> 
        </li><li><a  href="http://tncfire.org/"> http://tncfire.org/</a> 
        </li><li><a href="http://tncfellows.org/"> http://tncfellows.org/</a>
        </li><li><a href="http://parksinperil.org/"> http://parksinperil.org/</a>
        </li><li><a href="http://www.privateforest.org/"> http://www.privateforest.org/</a>
        </li><li><a href="http://www.freshwaters.org/"> http://www.freshwaters.org/</a>
        </li><li><a href="http://tncweeds.ucdavis.edu/"> http://tncweeds.ucdavis.edu/</a></li></ul>
                    </div>
                
                <span><div id="text8trigger" onclick="switchMenu('text8', 'arrow8');" style="cursor: pointer;"><img id="arrow8" src="{$staticprefix}images/arrowright.gif"/> <b>NatureServe</b></div></span>
                <div id="text8" style="display: none;" class="textSwitch">
        <ul><li><a  href="http://www.natureserve.org/">http://www.natureserve.org/</a></li></ul>
                </div>
                <span><div id="text9trigger" onclick="switchMenu('text9', 'arrow9');" style="cursor: pointer;"><img id="arrow9" src="{$staticprefix}images/arrowright.gif"/> <b>The World Wildlife Fund's English language sites</b></div></span>
                <div id="text9" style="display: none;" class="textSwitch">
        <ul><li><a  href="http://www.wwf.org/"> http://www.wwf.org/</a>
        </li><li><a  href="http://www.worldwildlife.org/"> http://www.worldwildlife.org/</a>
        </li><li><a  href="http://www.worldwildlife.org/bsp/"> http://www.worldwildlife.org/bsp/</a> 
        </li><li><a  href="http://www.wwfus.org/"> http://www.wwfus.org/</a>
        </li><li><a  href="http://www.panda.org/"> http://www.panda.org/</a> 
        </li><li><a  href="http://www.panda.org.za/"> http://www.panda.org.za/</a> 
        </li><li><a  href="http://www.wwfcanada.org/"> http://www.wwfcanada.org/</a> 
        </li><li><a  href="http://www.wwf.org.au/"> http://www.wwf.org.au/</a> 
        </li><li><a  href="http://www.wwf.org.nz/"> http://www.wwf.org.nz/</a>
        </li><li><a  href="http://www.wwf.org.uk/"> http://www.wwf.org.uk/</a> 
        </li><li><a  href="http://www.wwfpacific.org.fj/"> http://www.wwfpacific.org.fj/</a> </li></ul>
                </div>
                
                <span><div id="text10trigger" onclick="switchMenu('text10', 'arrow10');" style="cursor: pointer;"><img id="arrow10" src="{$staticprefix}images/arrowright.gif"/> <b>Portions of the World Resources Institute's site</b></div></span>
                <div id="text10" style="display: none;" class="textSwitch">
        <ul><li><a  href="http://www.wri.org/"> http://www.wri.org/</a> 
        </li><li><a  href="http://biodiv.wri.org/"> http://biodiv.wri.org/</a>
        </li><li><a  href="http://forests.wri.org/"> http://forests.wri.org/</a> 
        </li><li><a  href="http://marine.wri.org/"> http://marine.wri.org/</a> 
        </li><li><a  href="http://water.wri.org/"> http://water.wri.org/</a>
        </li><li><a  href="http://sustag.wri.org"> http://sustag.wri.org</a>/ 
        </li><li><a  href="http://climate.wri.org/"> http://climate.wri.org/</a> 
        </li><li><a  href="http://reefsatrisk.wri.org/"> http://reefsatrisk.wri.org/</a>
        </li><li><a  href="http://about.wri.org/"> http://about.wri.org/</a> 
        </li><li><a  href="http://newsroom.wri.org/"> http://newsroom.wri.org/</a>
        </li><li><a  href="http://pdf.wri.org/"> http://pdf.wri.org/</a> </li></ul>
                </div>
                <span><div id="text11trigger" onclick="switchMenu('text11', 'arrow11');" style="cursor: pointer;"><img id="arrow11" src="{$staticprefix}images/arrowright.gif"/> <b>Conservation International, including the Center for Applied Biodiversity Science</b></div></span>
                <div id="text11" style="display: none;" class="textSwitch">
        <ul><li><a  href="http://www.conservation.org/"> http://www.conservation.org/</a>
        </li><li><a  href="http://www.biodiversityscience.org/"> http://www.biodiversityscience.org/</a> </li></ul>
                </div>
                <span><div id="text12trigger" onclick="switchMenu('text12', 'arrow12');" style="cursor: pointer;"><img id="arrow12" src="{$staticprefix}images/arrowright.gif"/> <b>The National Sea Grant Library</b></div></span>
                <div id="text12" style="display: none;" class="textSwitch">
                    <ul><li> <a  href="http://nsgl.gso.uri.edu/">http://nsgl.gso.uri.edu/</a></li></ul>
                </div>
                <span><div id="text13trigger" onclick="switchMenu('text13', 'arrow13');" style="cursor: pointer;"><img id="arrow13" src="{$staticprefix}images/arrowright.gif"/> <b>Rainforest Action Network</b></div></span>
                <div id="text13" style="display: none;" class="textSwitch">
        <ul><li><a  href="http://www.ran.org/"> http://www.ran.org/</a>
        </li><li><a  href="http://www.rainforestweb.org/"> http://www.rainforestweb.org/</a> </li></ul>
                </div>
                <span><div id="text14trigger" onclick="switchMenu('text14', 'arrow14');" style="cursor: pointer;"><img id="arrow14" src="{$staticprefix}images/arrowright.gif"/> <b>Forest Action Network</b></div></span>
                <div id="text14" style="display: none;" class="textSwitch">    
                    <ul><li> <a  href="http://www.fanweb.org/">http://www.fanweb.org/</a></li></ul>
                </div>
                
                    
                <span><div id="text15trigger" onclick="switchMenu('text15', 'arrow15');" style="cursor: pointer;"><img id="arrow15" src="{$staticprefix}images/arrowright.gif"/> <b> The American Museum of Natural History's Science site</b></div></span>
                    <div id="text15" style="display: none;" class="textSwitch">
                       
                        <ul><li><a  href="http://www.amnh.org/science/">http://www.amnh.org/science/</a></li></ul>
                    </div>
                
                        
                <span><div id="text16trigger" onclick="switchMenu('text16', 'arrow16');" style="cursor: pointer;"><img id="arrow16" src="{$staticprefix}images/arrowright.gif"/> <b>Rainforest Alliance</b></div></span>
                        <div id="text16" style="display: none;" class="textSwitch">
                            <ul><li>  <a  href="http://www.rainforest-alliance.org/">http://www.rainforest-alliance.org/</a></li></ul>
                        </div>
                
                            
                <span><div id="text17trigger" onclick="switchMenu('text17', 'arrow17');" style="cursor: pointer;"><img id="arrow17" src="{$staticprefix}images/arrowright.gif"/> <b>The World Conservation Union</b></div></span>
                            <div id="text17" style="display: none;" class="textSwitch">
                                <ul><li><a  href="http://www.iucn.org/">http://www.iucn.org/</a> </li></ul>
                            </div>
                
                                
                <span><div id="text18trigger" onclick="switchMenu('text18', 'arrow18');" style="cursor: pointer;"><img id="arrow18" src="{$staticprefix}images/arrowright.gif"/> <b>Private Landowner Network</b></div></span>
                                <div id="text18" style="display: none;" class="textSwitch">
                                    <ul><li> <a  href="http://www.privatelandownernetwork.org/">http://www.privatelandownernetwork.org/</a></li></ul> 
                                </div>
                
                                    
                <span><div id="text19trigger" onclick="switchMenu('text19', 'arrow19');" style="cursor: pointer;"><img id="arrow19" src="{$staticprefix}images/arrowright.gif"/> <b>United Nations Envronment Programme's GRID-Arendal site</b></div></span>
                                    <div id="text19" style="display: none;" class="textSwitch">
                                        <ul><li>  <a  href="http://www.grida.no/">http://www.grida.no/</a></li></ul>
                                    </div>
                
                                        
                <span><div id="text20trigger" onclick="switchMenu('text20', 'arrow20');" style="cursor: pointer;"><img id="arrow20" src="{$staticprefix}images/arrowright.gif"/> <b>The GIS Portal Content</b></div></span>
                                        <div id="text20" style="display: none;" class="textSwitch">
        <span> Below is a collection of websites about conservation GIS that has been made available for searching.</span>
        <span> The current list is:</span>
        <ul><li><b> The Nature Conservancy's GIS Website:</b> <a  href="http://gis.example.com/">http://gis.example.com/</a> 
        </li><li><b> ESRI's Conservation Program Website: </b><a  href="http://www.conservationgis.org/">http://www.conservationgis.org/</a>
        </li><li><b> Inforain:</b> <a  href="http://www.inforain.org/">http://www.inforain.org/</a>
        </li><li><b> The Society for Conservation GIS:</b> <a  href="http://www.scgis.org/">http://www.scgis.org/</a>
        </li><li><b> RAMAS' GIS Website:</b> <a  href="http://www.ramas.com/consgis.htm">http://www.ramas.com/consgis.htm</a>
        </li><li><b> The Conservation GIS Consortium:</b> <a  href="http://www.pacificbio.org/conservation-gis-consortium/CGIS.html">http://www.pacificbio.org/conservation-gis-consortium/CGIS.html</a></li></ul>
                                        </div>
                
        <span>The internal search results will be displayed on the middle of the search page and the external search results will be displayed on the right-hand side of the page.</span>
                
            </div>
            
            <div id="text21trigger" onclick="switchMenu('text21', 'arrow21');" style="cursor: pointer;" class="help-content-head"><img id="arrow21" src="{$staticprefix}images/arrowright.gif"/> <b>Can I search other Conservation organizations?</b><a name="21"/></div>
            <div class="help-content-sub" id="text21" style="display: none;">

        <span>Yes. The search engine searches by default only ConserveOnline. If you want to search within the conservation sites or GIS Portal Content, select either from the dropdown list under the search area.</span>
            </div>
            
            <div id="text22trigger" onclick="switchMenu('text22', 'arrow22');" style="cursor: pointer;" class="help-content-head"><img id="arrow22" src="{$staticprefix}images/arrowright.gif"/> <b>Can I recommend other websites to search?</b><a name="22"/></div>
            <div class="help-content-sub" id="text22" style="display: none;">
                <span>Yes. Send us your recommendations using the Contact Us feedback link</span>
            </div>
            
            <div id="text23trigger" onclick="switchMenu('text23', 'arrow23');" style="cursor: pointer;" class="help-content-head"><img id="arrow23" src="{$staticprefix}images/arrowright.gif"/> <b>What are the Google results?</b><a name="23"/></div>
            <div class="help-content-sub" id="text23" style="display: none;">
                <span>When you perform a search, the search automatically queries Google for the terms you entered in the ConserveOnline search box. The top Google results are returned and displayed. Clicking on the Google logo will take you to the full Google results for your search.</span>
                </div>

  
            <br/>
            
            <div class="help-content-title">
                <h3>Library</h3>
                </div>
            
            <div id="text24trigger" onclick="switchMenu('text24', 'arrow24');" style="cursor: pointer;" class="help-content-head"><img id="arrow24" src="{$staticprefix}images/arrowright.gif"/> <b>What is the Library?</b><a name="24"/></div>
            <div class="help-content-sub" id="text24" style="display: none;">

        <span><p>The library is a formal place to publish your work. Once you post a file to the library, it is given a Digital Object Identifier (DOI), a unique permanent identifier given to an electronic document. DOIs do not change and they are associated with information about the document, such as the title, authors, topics etc. The associated information makes the documents easier for interested readers to find. By default, you will see the files posted in the library by the Search Terms but can always browse the library by Authors, Recently Added and All files.</p>
        <p>The screenshot below shows an example of the library by Search Terms:</p></span>
                <p><img src="{$staticprefix}images/FAQ01.jpg" border="0" alt="FAQ Screenshot"/></p>
                </div>
            
            <div id="text25trigger" onclick="switchMenu('text25', 'arrow25');" style="cursor: pointer;" class="help-content-head"><img id="arrow25" src="{$staticprefix}images/arrowright.gif"/> <b>What are the advantages of using the Library?</b><a name="25"/></div>
            <div class="help-content-sub" id="text25" style="display: none;">
        <span>The main advantage of using the library is the ability to look at the documents by Search Terms, Authors and Recently Added. In addition, the metadata has many advantages that makes the library feature valuable too. The metadata makes each Digital Object Identifier (DOI) a rich source of information that search engines can use to locate documents on the Internet. The metadata is all the information that is listed on the Add Library File page. See the frequently asked question for What is metadata and where is it entered in COL?</span>
            </div>
            
        <div id="text26trigger" onclick="switchMenu('text26', 'arrow26');" style="cursor: pointer;" class="help-content-head"><img id="arrow26" src="{$staticprefix}images/arrowright.gif"/> <b>What is a Digital Object Identifier (DOI)?</b><a name="26"/></div>
            <div class="help-content-sub" id="text26" style="display: none;">
        <span>A Digital Object Identifier (DOI) is a unique permanent identifier given to an electronic document. DOIs do not change and they are associated with information about the document, such as the title, authors, topics etc. The DOI that ConserveOnline issues is deposited in a central directory of DOIs of scholarly and research content. This directory is maintained by CrossRef (<a href="http://www.crossref.org" target="_blank">www.crossref.org</a>), a not-for-profit network founded on publisher collaboration, with a mandate to make reference linking throughout online scholarly literature efficient and reliable. Other publishers and librarians can then link to those DOIs, greatly increasing the visibility of your documents to search engines.</span>
            </div>
            
        <div id="text27trigger" onclick="switchMenu('text27', 'arrow27');" style="cursor: pointer;" class="help-content-head"><img id="arrow27" src="{$staticprefix}images/arrowright.gif"/> <b>How can I add a file to the Library?</b><a name="27"/></div>

            <div class="help-content-sub" id="text27" style="display: none;">
        <span>To add a file in the library:</span>
        <ul><li> Login to ConserveOnline.
        </li><li> Under the Library section on the homepage, click the add a file link on the right-side of the page.
        </li><li> The Add Library File page appears.
        </li><li> Fill out the information on the page. The descriptors on this page are considered metadata associated with your library and are searchable by the search engines.
        </li><li> Click Save.</li></ul>
        <span>The screenshot below shows an example of adding a file to the library:</span>
                <p align="center"><img src="{$staticprefix}images/FAQ02.jpg" border="0" alt="FAQ Screenshot"/></p>
                </div>
            
            <div id="text28trigger" onclick="switchMenu('text28', 'arrow28');" style="cursor: pointer;" class="help-content-head"><img id="arrow28" src="{$staticprefix}images/arrowright.gif"/> <b>What are Keywords?</b><a name="28"/></div>
            <div class="help-content-sub" id="text28" style="display: none;">
                
        <span><p><b>Keywords are used to describe and (similarly) organize files and pages in a workspace.</b> In migrated workspaces, they are initially set to the foldername in which a file or page was previously located. The workspace manager has the freedom to create the most appropriate and relevant keywords for use within each workspace. Keywords are only applicable within your workspace. Keywords are not used to search for information using a search engine.</p>
        <p>The advantages of using the specific keywords are:</p></span>
        <ul><li> It allows users to find the information they are looking for quickly.
        </li><li> It contains metadata. When documents are moved from the workspace to the library, they retain the metadata so the users don’t have to fill in the information again. </li></ul>
        <span>To enter a keyword:</span>
        <ul><li> Access your workspace.
        </li><li> Click Files &amp; Pages on the left-hand side menu.
        </li><li> The Browse All Files &amp; Pages page appears.
        </li><li> On the right-hand side of the screen, just below the green title bar, click on the blue Add Page or Add File button. 
        </li><li> The Add Page or Add File page appears. You can add keywords under the Keywords field.</li></ul>
        <span><p>Please note that a single keyword can be a phrase, for example: FDMT data model. You can also use more than one keyword, for example: FDMT, Data, Model.</p>
        <p>The screenshot below shows adding Keywords:</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ03.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        
        <div id="text29trigger" onclick="switchMenu('text29', 'arrow29');" style="cursor: pointer;" class="help-content-head"><img id="arrow29" src="{$staticprefix}images/arrowright.gif"/> <b>What are Search Terms?</b><a name="29"/></div>
            <div class="help-content-sub" id="text29" style="display: none;">
        <span><p>Search terms are used to index workspaces and files in the Library. They are author-created phrases that describe a workspace or a Library file.  Search Terms can be used to perform searches and to find library documents related to specific topics.</p>
        <p>The main advantage of using the specific Search Term is that it allows users to find the information they are looking for quickly.</p>
        <p>To enter a search term for a workspace:</p></span>
        <ul><li> Access your workspace.
        </li><li> Click Workspace Settings on the left-hand side menu.
        </li><li> The Workspace Settings page appears.
        </li><li> You can add search terms under the Other Search Terms field. </li></ul>
        <span><p>Please note that a search term can be a phrase, for example: FDMT data model. You can also use more than one search term to describe a document or page.</p>
        <p>The screenshot below shows adding Search Terms:</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ04.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        
        <div id="text30trigger" onclick="switchMenu('text30', 'arrow30');" style="cursor: pointer;" class="help-content-head"><img id="arrow30" src="{$staticprefix}images/arrowright.gif"/> <b>What is the difference between Keywords and Search Terms?</b><a name="30"/></div>
            <div class="help-content-sub" id="text30" style="display: none;">
        <span><p>A keyword is used to describe the file or page that you're creating in a workspace. A search term is used to describe a workspace or a file in a library. A keyword is not searchable by the search engine; however, search terms are searchable by the search engine.</p>
        <p><b>Tip: (to display on the Browse All Files &amp; Pages page as a quick tip)</b><br/>Keywords are mainly used to describe the file or page you're creating in a workspace.  Correct use of keywords will make it easier to browse for your file/page or identify what the file/page is meant to discuss.</p></span>
        </div>

           
           
           
            <br/>
    <div class="help-content-title">
                <h3>Workspaces</h3>
                </div>
    <div id="text31trigger" onclick="switchMenu('text31', 'arrow31');" style="cursor: pointer;" class="help-content-head"><img id="arrow31" src="{$staticprefix}images/arrowright.gif"/> <b>What is a Workspace?</b><a name="31"/></div>
            <div class="help-content-sub" id="text31" style="display: none;">
        <span><p>The workspace is the easiest way to make your work available on ConserveOnline. A workspace is a small website where you can post data, documents, images, maps etc. Using a workspace you can:</p></span>
        <ul><li> Create events calendar. 
        </li><li> Hold discussions.
        </li><li> Invite people with/without ConserveOnline membership to access your workspace.
        </li><li> Restrict the information to a group of collaborators or make it public.<br/></li></ul>
        <span><p>Please note that all documents that are available to the public will be accessible to search engines like Google.</p>
        <p>The screenshot below shows an example of a Workspace:</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ05.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        <div id="text32trigger" onclick="switchMenu('text32', 'arrow32');" style="cursor: pointer;" class="help-content-head"><img id="arrow32" src="{$staticprefix}images/arrowright.gif"/> <b>How Do I Join A Workspace?</b><a name="32"/></div>
            <div class="help-content-sub" id="text32" style="display: none;">
        <span><p>Each workspace is essentially a 'franchise' within ConserveOnline, and is independently owned and operated. To join a workspace you must contact the manager of that workspace.</p>
        <p>To join a workspace:</p></span>
        <ul><li> Login to ConserveOnline.
        </li><li> Select the Workspaces tab. 
        </li><li> The Browse My Workspaces page appears. By default, you will see your workspaces. 
        </li><li> You can browse for other workspaces by Countries, Search Terms or All Workspaces. 
        </li><li> Navigate to the name of the workspace that interests you.
        </li><li> The selected workspace home page appears. Click on the blue Join Workspace button on the right-hand side of the screen. Fill out the form and submit it to request permission to join the workspace. A request will be sent to the workspace manager, who will then approve or reject your request. You will get an e-mail or notification in your profile when your request is approved or rejected. </li></ul>
        </div>
        
        <div id="text33trigger" onclick="switchMenu('text33', 'arrow33');" style="cursor: pointer;" class="help-content-head"><img id="arrow33" src="{$staticprefix}images/arrowright.gif"/> <b>How can I change my Workspace homepage?</b><a name="33"/></div>
            <div class="help-content-sub" id="text33" style="display: none;">
        <span><p>To change your workspace homepage:</p></span>
        <ul><li> Access your workspace.
        </li><li> Click Workspace Settings on the left-hand side menu.
        </li><li> The Workspace Settings page appears. On this page, you can change the title of the workspace, icon and logo images and the associated metadata by altering the fields.<br/></li></ul>
        <span><p>In order to change the look of the homepage, you will need to use tool bar at the top of the content box that allows you to change the formatting of text, images, etc on the page.</p>
        <p>The screenshot below shows the use of the tool bar to edit the content.</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ06.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        
        <div id="text34trigger" onclick="switchMenu('text34', 'arrow34');" style="cursor: pointer;" class="help-content-head"><img id="arrow34" src="{$staticprefix}images/arrowright.gif"/> <b>How do I edit a page in my Workspace?</b><a name="34"/></div>
            <div class="help-content-sub" id="text34" style="display: none;">
        <span><p>In order to edit a page located under Files &amp; Pages:</p></span>
        <ul><li> Access your workspace.
        </li><li> Click Files and Pages on the left-hand side menu.
        </li><li> Navigate and click on the page you would like to edit.
        </li><li> Click the blue Edit button.
        </li><li> The Edit File page appears. 
        </li><li> Make desired changes and click Save.&nbsp;</li></ul>
        </div>
        
        <div id="text35trigger" onclick="switchMenu('text35', 'arrow35');" style="cursor: pointer;" class="help-content-head"><img id="arrow35" src="{$staticprefix}images/arrowright.gif"/> <b>What is metadata and where is it entered in COL?</b><a name="35"/></div>
            <div class="help-content-sub" id="text35" style="display: none;">
        <span><p>Metadata is a way of describing a file or a workspace in ConserveOnline. It is structured information that allows users to find and retrieve information quickly using descriptors rather than folders. In ConserveOnline, there are two types of metadata:</p></span>
        <ul><li> Searchable: Searchable means that you can use the Search box to find the information. 
        </li><li> Non-searchable: Non-searchable requires you to manually navigate to find the information.</li></ul>
        <span><p>The table below distinguishes between what is searchable and what is not.</p></span>
        <table border="1" cellpadding="2" cellspacing="0" align="center">
            <tbody>
                <tr bgcolor="#cccccc">
                    <td align="center">
                        <b>Searchable Metadata</b></td>
                    <td align="center"><b>Non-Searchable Metadata</b></td>
                </tr>
                <tr>
                    <td valign="top">
                        <ul><li> All Search Terms
                        </li><li> Workspace Settings Descriptors:
                            <ul><li> Workspace Name
                            </li><li> Biogeographic Realm
                            </li><li> Habitat Type
                            </li><li> Direct Threats
                            </li><li> Etc. </li></ul>
                        </li><li> Library File Descriptors:
                            <ul><li> Author
                            </li><li> Title
                            </li><li> All file content
                            </li><li> Etc. </li></ul>
                        </li></ul>
                    </td>
                    <td valign="top">
                        <ul><li>Workspace Files &amp; Pages Keywords</li></ul>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
        
        <div id="text36trigger" onclick="switchMenu('text36', 'arrow36');" style="cursor: pointer;" class="help-content-head"><img id="arrow36" src="{$staticprefix}images/arrowright.gif"/> <b>What is searchable in my Workspace?</b><a name="36"/></div>
            <div class="help-content-sub" id="text36" style="display: none;">
                
        <span><p>Everything except keywords in a workspace is searchable. The search engine will search the full text of every document and page in the workspace.</p></span>
        </div>
        
                <div id="text37trigger" onclick="switchMenu('text37', 'arrow37');" style="cursor: pointer;" class="help-content-head"><img id="arrow37" src="{$staticprefix}images/arrowright.gif"/> <b>Can I publish documents in my Workspace?</b><a name="37"/></div>
            <div class="help-content-sub" id="text37" style="display: none;">
        <span><p>Yes, you can move a file directly from your workspace to the library by viewing the properties of a file and pressing the blue Add to Library button. You can also post a document to the library by going to the Library tab and following the instructions for adding a file to the library.</p></span>
        </div>
        
         <div id="text38trigger" onclick="switchMenu('text38', 'arrow38');" style="cursor: pointer;" class="help-content-head"><img id="arrow38" src="{$staticprefix}images/arrowright.gif"/> <b>How do I add new members to Workspaces?</b><a name="38"/></div>
            <div class="help-content-sub" id="text38" style="display: none;">
        
        <span><p>If you create a workspace, you are automatically assigned as the workspace manager. To add new members:</p></span>
        <ul><li> Access your workspace.
        </li><li> Click Members on the left hand side menu.
        </li><li> The Manage Workspace Members page appears. You can invite new members to join your workspace by entering their email addresses in the Invite New Members box. You can also use the Search function to find ConserveOnline members by first and/or last name and then obtain their email address. When you have completed the list of people to invite, click the Invite Button below the box to send the invitations.</li></ul>
        <span><p>You can invite people to join your workspace; in addition, other members of ConserveOnline can contact you and request permission to join your workspace.</p>
        <p>Below is an example of adding new members to Workspace:</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ07.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        
        
        <div id="text39trigger" onclick="switchMenu('text39', 'arrow39');" style="cursor: pointer;" class="help-content-head"><img id="arrow39" src="{$staticprefix}images/arrowright.gif"/> <b>How do I create an event in a calendar?</b><a name="39"/></div>
            <div class="help-content-sub" id="text39" style="display: none;">
        <span><p>To create an event in a calendar:</p></span>
        <ul><li> Go to your workspace.
        </li><li> Click Calendar on the left hand side menu.
        </li><li> The Calendar page appears. On the right hand side of the screen, just below the green title bar, click on the blue Add Event button.
        </li><li> The Add Event page appears. Fill out the required information and then click Save to add an event.</li></ul>
        <span><p>Below is an example of adding an event:</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ08.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        
        <div id="text40trigger" onclick="switchMenu('text40', 'arrow40');" style="cursor: pointer;" class="help-content-head"><img id="arrow40" src="{$staticprefix}images/arrowright.gif"/> <b>How do I create a topic in a discussion?</b><a name="40"/></div>
            <div class="help-content-sub" id="text40" style="display: none;">
        
        <span><p>To create a topic in a discussion:</p></span>
        <ul><li> Go to your Workspace.
        </li><li> Click Discussions on the left hand side menu.
        </li><li> The Discussions page appears. On the right hand side of the screen, just below the green title bar, click on the blue Add Discussions button.
        </li><li> The Add Discussion page appears. Fill out the required information and then click Save to add a discussion topic.</li></ul>
        <span><p>Below is an example of adding an event:</p></span>
                <p align="center"><img src="{$staticprefix}images/FAQ09.jpg" border="0" alt="FAQ Screenshot"/></p>
        </div>
        
        <div id="text41trigger" onclick="switchMenu('text41', 'arrow41');" style="cursor: pointer;" class="help-content-head"><img id="arrow41" src="{$staticprefix}images/arrowright.gif"/> <b>What is the Workspace Settings tab?</b><a name="41"/></div>
            <div class="help-content-sub" id="text41" style="display: none;">
                
        <span><p>In your workspace, you will see a menu on the left hand side of the screen titled Workspace Home. The last item on the menu is called the Workspace Settings. This item appears in the workspace only if you are the owner of that workspace.</p>
        <p>Using the Workspace Settings tab the user can:</p></span>
        <ul><li> Change the name, description, and permissions (public/private) of your workspace.
        </li><li> Add an icon or logo.
        </li><li> Change the Biogeographic Realm, Habitat Type and other properties associated with your workspace.  These terms are considered metadata.  They are searchable by search engines.</li></ul>
        </div>
        
        <div id="text42trigger" onclick="switchMenu('text42', 'arrow42');" style="cursor: pointer;" class="help-content-head"><img id="arrow42" src="{$staticprefix}images/arrowright.gif"/> <b>What is the difference between searching and browsing in a Workspace?</b><a name="42"/></div>
            <div class="help-content-sub" id="text42" style="display: none;">
        <span><p>Search within a workspace uses a Google search engine.  It searches:</p></span>
        <ul><li> The full text of all documents in your workspace. 
        </li><li> Specific search terms for your workspace and its files/pages.</li></ul>
        <span><p>Note that Keywords associated with Files &amp; Pages are not included in the Google searching.</p>
        <p>Browsing within a workspace involves organizing files in a workspace using keywords.</p></span>
        <ul><li> Keywords are author-defined at the time a file or a page is uploaded into the workspace and it groups-together files based on their keywords, purposes, and authors.</li></ul>
        <span><p>Note that if your workspace was migrated from old ConserveOnline, the keyword for a file or page will default to the foldername it existed in (for the top two folder levels).  (Keywords can be added or changed by editing the file or page.)</p></span>
            </div>
        </div>
           

    </xsl:template>
</xsl:stylesheet>

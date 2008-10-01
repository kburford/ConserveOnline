<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY copy   "&#169;">
<!ENTITY nbsp   "&#160;">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <xsl:import href="../../shared/commontemplates.xsl"/>
    <xsl:output indent="yes"/>
    <xsl:template match="view[@name='view-workspace.html' and @type='workspace']">
        <div>
            <xsl:if test="/response/workspace/private='true'">
                <div class="profileHeader textCenter"> ** This is private. ** </div>
            </xsl:if>
            <div id="workspaceInfo">
                <div class="workspaceBrandingLogo">
                    <xsl:if test="not(/response/workspace/logo)">
                        <xsl:attribute name="class">workspaceBrandingLogo invisible</xsl:attribute>
                    </xsl:if>

                    <img src="{/response/workspace/logo/@src}" alt="Workspace Branding Logo"/>
                </div>
                <div>
                    <xsl:if test="not(/response/resource/content) and /response/workspace/logo">
                        <xsl:attribute name="style">height: 200px </xsl:attribute>
                    </xsl:if>
                    <p class="workspacePurpose">
                        <xsl:value-of select="/response/resource/description"/>
                    </p>
                    <xsl:apply-templates select="/response/resource/content/*" mode="copy"/>

                </div>
            </div>
            
            <xsl:variable name="gtwcurrurl" select="/response/breadcrumbs/entry/@href"/>
            <xsl:if test="((/response/workspace/@href !=concat($gtwcurrurl, '/workspaces/cbdgateway')) and (/response/workspace/@href !=concat($gtwcurrurl, '/workspaces/marine06documents'))) or (/response/user/isadmin[.='true'])">	

            <!-- XXX Kyle, insert keyword listing here -->
            <xsl:if test="/response/workspacekeywords">
                <div>
                    <table class="content-listing" id="kw-table">
                        <thead>
                            <tr>
                                <th class="cllabel">
                                    <a href="/server/url/to/sort/column"
                                        title=" Sort descending on Keyword">Keywords Associated with
                                            <xsl:value-of select="/response/workspace/title"/>
                                        Workspace</a>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="/response/workspacekeywords/keyword">
                                <tr>
                                    <xsl:attribute name="class">
                                        <xsl:choose>
                                            <xsl:when test="position() mod 2 = 1">odd</xsl:when>
                                            <xsl:otherwise>even</xsl:otherwise>
                                        </xsl:choose>
                                    </xsl:attribute>
                                    <td class="cllabel">
                                        <a href="{@href}">
                                            <xsl:value-of select="title"/>
                                        </a> (<xsl:value-of select="count"/>) <br/>
                                        <xsl:choose>
                                            <xsl:when test="description">
                                                <xsl:value-of select="description"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <em>No description found.</em>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>
                </div>
            </xsl:if>
            </xsl:if>
            
            <!--  Now show the taxonomy values -->
            <xsl:apply-templates select="../resource" mode="taxonomytable"/>

            <div class="clearBox clearBoth">&nbsp;</div>
        </div>

    </xsl:template>
    
    <xsl:template match="view[@name='subscribe.html' and @type='workspace']">
        <xsl:variable name="wsname" select="/response/resource/@href"/>
        
        
        <div>
            <div id="workspaceInfo">
               <p>The following RSS feeds are available for the <xsl:value-of select="/response/resource/title"/> workspace:</p>
       
                <div class="rss-box">
                    <h3>Looking To Receive<br/>ConserveOnline Updates?</h3>
                    <div class="rss-box-content">
                        You can receive notification by RSS or email when new ConserveOnline content is added that matches your selections. To get started, click <a href="/subscriptions/subscription.html">here</a>
or the "Subscribe" link in the top navigation bar.
                    </div>
                </div>
                
                <div class="nostyle">
                 <ul>
                     <li><img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
                         title="Get RSS"/> <a href="{$wsname}/@@feed-files-pages.xml ">Files &amp; Pages</a> </li>
                     
                     <li><img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
                         title="Get RSS"/> <a href="{$wsname}/@@feed-events.xml ">Calendar Events</a></li>
                     
                     <li><img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
                         title="Get RSS"/> <a href="{$wsname}/@@feed-discussions.xml">Discussion Board Postings</a></li>
                     
                     <li><img src="{$staticprefix}images/icoRSS_24.gif" alt="Get RSS"
                         title="Get RSS"/> <a href="{$wsname}/@@feed-all.xml">All Feeds (Files &amp; Pages, Calendar Events and Discussion Board Postings)</a></li>
                     </ul>
                     
                </div>
                
                <xsl:call-template name="rss-helper"/>
                </div>
            </div>
        
        
        
        
    </xsl:template>
    <xsl:template match="view[@name='view.html' and @type='workspaces']">
        <p>Temporary placeholder for viewing all workspaces. We will do the specification and
            implementation for this in a later iteration.</p>
        <ul>
            <li>
                <a href="/workspaces/qwertyu">Visit the "California Birds" test workspace</a>
            </li>
            <li>
                <a href="/workspaces/workspace-add-step1.html">Add a Workspace</a>
            </li>
        </ul>
    </xsl:template>
    <xsl:template match="view[@name='manage-members.html' and @type='workspace']">
        <form name="formInvite" action="" method="post">

            <div class="content">
                <xsl:if test="/response/messages/message">
                    <span class="fieldHelp">
                        <xsl:value-of select="/response/messages/message"/>
                    </span>
                </xsl:if>
                <div class="table3">
                    <h1>Invite New Members</h1>
                    <div id="MemberBoxRight">
                        <h1 id="options">More Options:</h1>
                        <table>
                            <tr>
                                <td>Search for ConserveOnline users</td>
                                <td>
                                    <input class="btnGreen btnGreenWidth95" type="button"
                                        value="Search" name="doSearch" id="doSearch"/>
                                </td>
                            </tr>
                            <!-- 
                                Note: These next two rows are for functionality that was 
                                triaged out of Evolution One.  I am leaving them in the DOM 
                                but commented out because the JS is expecting it.
                                Would be better to change the JS to not fail when the boxes are 
                                absent.
                            -->
                            <tr style="display:none">
                                <td>Copy names from another ConserveOnline workspace</td>
                                <td>
                                    <input class="btnGreen btnGreenWidth95" type="button"
                                        value="Copy From..." name="btnCopy" id="btnCopy"/>
                                </td>
                            </tr>
                            <tr style="display:none">
                                <td>Upload names from spreadsheet</td>
                                <td>
                                    <input class="btnGreen btnGreenWidth95" type="button"
                                        value="Upload" id="btnUpload"/>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div id="MemberBoxLeft">
                        <div>Enter the email address of each person you want to add (one address per
                            line).</div>
                        <div>
                            <textarea id="emailList" name="" rows="20" cols="10"/>
                        </div>
                        <div id="AddButton" align="right">
                            <input class="btnGreen btnGreenWidth83" type="button" id="addBtn"
                                value="Invite &gt;"/>
                        </div>

                    </div>


                </div>
                <div class="tabs1">

                    <div id="tab1Trigger" class="tab tabClose">
                        <a href="javascript:;" id="toggle1">
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Request
                            to Join (<span id="requestCount">&nbsp;</span>) </a>
                    </div>

                    <div id="tab1">
                        <div id="grid-request">
                            <div id="request-grid"/>
                        </div>
                        <input class="btnGreen btnGreenWidth130" type="button"
                            value="Accept As Member" name="Update" id="requestUpdate"
                        />&nbsp;&nbsp; <input class="btnGreen btnGreenWidth130"
                            type="button" value="Reject Application" name="Reject" id="rejectApp"
                        />&nbsp;&nbsp; </div>

                    <div id="tab2Trigger" class="tab tabClose">
                        <a href="javascript:;" id="toggle2">
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Outstanding
                            Invitations (<span id="outstandingInvites">&nbsp;</span>) </a>
                    </div>


                    <div id="tab2">
                        <div id="grid-outstanding">
                            <div id="outstanding-grid"/>
                        </div>
                        <input class="btnGreen btnGreenWidth95" type="button" value="Resend"
                            name="inviteResend" id="inviteResend"/>&nbsp;&nbsp; <input
                            class="btnGreen btnGreenWidth95" type="button" value="Remove"
                            name="inviteRemove" id="inviteRemove"/>
                    </div>

                    <div id="tab3Trigger" class="tab tabOpen">
                        <a href="javascript:;" id="toggle3">
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Members
                                (<span id="memberCount">&nbsp;</span>) </a>
                    </div>

                    <div id="tab3">
                        <div id="grid-member">
                            <div id="member-grid"/>
                        </div>
                        <input class="btnGreen btnGreenWidth95" type="button" value="Update"
                            name="Update" id="doUpdate"/>

                        <!-- manager flyover box -->
                        <div id="managerFlyover" class="libraryToolTip1">
                            <h1>Tip: Workspace Manager</h1>
                            <div>When this is selected, the person is allowed to add and remove
                                members, configure the workspace, and delete folders and documents
                                when necessary. Most workspaces should have more than one person to
                                share these manager responsibilities.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Search Box Dialog -->
            <div id="search-dlg" class="srchDlg">
                <div class="x-dlg-hd">Search for ConserveOnline Users</div>
                <div class="x-dlg-tab" title="Search">
                    <!-- Nested "inner-tab" to safely add padding -->
                    <div class="inner-tab">
                        <div>Type as much of the name as you know. For example: "Smith" or "J.
                            Smith"</div>
                        <div class="searchLine">Name: <input type="text" id="searchFor"/>
                            <input class="btnGreen btnGreenWidth95" type="button" value="Search"
                                name="runSearch" id="search-btn"/>
                        </div>
                        <div id="grid-panel">
                            <div id="editor-grid">&nbsp;</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Workspace Dialog -->

            <div id="copy-dlg">
                <div class="x-dlg-hd">Import from other workspaces.</div>
                <div class="x-dlg-tab" title="Import">
                    <!-- Nested "inner-tab" to safely add padding -->
                    <div class="inner-tab">
                        <div class="selectWG">Select workspace:&nbsp; <select id="selworkspace">
                                <option selected="selected">Loading workspaces</option>
                            </select>
                            <input class="btnGreen btnGreenWidth95" type="button" value="Search"
                                name="btnCopy" id="grabworkspace"/>
                        </div>
                        <div id="grid-panel2">
                            <div id="editor-grid2">&nbsp;</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- App Letter Flyover Box -->
            <div class="" id="appLetter"> </div>

            <!-- Tooltip Flyover Box -->
            <div class="tooltip" id="toolTip1">
                <div class="underline" id="box1">
                    <div>
                        <a href="javascript:tooltipUnPop();" id="closeTooltip">
                            <img id="closeImg" width="16px" height="16px"
                                src="../static/images/bulletDelete.gif" alt="close tooltip"/>
                        </a>
                    </div>
                    <div id="box2"> %img </div>
                    <div id="box6">
                        <div id="box7">%firstName %lastName</div>
                        <div>%loc</div>
                        <div>%org</div>
                    </div>
                </div>
                <div id="box3">Member of workspaces:</div>
                <div class="underline" id="box4"> %ws </div>
                <div>More about %firstName %lastName:</div>
                <div id="box5">
                    <a href="%history">Documents posted</a> | <a href="{../user/@href}"
                >Profile</a></div>
            </div>

            <!-- Upload Box Dialog -->
            <div id="upload-dlg">
                <div class="x-dlg-hd">Upload Spreadsheet</div>
                <div class="x-dlg-tab" title="Upload">
                    <!-- Nested "inner-tab" to safely add padding -->
                    <div class="inner-tab">
                        <div>Select the file to upload.</div>
                        <div class="searchLine">
                            <input type="file" id="uploadr"/>
                            <input class="btnGreen btnGreenWidth95" type="button" value="Upload"
                                name="runSearch" id="upload-btn"/>
                        </div>
                        <div id="grid-panel3">
                            <div id="editor-grid3">&nbsp;</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Confirmation / Status Dialog -->

            <input class="btnGreen btnGreenWidth95" type="hidden" value="Search" name="doSearch"
                id="status-btn"/>
            <div id="status-dlg">
                <div class="x-dlg-hd">Confirmation</div>
                <div class="x-dlg-bd">
                    <div class="x-dlg-tab" title="Status Messages">
                        <!-- Nested "inner-tab" to safely add padding -->
                        <div class="inner-tab">
                            <div class="statusMsg"><span id="namesAdded">&nbsp;</span> new
                                invitations sent.<hr class="sethr"/></div>
                            <div id="errorList">&nbsp;</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Rejection Letter Dialog -->

            <div id="reject-dlg">
                <div class="x-dlg-hd">Rejection Letter</div>
                <div class="x-dlg-bd">
                    <div class="x-dlg-tab" title="Rejection Letter">
                        <!-- Nested "inner-tab" to safely add padding -->
                        <div class="inner-tab">
                            <div id="formLetter">
                                <textarea id="rejectLetter" rows="60" cols="25" class="txtArea"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <!-- EXT UI scripts -->
            <script type="text/javascript"
                src="{$staticprefix}static/js/ext/adapter/yui/yui-utilities.js"/>
            <script type="text/javascript"
                src="{$staticprefix}js/ext/adapter/yui/ext-yui-adapter.js"/>
            <script type="text/javascript" src="{$staticprefix}js/ext/ext-all.js"/>

            <!-- COL resource library -->
            <script language="javascript" type="text/javascript"
                src="{$staticprefix}js/wsinvitations-manage.js"/>
            <div class="footer">
                <div class="left">
                    <div class="right">&nbsp;</div>
                </div>
            </div>
        </form>
    </xsl:template>
    <xsl:template match="view[@name='list-members.html' and @type='workspace']">
        <div> Your workspace has <span class="bold">
                <xsl:value-of select="../batch/@total"/>
            </span> member<xsl:if test="../batch/@total > 1 or ../batch/@total = 0">s</xsl:if>
        </div>
        <xsl:apply-templates select="../batch"/>
    </xsl:template>
    <xsl:template match="view[@name='add-joinrequest.html' and @type='workspace'] ">
        <div id="boxHeader">
            <div>Please review the information about you, which will be forwarded to the workspace
                manager, and write a brief message explaining why you would like to join.</div>
        </div>
        <xsl:apply-templates select="../formcontroller"/>
    </xsl:template>
    <xsl:template match="field[@name='form.reason']">
        <div class="box8">
            <div class="table1">
                <div class="left">
                    <h1>My Profile</h1>
                    <dl class="table2">
                        <xsl:for-each select="../../profile/about">
                            <dt>Name :</dt>
                            <!-- I added conditional statements to each form value so that if an element is missing from
                                // the XML, it doesn't break the layout. - Logan 7/30-->
                            <dd>
                                <xsl:choose>
                                    <xsl:when test="string(firstname) and string(lastname)">
                                        <xsl:value-of select="firstname"/>&nbsp; <xsl:value-of
                                            select="lastname"/>
                                    </xsl:when>
                                    <xsl:otherwise> &nbsp;</xsl:otherwise>
                                </xsl:choose>

                            </dd>
                            <dt>E-mail :</dt>
                            <dd>
                                <xsl:choose>
                                    <xsl:when test="string(email)">
                                        <xsl:value-of select="email"/>
                                    </xsl:when>
                                    <xsl:otherwise>&nbsp;</xsl:otherwise>
                                </xsl:choose>
                            </dd>
                            <dt>Region/Country :</dt>
                            <dd>
                                <xsl:choose>
                                    <xsl:when test="string(country)">
                                        <xsl:value-of select="country"/>
                                    </xsl:when>
                                    <xsl:otherwise>&nbsp;</xsl:otherwise>
                                </xsl:choose>
                            </dd>
                            <dt>Background :</dt>
                            <dd>
                                <xsl:choose>
                                    <xsl:when test="string(background)">
                                        <xsl:value-of select="background"/>
                                    </xsl:when>
                                    <xsl:otherwise>&nbsp;</xsl:otherwise>
                                </xsl:choose>
                            </dd>
                            <dt>Organization :</dt>
                            <dd>
                                <xsl:choose>
                                    <xsl:when test="string(organization)">
                                        <xsl:value-of select="organization"/>
                                    </xsl:when>
                                    <xsl:otherwise>&nbsp;</xsl:otherwise>
                                </xsl:choose>
                            </dd>
                        </xsl:for-each>
                    </dl>
                </div>
                <div class="right">
                    <div>
                        <xsl:choose>
                            <xsl:when test="error">
                                <span class="messageError">
                                    <xsl:value-of select="error"/>
                                </span>
                                <div>I would like to join the <strong>
                                        <xsl:value-of select="/response/workspace/title"/>
                                    </strong> workspace because:</div>
                                <textarea class="joinErrorTextarea" rows="10" cols="10"
                                    name="{@name}" id="{@name}"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <div>I would like to join the <strong>
                                        <xsl:value-of select="/response/workspace/title"/>
                                    </strong> workspace because:</div>
                                <textarea rows="10" cols="10" name="{@name}" id="{@name}"/>
                            </xsl:otherwise>
                        </xsl:choose>


                    </div>
                </div>
            </div>
        </div>
        <div style="clear: both;"/>
    </xsl:template>
    <xsl:template match="branding">
        <div class="workspaceHeader">
            <xsl:if test="@href !='' ">
                <a href="{@href}" class="workspaceBtn">Edit &gt;</a>
            </xsl:if> Workspace Branding Area </div>
        <div class="workspaceBrandingLogo">
            <img src="{graphic/@src}" width="150px" height="100px" alt="Workspace Logo"/>
        </div>
        <div class="workspaceBrandingText">
            <h1>
                <xsl:value-of select="../title"/>
            </h1>
            <p>
                <xsl:value-of select="description"/>
            </p>
        </div>
    </xsl:template>


</xsl:stylesheet>

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
    <xsl:template match="view[@name='logout.html' and @type='site']">
        <div id="logoutContent">
            <p>You have logged off of your ConserveOnline account. To sign in again, please provide
                your user name and password in the fields at the top of this screen and log in
                again.</p>
            <p>Thank you for using ConserveOnline!</p>
        </div>
    </xsl:template>

    <xsl:template match="view[@name='accept-invitation.html' and @type='people']">
        <div id="invitationContent">

            <p>Do you want to accept the invitation to join this workspace?</p>
            <div id="invitationInfo">
                <dl class="invitationListing">
                    <dt>Workspace:</dt>
                    <dd>
                        <xsl:apply-templates select="../resource/title"/>
                    </dd>
                    <dt>Invited By:</dt>
                    <dd>
                        <xsl:apply-templates select="../resource/manager"/>
                    </dd>
                </dl>
            </div>

            <div class="invitationBtnBox">
                <a href="{accept/@href}" class="blueBtn">Accept Invitation</a>
                <a href="{reject/@href}" class="greenBtn">Reject Invitation</a>
                <a href="{cancel/@href}" class="greenBtn">Cancel</a>
                <div class="clearBox"></div> <!--keeps the floating items from spilling out the bottom of the box-->
            </div>
        </div>
    </xsl:template>
    <xsl:template match="view[@name='login.html' and @type='site']">
        <div id="loginContent">
            <p>Please sign in to continue.</p>


            <div class="loginBox">
                <h3>Not a registered user yet?</h3>
                <p>Please register – it’s free.</p>
                <p>More explanation of why to become a member.</p>
                <a class="greenBtn loginRegisterBtn" href="{$urlprefix}register.html">Register</a>
            </div>
            <div class="loginBox">
                <h3>ConserveOnline Users</h3>
                    <xsl:choose>
                        <xsl:when test="failed">
                            <span class="messageError">Login information is incorrect</span>
                        </xsl:when>
                        <xsl:otherwise>
                            <p>Please sign in.</p>
                        </xsl:otherwise>
                    </xsl:choose>
                <form method="post" action="{@href}">
                    <input type="hidden" name="loginsubmitted" value="1" />
                    <div class="loginFormBox">
                        <input class="loginField" type="text" name="__ac_name" value="{failed/@username}" size="20"
                            maxlength="255"/>
                        <div>Username:</div>
                    </div>
                    <div class="loginFormBox">
                        <input class="loginField" type="password" name="__ac_password" value="" size="20"
                            maxlength="255"/>
                        <div>Password:</div>
                        <div class="loginFieldHelp">
                            <a href="/resetpassword.html">Forgot password?</a>
                        </div>
                    </div>
                    <input class="loginSignOnBtn btnGreen btnGreenWidth83" name="loginsubmitted"
                        type="submit" value="Sign In"/>
                </form>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="view[@name='add-registration.html']">
        <xsl:if test="invitation and not(../user)">
            <div id="registrationMessage">
                <p><strong>If you are already a registered user of ConserveOnline, please <a
                            href="/login.html">log in</a></strong>. Otherwise, complete this form to
                    register and accept your invitation to join the workspace.</p>

                <dl id="registrationWorkspaceInfo">
                    <dt class="registrationMessageLabel"> Workspace: </dt>
                    <dd>
                        <xsl:value-of select="invitation/workspace/@title"/>
                    </dd>
                    <dt class="registrationMessageLabel"> Invited by: </dt>
                    <dd>
                        <xsl:value-of select="invitation/inviter"/>
                    </dd>
                </dl>
            </div>
        </xsl:if>
        <xsl:apply-templates select="../formcontroller"/>
    </xsl:template>

    <xsl:template match="@widget[../@name='form.verificationcode']">
        <!-- Override this widget as we need the "Can't see the code" popup -->
        <input type="text" id="{../@name}" name="{../@name}" value="{../value}" size="40"
            maxlength="255"/>
    </xsl:template>


    <xsl:template match="field[@name='form.termsandconditions']">
        <div class="formFieldBox" id="div-{@name}">
            <xsl:attribute name="class">
                <xsl:choose>
                    <xsl:when test="error">
                        <xsl:text>errorField formFieldBox</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>formFieldBox</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <div class="formFieldSideLayout  formTC">
                <xsl:apply-templates select="error"/>
                <xsl:call-template name="disclaimer"/>
                <div class="formTC">
                    <input id="{@name}.used" name="{@name}.used" type="hidden" value=""/>
                    <input class="checkboxType" id="{@name}" name="{@name}" type="checkbox"
                        value="on">
                        <xsl:if test="value">
                            <xsl:attribute name="checked">checked</xsl:attribute>
                        </xsl:if>
                    </input>
                    <xsl:apply-templates select="@required"/>
                    <strong>I agree to the terms and conditions</strong>
                </div>
            </div>
            <div class="clearBox">&#160;</div>
        </div>
    </xsl:template>
    <xsl:template name="disclaimer">
        <div id="registrationDisclaimer">
            <P>September 17, 2007</P>
            <P><STRONG>PLEASE READ THIS AGREEMENT CAREFULLY; THIS IS A BINDING
                CONTRACT</STRONG>.&nbsp; This website (the "Website") is a service offered by
                The Nature Conservancy.&nbsp; This Terms of Use Agreement (the &ldquo;Terms
                of Use&rdquo; or &ldquo;Agreement&rdquo;) describes the terms and
                conditions applicable to your access and use of the Website and The Nature
                Conservancy&rsquo;s services.&nbsp; The Nature Conservancy may revise this
                Agreement at any time by posting the amended Terms of Use on the Website, and you
                agree that you will be bound by any changes to the Terms of Use.&nbsp; For your
                convenience, the date of last revision is included at the top of this
                page.&nbsp; The Nature Conservancy may make changes in the services described on
                the Website at any time.&nbsp; You understand that The Nature Conservancy may
                discontinue or restrict your use of the Website for any reason.&nbsp; </P>

            <P><STRONG>ABOUT THE INFORMATION ON THIS SITE</STRONG>.&nbsp; The content available
                on the Website is intended to be a general information resource and is provided
                solely on an &ldquo;AS IS&rdquo; and &ldquo;AS AVAILABLE&rdquo;
                basis.&nbsp; You are encouraged to confirm the information contained
                herein.&nbsp; You should not construe The Nature Conservancy's publication of
                the content on the Website as a warranty or guarantee of the quality or availability
                of any goods or services.
                <BR/>&nbsp;<BR/><STRONG>ELIGIBILITY</STRONG>.&nbsp; By using the Website,
                you represent and warrant that (a) all registration and other information you
                submit, if any, is truthful and accurate; (b) you will maintain the accuracy of any
                information you provide; (c) you will not submit any personal information if you are
                under 13 years of age; and (d) your use of the Website does not violate any
                applicable law or regulation. <BR/>&nbsp; <BR/><STRONG>USE OF MATERIALS ON THIS
                    SITE</STRONG>.&nbsp; The Nature Conservancy invites you to view and use a
                single copy of the materials obtained from this Website for your personal,
                non-commercial use. You agree not to license, distribute, create derivative works
                from, transfer, sell or re-sell any information, content, or services obtained from
                the Website; provided, however, that you may distribute or redistribute articles,
                messages and other narrative content posted to the Website by third parties only to
                the extent that you maintain (a) all copyright and trademark notices, (b)
                attribution of authorship to the extent available, and (c) the integrity of the
                content, i.e., the article, message or other narrative content must not be
                distributed except as a whole and must not be modified in any way.&nbsp; No
                graphics, photographs or other visual elements obtained through the Website may be
                used, copied, or distributed separate from the accompanying text without the prior
                express written consent of the original owner or The Nature Conservancy.&nbsp;
                You are not permitted to use the materials on this Website except as expressly set
                forth herein.&nbsp; You may not under any circumstances attempt to deface, shut
                down or otherwise damage the Website.</P>

            <P><STRONG>LINKS TO THIS SITE AND USE OF MARKS</STRONG>.&nbsp; The Website may
                contain links to websites operated by other parties.&nbsp; The Nature
                Conservancy provides these links to other websites as a convenience, and use of
                these sites is at your own risk.&nbsp; The linked sites are not under the
                control of The Nature Conservancy, and The Nature Conservancy is not responsible for
                the content available on the other sites.&nbsp; Such links do not imply The
                Nature Conservancy&rsquo;s endorsement of information or material on any other
                site and The Nature Conservancy disclaims all liability with regard to your access
                to and use of such linked Websites.&nbsp; </P>
            <P><STRONG>LINKS TO NATURE CONSERVANCY WEBSITES</STRONG>.&nbsp; Unless otherwise set
                forth in a written agreement between you and The Nature Conservancy, you must adhere
                to The Nature Conservancy&rsquo;s linking policy as follows:&nbsp; (i) the
                appearance, position and other aspects of the link may not be such as to damage or
                dilute the goodwill associated with The Nature Conservancy&rsquo;s names and
                trademarks, (ii) the appearance, position and other attributes of the link may not
                create the false appearance that your organization or entity is sponsored by,
                affiliated with, or associated with The Nature Conservancy, (iii) when selected by a
                user, the link must display the Website on full-screen and not within a
                &ldquo;frame&rdquo; on the linking Website, and (iv) The Nature Conservancy
                reserves the right to revoke its consent to the link at any time and in its sole
                discretion.&nbsp; Use of any of the Conservancy's logos, designs, images,
                photographs, slogans, trademarks or service marks in conjunction with the external
                links is not permitted.</P>

            <P><STRONG>TRADEMARKS</STRONG>.&nbsp; The Nature Conservancy, The Nature Conservancy
                &amp; Design, The Nature Conservancy Logos, Diversidata, Last Great Places, The
                Nature Conservancy International, Parks in Peril, Adopt An Acre, Rescue the Reef
                &amp; Design, Virginia Coast Reserve, America Verde, Wings of the Americas, TNC,
                example.com, and all other names of Nature Conservancy programs referenced herein are
                registered or common law trademarks of The Nature Conservancy in the United States.
                The Nature Conservancy and other trademarks are registered in several other
                countries, including without limitation Argentina, Australia, Bolivia, Brazil,
                Chile, Columbia, Costa Rica, Dominican Republic, Ecuador, France, Guatemala,
                Honduras, Hong Kong, Indonesia, Jamaica, Japan, Mexico, New Zealand, Nicaragua,
                Panama, Papua New Guinea, Paraguay, Peru, Philippines, Taiwan, and
                Venezuela.&nbsp; For more information, please contact The Nature Conservancy
                Legal Department at 4245 North Fairfax Drive, Arlington Virginia, 22203-1606
                USA.&nbsp; Unauthorized use of any Nature Conservancy trademark, service mark or
                logo may be a violation of federal and state law.</P>
            <P>DISCLAIMERS AND LIMITATION OF LIABILITY.&nbsp; ALL CONTENT ON THE WEBSITE IS
                PROVIDED TO YOU ON AN &ldquo;AS IS&rdquo; &ldquo;AS AVAILABLE&rdquo;
                BASIS WITHOUT WARRANTY OF ANY KIND EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT
                LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
                PURPOSE, AND NON-INFRINGEMENT.&nbsp; THE NATURE CONSERVANCY MAKES NO WARRANTY AS
                TO THE ACCURACY, COMPLETENESS OR RELIABILITY OF ANY CONTENT AVAILABLE THROUGH THE
                WEBSITE.&nbsp; YOU ARE RESPONSIBLE FOR VERIFYING ANY INFORMATION BEFORE RELYING
                ON IT.&nbsp; USE OF THE WEBSITE AND THE CONTENT AVAILABLE ON THE WEBSITE IS AT
                YOUR SOLE RISK.</P>

            <P>THE NATURE CONSERVANCY MAKES NO REPRESENTATIONS OR WARRANTIES THAT USE OF THE WEBSITE
                WILL BE UNINTERRUPTED OR ERROR-FREE.&nbsp; YOU ARE RESPONSIBLE FOR TAKING ALL
                NECESSARY PRECAUTIONS TO ENSURE THAT ANY CONTENT YOU MAY OBTAIN FROM THE WEBSITE IS
                FREE OF VIRUSES OR OTHER HARMFUL CODE.</P>
            <P>TO THE MAXIMUM EXTENT PERMITTED BY LAW, THE NATURE CONSERVANCY DISCLAIMS ALL
                LIABILITY, WHETHER BASED IN CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY
                OR OTHERWISE, AND FURTHER DISCLAIMS ALL LOSSES, INCLUDING WITHOUT LIMITATION
                INDIRECT, INCIDENTAL, CONSEQUENTIAL, OR SPECIAL DAMAGES ARISING OUT OF OR IN ANY WAY
                CONNECTED WITH ACCESS TO OR USE OF THE WEBSITE, EVEN IF THE NATURE CONSERVANCY HAS
                BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. </P>
            <P><STRONG>INDEMNITY</STRONG>.&nbsp; You agree to indemnify, defend and hold The
                Nature Conservancy, its subsidiaries, and affiliates, and their respective officers,
                agents, partners and employees, harmless from any loss, liability, claim, or demand,
                including reasonable attorneys' fees, due to or arising out of your use of the
                Website and/or breach of this Agreement.</P>
            <P><STRONG>COPYRIGHT</STRONG>. The Website is protected by U.S. and international
                copyright laws.&nbsp; Except for your use as authorized above, you may not
                modify, reproduce or distribute the content, design or layout of the Website, or
                individual sections of the content, design or layout of the Website, without The
                Nature Conservancy&rsquo;s express prior written permission.</P>
            <P><STRONG>NOTICE FOR CLAIMS OF COPYRIGHT INFRINGEMENT</STRONG>.&nbsp; If you are a
                copyright owner or agent thereof and believe that content posted on the Website by a
                Nature Conservancy user infringes upon your copyright, please submit notice,
                pursuant to the Digital Millennium Copyright Act (17 U.S.C. &sect; 512(c)) to
                our Copyright Agent with the following information: (a) an electronic or physical
                signature of the person authorized to act on behalf of the owner of the copyright;
                (b) a description of the copyrighted work that you claim has been infringed; (c) the
                URL of the location on our website containing the material that you claim is
                infringing; (d) your address, telephone number, and email address; (e) a statement
                by you that you have a good faith belief that the disputed use is not authorized by
                the copyright owner, its agent, or the law; and (f) a statement by you, made under
                penalty of perjury, that the above information in your notice is accurate and that
                you are the copyright owner or authorized to act on the copyright owner's
                behalf.&nbsp; Our Copyright Agent can be reached by mail at: The Nature
                Conservancy, ATTN: COPYRIGHT AGENT or SUSAN LAUSCHER, Legal Department, The Nature
                Conservancy, 4245 N. Fairfax Drive, Arlington, VA&nbsp; 22203-1606, USA, by
                phone at 1-703-841-4849, by fax at 1-703-841-0128, or by email at <A
                    href="mailto:slauscher@example.com">slauscher@example.com</A>.&nbsp; Please note
                that attachments cannot be accepted at the email address for security
                reasons.&nbsp; Accordingly, any notification of infringement submitted
                electronically with an attachment will not be received or processed.</P>

            <P><STRONG>LOCATION</STRONG>. The Website is operated by The Nature Conservancy from its
                offices in the United States.&nbsp; The Nature Conservancy makes no
                representation that the content of this Website is available or appropriate for use
                in other locations.&nbsp; Those who choose to access the Website from locations
                outside the United States do so on their own initiative and are responsible for
                compliance with applicable local laws.</P>
            <P><STRONG>CHILDREN</STRONG>.&nbsp; The Website is not directed toward children
                under 13 years of age nor does The Nature Conservancy knowingly collect information
                from children under 13.&nbsp; If you are under 13, please do not submit any
                personally identifiable information to The Nature Conservancy.</P>
            <P><STRONG>PRIVACY POLICY</STRONG>.&nbsp; By agreeing to these terms, you
                acknowledge that The Nature Conservancy may collect, use and disclose your
                information as described in our <A href="http://conserveonline.org/privacy">Privacy
                    Policy</A>. </P>

            <P><STRONG>USER CONTENT</STRONG>.&nbsp; By posting or providing any content on or
                through the Website, you hereby grant to The Nature Conservancy a worldwide,
                irrevocable, royalty-free, nonexclusive, limited license to reproduce, use, adapt,
                modify, publish, translate, publicly perform, publicly display, distribute and
                create derivative works from such content in any form, and The Nature Conservancy
                may sublicense all or part of its rights under this license or assign them to third
                parties.&nbsp; You represent and warrant that: (i) you own the content posted by
                you on or through the Website or otherwise have the right to grant the license set
                forth in this section, and (ii) the posting of your content on or through the
                Website does not violate the privacy rights, publicity rights, copyrights, contract
                rights or any other rights of any person.&nbsp; The Nature Conservancy may
                delete any content that in the sole judgment of The Nature Conservancy may be
                offensive, illegal or violate the rights, harm, or threaten the safety of any
                person.&nbsp; The Nature Conservancy has the right, but does not assume the
                responsibility, for monitoring the Website for inappropriate content.&nbsp; You
                are solely responsible for the content that you post on or through the
                Website.&nbsp; </P>
            <P><STRONG>SUBMISSIONS</STRONG>.&nbsp; It has been the long-standing policy of The
                Nature Conservancy not to accept or consider creative ideas, suggestions, or
                materials, including, but not limited to, notes, drawings, concepts, comments,
                questions or answers, techniques, know-how, or other information (hereinafter
                &ldquo;Submissions&rdquo;) other than those specifically requested. The
                intent of this policy is to avoid the possibility of future misunderstandings when
                projects developed by The Nature Conservancy's professional staff might seem to
                others to be similar to their own creative work.&nbsp; All Submissions,
                including unsolicited submissions and those made at the request of The Nature
                Conservancy, will be treated as non-confidential and non-proprietary, and will be
                subject to the license granted in the preceding paragraph. The Nature Conservancy
                will not be liable for any use or disclosure of any Submissions.</P>

            <P><STRONG>PASSWORD</STRONG>.&nbsp; You may be assigned a username and password with
                which to access restricted areas of the Website. You agree not to use the username
                or password of another user at any time or to disclose your password to any third
                party. You agree to notify The Nature Conservancy immediately if you suspect any
                unauthorized use of your username or access to your password.&nbsp; You are
                solely responsible for any and all uses of your username and password.</P>
            <P><STRONG>EMAIL</STRONG>.&nbsp; Email submissions over the internet may not be
                secure.&nbsp; Please do not email The Nature Conservancy any personal or
                confidential information.</P>
            <P><STRONG>CHOICE OF LAW/FORUM</STRONG>.&nbsp; All claims arising out of this
                Agreement or relating to the Website will be governed by the laws of the
                Commonwealth of Virginia, USA, excluding the application of its conflicts of law
                rules.&nbsp; Any legal action or proceeding arising out of this Agreement or
                relating to the Website shall be brought exclusively in a state or federal court in
                or for Arlington County, Virginia, USA.&nbsp; </P>

            <P><STRONG>MISCELLANEOUS</STRONG>. If any provision of this Agreement is held to be
                invalid or unenforceable, such provision shall be struck and the remaining
                provisions shall be enforced.&nbsp; Headings are for reference purposes only and
                in no way define, limit, construe or describe the scope or extent of such
                section.&nbsp; The Nature Conservancy&rsquo;s failure to act with respect to
                any failure by you or others to comply with these Terms of Use does not waive The
                Nature Conservancy&rsquo;s right to act with respect to subsequent or similar
                failures.&nbsp; These Terms of Use set forth the entire understanding and
                agreement between you and The Nature Conservancy with respect to the subject matter
                hereof.&nbsp; Any cause of action or claim you may have with respect to this
                Agreement or the Website must be commenced within six (6) months after the claim or
                cause of action arises or such claim or cause of action shall be barred.</P>
            <P><STRONG>VIOLATIONS AND ADDITIONAL POLICIES</STRONG>.&nbsp; The Nature Conservancy
                reserves the right to seek all remedies available at law and in equity for
                violations of this Agreement, including without limitation the right to block access
                from a particular Internet address.&nbsp;</P>
            <P>Copyright &copy; 2007 The Nature Conservancy.&nbsp; All rights reserved.<BR/></P>

        </div>
    </xsl:template>
</xsl:stylesheet>

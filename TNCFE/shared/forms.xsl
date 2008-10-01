<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xsl:stylesheet  [
<!ENTITY nbsp   "&#160;">
<!ENTITY copy   "&#169;">
]>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:import href="commontemplates.xsl"/>
	<xsl:strip-space elements="*"/>


	<!-- Formcontroler -->
	<xsl:template match="formcontroller">
		<!-- You can pass an optional parameter to indicate the layout of the 
			form. -->
		<xsl:param name="layout">beside</xsl:param>
		<!-- Handle form help.  To get form help on a screen, put a 
		xsl:template match="formcontroller[../view etc.] mode="formhelp" in 
		one of the per-type XSLT files. -->
		<xsl:apply-templates select="." mode="formhelp"/>
		<p class="textRequired">* = required</p>
		<form class="boxForm" action="{@action}" enctype="multipart/form-data" method="post">
			<xsl:apply-templates select="error"/>
			<xsl:apply-templates select="field">
				<xsl:with-param name="layout" select="$layout"/>
			</xsl:apply-templates>
			<xsl:apply-templates select="." mode="submit-block"/>
		</form>
	</xsl:template>

	<!-- match on all fields -->
	<xsl:template match="field">
		<xsl:param name="layout">beside</xsl:param>
		<!--
			This template is a dispatcher to the various elements that 
			get rendered in HTML for a form field.  Having this dispatcher 
			lets us customize cases where the layout is radically different, 
			simply byF making new template rules that override special 
			cases.
			
			Even this template can be customized to provide a different 
			dispatcher.  As such, think of this template rule as a 
			plug-point allowing FF "layouts" for fields: stacked, 
			one-line, no label, etc.
		-->

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
			<xsl:choose>
				<xsl:when test="$layout='beside'">
					<div class="formFieldSideLayout">
						<xsl:apply-templates select="error"/>
						<xsl:apply-templates select="@widget"/>
						<xsl:apply-templates select="description"/>
					</div>
					<div class="formLabelSideLayout">
						<xsl:apply-templates select="label"/>
					</div>
					<div class="clearBoxForm">&nbsp;</div>
				</xsl:when>
				<xsl:when test="$layout='stacked'">
					<xsl:apply-templates select="label" mode="stacked"/>
					<xsl:apply-templates select="error"/>
					<xsl:apply-templates select="@widget"/>
					<xsl:apply-templates select="description"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:apply-templates select="label"/>
					<xsl:apply-templates select="error"/>
					<xsl:apply-templates select="@widget"/>
					<xsl:apply-templates select="description"/>
				</xsl:otherwise>
			</xsl:choose>
		</div>
	</xsl:template>

	<!-- Form Action (submit ) -->
	<xsl:template match="formcontroller" mode="submit-block">
		<div class="formFieldBox" id="div-submit">
			<div class="formFieldSideLayout formButtons">
				<div>
					<xsl:for-each select="submit">
						<xsl:choose>
							<xsl:when test="position() = 1">
								<input class="btnGreen btnBlue83" name="{@name}" type="submit"
									value="{.}"/>
							</xsl:when>
							<xsl:when test="@name='description' ">
								<input class="btnGreen btnGreenWidth130" name="{@name}"
									type="submit" value="{.}"/>
							</xsl:when>
							<xsl:otherwise>
								<input class="btnGreen btnGreenWidth83" name="{@name}" type="submit"
									value="{.}"/>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:for-each>
				</div>
			</div>
			<div class="clearBox"> </div>
		</div>
	</xsl:template>
	


	<!--Authors Widget-->
	<xsl:template match="@widget[.='authors']">
		<div id="authors-container">
			<div id="first-author-box" class="subField">
				<input id="nameStaticId1" type="hidden" name="{../@name}" value="{../value/option[1]}" class="hidden"/>
				<span class="bold">First Name</span>
				<input type="text" name="{../@name}-firstname" value="" size="15" maxlength="255"/>
				<span class="bold">Last Name</span>
				<input type="text" name="{../@name}-lastname" value="" size="15" maxlength="255"/>
			</div>
			<div class="subField">
				<input id="nameStaticId2"  type="hidden" name="{../@name}" value="{../value/option[2]}" class="hidden"/>
				<span class="bold">First Name</span>
				<input type="text" name="{../@name}-firstname" value="" size="15" maxlength="255"/>
				<span class="bold">Last Name</span>
				<input type="text" name="{../@name}-lastname" value="" size="15" maxlength="255"/>
			</div>
			<xsl:if test="count(../value/option) > 3">
				<xsl:apply-templates select="../value/option[position() >= 3]" mode="authorField"/>
			</xsl:if>
			<div id="last-author-box" class="subField">
				<xsl:variable name="lastvalue">
					<xsl:choose>
						<xsl:when test="count(../value/option) >= 3">
							<xsl:value-of select="../value/option[last()]"/>
						</xsl:when>
					</xsl:choose>
				</xsl:variable>
				<input type="hidden" name="{../@name}" value="{$lastvalue}" class="hidden"/>
				<span class="bold">First Name</span>
				<input type="text" name="{../@name}-firstname" value="" size="15" maxlength="255"/>
				<span class="bold">Last Name</span>
				<input type="text" name="{../@name}-lastname" value="" size="15" maxlength="255"/>
				<input id="addNameBtn" class="btnGreen btnGreenWidth130 btnAuthors"
					onclick="colAddAuthor();" type="button"
					value="Add More Authors &gt;" name="submit"/>
			</div>
		</div>
	</xsl:template>
	<!-- Text Widget -->
	<xsl:template match="@widget[.='text']">
		<xsl:choose>
			<xsl:when test="../@name = 'form.dateauthored' ">
				<input type="text" id="{../@name}" name="{../@name}" value="{../value}" size="10"
					maxlength="10"/>
			</xsl:when>
			<xsl:when test="../@name='form.title' ">
				<input type="text" id="{../@name}" name="{../@name}" value="{../value}" size="60"
					maxlength="75"/>
			</xsl:when>
			<xsl:otherwise>
				<input type="text" id="{../@name}" name="{../@name}" value="{../value}" size="40"
					maxlength="255"/>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:if test="../@name = 'form.id'">
			
			<a href="{$staticprefix}html/address_popup.html"
				onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
				return false;">Questions?</a>
		</xsl:if>
		
		<xsl:if test="/response/view[@name='edit.html' and @type='profile']">
			
			<xsl:variable name="qstring" select="/response/formcontroller/@action"/>
			<xsl:variable name="qstring-edit" select="concat('/response/attachments/attachment@href',  '/report-recommendation.html?username=')" />
			<xsl:variable name="rec-count" select ="string-length($qstring-edit)"/>
			<xsl:variable name="rec-username" select="substring-after($qstring, '=')"/>
			
			<input type="hidden" name="userid" value="{$rec-username}"/>
			
		</xsl:if>
	</xsl:template>

	<!-- File upload -->
	<xsl:template match="@widget[.='upload']">
		<input type="file" id="{../@name}" name="{../@name}" size="{../@size}" maxlength="255"/>
	</xsl:template>

	<!-- Password Widget -->
	<xsl:template match="@widget[.='password']">
		<input type="password" id="{../@name}" name="{../@name}" value="{../value}" size="20"
			maxlength="255"/>
	</xsl:template>

	<!-- boolean -->
	<xsl:template match="@widget[.='boolean']">
		<input type="radio" id="{../@name}-true" name="{../@name}" value="true">Yes</input>
		<input type="radio" id="{../@name}-false" name="{../@name}" value="false">No</input>
	</xsl:template>

	<!-- checkbox -->
	<xsl:template match="@widget[.='checkbox']">
		<!-- XXX I suspect this no longer works -->
		<xsl:for-each select="../value/item">
			<input type="hidden" name="{@name}.used" id="{@name}.used"/>
			<input type="checkbox" id="{@name}" name="{@name}" value="{.}"/>
			<label for="{@name}">
				<xsl:value-of select="."/>
			</label>
		</xsl:for-each>
	</xsl:template>

	<!-- radiogroup -->
	<xsl:template match="@widget[.='radiogroup']">
		<div>
			<xsl:choose>
				<xsl:when test="../@name = 'form.rating'">
					
					<xsl:for-each select="../value/option">
						<input class="radRating" type="radio" id="{../../@name}" name="{../../@name}" value="{@value}" required="required">
							<xsl:if test="@selected">
								<xsl:attribute name="checked">checked</xsl:attribute>
							</xsl:if>
						</input>&nbsp;
						<span>
							<xsl:if test="@value!=0">
								<img src="{$staticprefix}images/stars_{@value}0.gif" alt="{@value} stars"></img>
							</xsl:if>
							<xsl:if test="@value=0">
								No Stars
							</xsl:if>
						</span>
						&nbsp;&nbsp;
					</xsl:for-each>
					
					
				</xsl:when>
				<xsl:when test="../@name = 'form.createdoi' ">
					<xsl:choose>
						<xsl:when test="/response/user/username='admin' or /response/user/username='admin2'">
							<input class="checkBox" type="radio" id="{../@name}" name="{../@name}" value="yes" >
								<xsl:if test="@selected">
									<xsl:attribute name="checked">checked</xsl:attribute>
								</xsl:if>
							</input>&nbsp;
							<span>
								Yes
							</span>&nbsp; &nbsp;
							<input class="checkBox" type="radio" id="{../@name}" name="{../@name}" value="no" checked="checked" >
								<xsl:if test="@selected">
									<xsl:attribute name="checked">checked</xsl:attribute>
								</xsl:if>
							</input>&nbsp;
							<span>
								No
							</span>
						</xsl:when>
						<xsl:otherwise>
							<input type="hidden" id="{../@name}" name="{../@name}" value="no" />
						</xsl:otherwise>
					</xsl:choose>
					
				</xsl:when>
				<xsl:when test="../@name='form.flagged'">
					
					<xsl:choose>
						<xsl:when test="/response/user/username='admin' or /response/user/username='admin2'">
							<input class="checkBox" type="radio" id="{../@name}" name="{../@name}" value="False" checked="checked">
								<xsl:if test="@selected">
									<xsl:attribute name="checked">checked</xsl:attribute>
								</xsl:if>
							</input>&nbsp;
							<span>
								No
							</span>&nbsp; &nbsp;
							<input class="checkBox" type="radio" id="{../@name}" name="{../@name}" value="True" >
								<xsl:if test="@selected">
									<xsl:attribute name="checked">checked</xsl:attribute>
								</xsl:if>
							</input>&nbsp;
							<span>
								Yes
							</span>
						</xsl:when>
						<xsl:otherwise>
							<input type="hidden" id="{../@name}" name="{../@name}" value="False" />
						</xsl:otherwise>
					</xsl:choose>
					
					
				</xsl:when>
				<xsl:otherwise>
					<xsl:for-each select="../value/option">
						<input class="checkBox" type="radio" id="{../../@name}" name="{../../@name}"
							value="{@value}">
							<xsl:if test="@selected">
								<xsl:attribute name="checked">checked</xsl:attribute>
							</xsl:if>
						</input>
						<span>
							<xsl:value-of select="."/>
						</span>
					</xsl:for-each>
				</xsl:otherwise>
			</xsl:choose>
			
			<xsl:if test="../@name = 'form.delivery_method'">
				
				<a href="{$staticprefix}html/rss_popup.html"
					onclick="window.open(this.href, 'popupwindow', 'width=500,height=300,scrollbars,resizable');
					return false;">What Is RSS?</a>
			</xsl:if>
		</div>
	</xsl:template>
	

	<!-- textarea widget -->
	<xsl:template match="@widget[.='textarea']">
		<xsl:if test="../@name = 'form.description' or ../@name = 'form.text'">
			<div id="charText"/>
		</xsl:if>
		<xsl:if test="../@name='form.text'">
			<xsl:variable name="qstring" select="/response/formcontroller/@action"/>
			<xsl:variable name="qstring-edit" select="concat('/response/attachments/attachment@href',  '/report-recommendation.html?username=')" />
			<xsl:variable name="rec-count" select ="string-length($qstring-edit)"/>
			<xsl:variable name="rec-username" select="substring-after($qstring, '=')"/>

		
			
			<input type="hidden" name="username" value="{$rec-username}" />
		</xsl:if>
		<textarea class="textareaWidget" rows="20" cols="10" name="{../@name}" id="{../@name}">
			<xsl:if test="../@name = 'form.description' or ../@name = 'form.text'">
				<xsl:attribute name="onkeydown">limitText(this,1000)</xsl:attribute>
				<xsl:attribute name="onblur">limitText(this,1000)</xsl:attribute>
				<xsl:attribute name="onkeyup">STATEMENT.charCount(this)</xsl:attribute>
			</xsl:if>
			<xsl:if test="../@name = 'form.attendees'">
				<xsl:attribute name="onkeydown">limitText(this,250)</xsl:attribute>
				<xsl:attribute name="onblur">limitText(this,250)</xsl:attribute>
			</xsl:if>
			<xsl:value-of select="../value"/>
		</textarea>
	</xsl:template>

	<!-- captcha widget -->
	<xsl:template match="@widget[.='captcha']">
		<input type="text" name="{../@name}" id="{../@name}"/>
		<img src="{../value/captcha/@href}" alt="Captcha Image" title="Captcha Image"/>
		<input type="hidden" name="{../@name}.hashkey" id="{../@name}.hashkey"
			value="{../value/captcha/@hashkey}"/>
	</xsl:template>

	<!-- file widget -->
	<xsl:template match="@widget[.='file']">
		<input type="file" id="{../@name}" name="{../@name}" size="20" value="{../value}"
			maxlength="255"/>
	</xsl:template>

	<!-- check box group widget -->
	<xsl:template match="@widget[.='checkboxgroup']">
		<xsl:variable name="value" select="../value"/>
		<xsl:variable name="fieldname" select="../@name"/>
		<xsl:variable name="gv" select="document('../shared/vocabularies.xml')"/>
		<xsl:variable name="thisvocab" select="$gv/vocabularies/vocabulary[@id=$value/@vocabulary]"/>
		<xsl:variable name="count" select="count($thisvocab/term)"/>
		<xsl:variable name="length">
			<xsl:value-of select="ceiling($count div 3)"/>
		</xsl:variable>
		<input type="hidden" name="{../@name}-empty-marker" value="1"/>
		<table class="checkBoxes">
			<tr>
				<td>
					<xsl:apply-templates select="$thisvocab/term[position() &lt;= $length]"
						mode="checkboxgroup">
						<xsl:with-param name="field" select="$fieldname"/>
						<xsl:with-param name="values" select="$value"/>
					</xsl:apply-templates>
				</td>
				<td>
					<xsl:apply-templates
						select="$thisvocab/term[position() > $length and position() &lt;= (2 * $length)]"
						mode="checkboxgroup">
						<xsl:with-param name="field" select="$fieldname"/>
						<xsl:with-param name="values" select="$value"/>
					</xsl:apply-templates>
				</td>
				<td>
					<xsl:apply-templates
						select="$thisvocab/term[position() > (2 * $length) and position() &lt;= (3 * $length)]"
						mode="checkboxgroup">
						<xsl:with-param name="field" select="$fieldname"/>
						<xsl:with-param name="values" select="$value"/>
					</xsl:apply-templates>
				</td>
			</tr>
		</table>
	</xsl:template>
	<xsl:template match="term" mode="checkboxgroup">
		<xsl:param name="field"/>
		<xsl:param name="values"/>
		<xsl:param name="boxname" select="@id"/>
		<div class="metadataBox">
			<div class="metadataLabels">
				<a title="{.}">
					<xsl:variable name="termlength">18</xsl:variable>
					<xsl:choose>
						<xsl:when test="string-length(.) &gt; $termlength"><xsl:value-of
								select="substring(.,1,$termlength)"/>...</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="."/>
						</xsl:otherwise>
					</xsl:choose>
				</a>
			</div>
			<div>
				<input class="checkBox" type="checkbox" name="{$field}" value="{$boxname}">
					<xsl:for-each select="$values/selected[@id=$boxname]">
						<xsl:attribute name="checked">checked</xsl:attribute>
					</xsl:for-each>
				</input>
			</div>
			<div class="clearBox">&nbsp;</div>
		</div>
	</xsl:template>

	<!-- selection widget -->
	<xsl:template match="@widget[.='selection']">
		<xsl:variable name="value" select="../value"/>
		<xsl:variable name="gv" select="document('../shared/vocabularies.xml')"/>
		<xsl:variable name="thisvocab" select="$gv/vocabularies/vocabulary[@id=$value/@vocabulary]"/>
		<select size="1" name="{../@name}" id="{../@name}">
                <xsl:choose>
                    <xsl:when test="../../../view/@name = 'subscription.html'">            
			<option value="">No Choice</option>
                    </xsl:when>
                    <xsl:otherwise>
			<option value="noselection"> -- Select Choice -- </option>
                    </xsl:otherwise>
                </xsl:choose>
			<xsl:for-each select="$thisvocab/term">
				<option value="{@id}">
					<xsl:if test="@id=$value">
						<xsl:attribute name="selected">selected</xsl:attribute>
					</xsl:if>
					<xsl:value-of select="."/>
				</option>
			</xsl:for-each>
		</select>
		<xsl:choose>
			<xsl:when test="../@name = 'form.biogeographic_realms'">
				
				
				<a href="{$staticprefix}html/realm_popup.html"
					onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
					return false;">?</a>
			</xsl:when>
			<xsl:when test="../@name = 'form.license'">
				
				
				<a href="{$staticprefix}html/license_popup.html"
					onclick="window.open(this.href, 'popupwindow', 'width=500,height=700,scrollbars,resizable');
					return false;">What Are These Licenses?</a>
			</xsl:when>
		</xsl:choose>
	</xsl:template>

	<!-- Editor Widget -->
	<xsl:template match="@widget[.='editor']">
		<textarea rows="20" cols="10" name="{../@name}" id="{../@name}" class="mceEditor">
			<xsl:apply-templates select="../../../quoted_reply"/>
			<xsl:apply-templates select="../value/*" mode="copy"/>
		</textarea>
	</xsl:template>

	<!-- Multiselect Widget -->
	<xsl:template match="@widget[.='multiselect']">
		<select multiple="multiple" name="{../@name}" id="{../@name}">
			<xsl:for-each select="../value/option">
				<option value="{@name}">
					<xsl:if test="@selected">
						<xsl:attribute name="selected">selected</xsl:attribute>
					</xsl:if>
					<xsl:value-of select="."/>
				</option>
			</xsl:for-each>
		</select>
	</xsl:template>

	<!-- Labels Widget -->
	<xsl:template match="@widget[.='labels']">
		<div id="labels-container">
			<div style="display:none" id="labels-list">
				<!-- A || separated list of all labels -->
				<xsl:for-each select="/response/keywords/item">
					<xsl:value-of select="."/>
					<xsl:if test="position() != last()">||</xsl:if>
				</xsl:for-each>
			</div>
			<div id="first-label-box" class="formFieldBox formSubField">
				<div class="labelInputField">
					<input type="text" name="{../@name}" id="form.labels" class="labelField"
						onblur="setTimeout(&quot;LABELS.trapBlur()&quot;,50); LABELS.elementFocus=0"
						onfocus="LABELS.elementFocus=1; LABELS.keySearch(this,event)"
						onkeyup="return LABELS.keySearch(this,event)" size="40" maxlength="50"
						value="{../value/option[1]}"/>
				</div>

				
				<a href="{$staticprefix}html/popup.html"
					onclick="window.open(this.href, 'popupwindow', 'width=500,height=500,scrollbars,resizable');
					return false;">What's This?</a>
			</div>
			<xsl:apply-templates select="../value/option[position() > 1]"/>

			<div class="formFieldBox" id="last-label-box">
				
				<xsl:variable name="lastvalue">
					<xsl:choose>
						<xsl:when test="count(../value/option) != 1">
							<xsl:value-of select="../value/option[last()]"/>
						</xsl:when>
					</xsl:choose>
				</xsl:variable>

				<div class="labelInputField">
					<input type="text" name="{../@name}" id="example-label" class="labelField"
						onblur="setTimeout(&quot;LABELS.trapBlur()&quot;,50); LABELS.elementFocus=0"
						onfocus="LABELS.elementFocus=1; LABELS.keySearch(this,event)"
						onkeyup="return LABELS.keySearch(this,event)" size="40" maxlength="50"
						value="{$lastvalue}"/>

				</div>
				<input id="addLabelsBtn" class="btnGreen btnGreenWidth130" type="button"
					onclick="LABELS.insertLabel(this)" value="Add More Keywords &gt;"/>

			</div>
		</div>
	</xsl:template>

	<xsl:template match="value/option">
		<xsl:if test="position() &lt; last()">
			<div class="formFieldBox">
				<input type="text" name="{../../@name}" id="labelStatic{position() + 1}"
					class="labelField"
					onblur="setTimeout(&quot;LABELS.trapBlur()&quot;,50); LABELS.elementFocus=0"
					onfocus="LABELS.elementFocus=1; LABELS.keySearch(this,event)"
					onkeyup="return LABELS.keySearch(this,event)" size="40" maxlength="50"
					value="{.}"/>
			</div>
		</xsl:if>

	</xsl:template>

	<xsl:template match="value/option" mode="authorField">
		<xsl:if test="position() &lt; last()">
			<div class="subField">
				<input type="hidden" class="hidden" id="nameStaticId{position() + 2}"
					name="{../@name}" value="{.}"/>
				<span class="bold">First Name</span>
				<input type="text" name="{../@name}-firstname" value="" size="15" maxlength="255"/>
				<span class="bold">Last Name</span>
				<input type="text" name="{../@name}-lastname" value="" size="15" maxlength="255"/>
			</div>
		</xsl:if>

	</xsl:template>

	<!-- workspace Action Wizard Step 4 -->
	<!-- TEMPORARY: this can be divided into two components: an AddWithOptions widget and a RemoveFromTable widget -->
	<xsl:template match="@widget[.='member-roster']">
		<script type="text/javascript" src="{$staticprefix}js/ext-1.0.1/extEnfold.js">
			<xsl:comment>YUI utilities and Ext</xsl:comment>
		</script>
		<script> var xmlData = []; </script>
		<input type="hidden" name="{@name}-marker" value="x"/>
		<div class="table3 memberBox">
			<h1 id="options">Add New Members</h1>
			<div id="MemberBoxRight">
				<h1 id="options">More Options:</h1>
				<div style="float:left">Search for ConserveOnline users</div>
				<div style="float:right">
					<input class="btnGreen btnGreenWidth95" type="button" value="Search"
						name="doSearch" id="doSearch"/>
				</div>
				<div style="clear:left;float:left">Copy the names from another <br/>ConserveOnline
					workspace</div>
				<div style="float:right">
					<input type="image" src="{$staticprefix}images/btnCopyFromGreen.gif"
						name="btnCopyFrom" id="btnCopyFrom" class="btnCopyFromGreen"
						onClick="return false"/>
				</div>
				<div style="clear:left;float:left">Upload the names from a spreadsheet</div>
				<div style="float:right">
					<input class="btnGreen btnGreenWidth95" type="button" value="Upload"
						name="doUpload" id="doUpload"/>
				</div>
			</div>
			<div id="MemberBoxLeft">
				<div>Enter the email address of each person you want to add (one address per line).</div>
				<div>
					<textarea id="emailList" name="" rows="20" cols="10"> </textarea>
				</div>
				<div id="AddButton" align="right">
					<input class="btnGreen btnGreenWidth83" type="button" id="addBtn"
						value="Add &gt;"/>
				</div>

			</div>
		</div>
		<div>
			<description for="allowParticipate">You are inviting <xsl:value-of
					select="../value/records/@count"/> people to join your workspace</description>
			<div id="grid-panel"
				style="padding: 0px; margin-top: 0px; margin-bottom: 0px; width:615px; height:300px;">
				<div id="editor-grid"/>
			</div>
		</div>
		<div>
			<input type="image" src="{$staticprefix}images/btnRemoveGreen.gif" name="btnRemove"
				id="btnRemove" class="btnRemoveGreen" onClick="return false"/>
		</div>
	</xsl:template>

	<!-- Templates Used for All Form Elements -->
	<!-- basically called by field template above -->

	<!-- Label Block -->
	<!-- A label may contain parenthetical descriptive text, as in "Name (up to 20 characters)" -->
	<xsl:template match="label">
		<label class="formLabel">
			<xsl:choose>
			<xsl:when test="../@name = 'form.createdoi' ">
				<xsl:if test="/response/user/username='admin' or /response/user/username='admin2'">
						<span>Register This DOI With Crossref?</span>
					</xsl:if>
				
			</xsl:when>
				<xsl:when test="../@name = 'form.flagged' ">
					<xsl:if test="/response/user/username='admin' or /response/user/username='admin2'">
						<span>Flag As Inappropriate?</span>
					</xsl:if>
					
				</xsl:when>
			<xsl:otherwise>
					<xsl:apply-templates select="../@required"/>
					<xsl:value-of select="."/>
			</xsl:otherwise>
			</xsl:choose>

		</label>
	</xsl:template>

	<xsl:template match="label" mode="stacked">
		<label class="formLabel labelStacked">
			<xsl:apply-templates select="../@required"/>
			<xsl:value-of select="."/>
		</label>
	</xsl:template>

	<!-- Required Icon -->
	<xsl:template match="@required">
		<span class="requiredIndicator">*</span>
	</xsl:template>

	<!-- Help Block -->
	<xsl:template match="description">
		<div class="fieldHelp">
			
			<xsl:choose>
				<xsl:when test="../@name = 'form.createdoi' ">
					<xsl:if test="/response/user/username='admin' or /response/user/username='admin2'">
						<span>Should this library file be registered with Crossref?</span>
					</xsl:if>
					
				</xsl:when>
				
				<xsl:otherwise>
					<xsl:apply-templates select="../@required"/>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</div>
	</xsl:template>

	<!-- Form error -->
	<xsl:template match="formcontroller/error">
		<div class="formError">
			<xsl:value-of select="."/>
		</div>
	</xsl:template>

	<!-- Field error -->

	<xsl:template match="field/error">
		<div>
			<span class="messageError">
				<xsl:value-of select="."/>
			</span>
		</div>
	</xsl:template>

	<xsl:template match="quoted_reply">
		<span class="quoteAuthor"><xsl:value-of select="author"/> wrote:</span>
		<div class="quoteBox">
			<xsl:apply-templates select="text/*" mode="copy"/>
		</div>
	</xsl:template>
	<xsl:template match="formcontroller" mode="formhelp">
		<!-- Do nothing.  These rules should be provided in screen handlers. -->
	</xsl:template>

</xsl:stylesheet>

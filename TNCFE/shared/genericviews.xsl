<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<!-- 
		
	View handlers when no other view handler matches 
	
	-->
	<xsl:template match="view">
		<p>You just experienced an error. It has been recorded and sent to the ConserveOnline administrator so you do not need to report this error.  Please be patient while we look into this problem and work to resolve the problem.  Thank you for using ConserveOnline.</p>
	</xsl:template>
	
	<xsl:template match="view[@name='notfound-error.html']">
		<p>The page that you attempted to view is not found. This likely is caused by a mistyped URL or an external site that is unavailable.  The URL of the page you sought has been recorded and sent to the ConserveOnline administrator so you do not need to report this error. Please be patient while we look into this problem and work to resolve the problem. Thank you for using ConserveOnline.</p>
	</xsl:template>
	
	<xsl:template match="view[@name='unauthorized-error.html']">
		<p>You have reached a private workspace of which you are not a member.  You can not request to join this workspace.</p>
	</xsl:template>
	
	<xsl:template match="view[@currenturl='accept-invitation.html']">
		<p>You are not authorized to view the requested page, probably because you have already responded to this workspace invitation.  Please contact  the workspace owner and request another invitation. The event has been recorded and sent to the ConserveOnline administrator so you do not need to report this error. Please be patient while we look into this problem and work to resolve the problem. Thank you for using ConserveOnline.</p>
	</xsl:template>
	

	<xsl:template match="view[../formcontroller or ../batch]">
		<xsl:apply-templates select="." mode="formhelp"/>
		<xsl:apply-templates select="../formcontroller|../batch"/>
	</xsl:template>
	<xsl:template match="view[@name='delete.html']">
		<div class="deleteMessage">
			<p>Do you really want to delete <strong>
					<xsl:value-of select="../resource/title"/>
				</strong><xsl:if test="@type='topic'"> and <em>all</em> of its comments </xsl:if>?</p>
			<div class="deleteButtonsWrapper">
				<a href="delete.html?confirm=1" class="context">
					<span>OK</span>
				</a>
				<a href="javascript:history.back()" class="standalone">
					<span>Cancel</span>
				</a>
			</div>

		</div>
	</xsl:template>
	
	<xsl:template match="view[@name='delete-recommendation.html' or @name='unsubscription.html']">
		<div class="deleteMessage">
			<p>Do you really want to delete <strong>
				<xsl:value-of select="../resource/title"/>
			</strong><xsl:if test="@type='topic'"> and <em>all</em> of its comments </xsl:if>?</p>
			<div class="deleteButtonsWrapper">
				<a href="delete-recommendation.html?confirm=1" class="context">
					<span>OK</span>
				</a>
				<a href="javascript:history.back()" class="standalone">
					<span>Cancel</span>
				</a>
			</div>
			
		</div>
	</xsl:template>
	<xsl:template match="@widget[.='custom' and ../@name='form.is_private']">
		<div>
			<span>
				<input class="checkBox" type="radio" id="form.is_private" name="form.is_private" value="public">
					<xsl:if test="not(../value) or ../value!='private'">
						<xsl:attribute name="checked">checked</xsl:attribute>
					</xsl:if>
				</input>
				No
			</span>
			<span style="margin-left: 10px">
				<input class="checkBox" type="radio" id="form.is_private.yes"
					name="form.is_private" value="private">
					<xsl:if test="../value='private'">
						<xsl:attribute name="checked">checked</xsl:attribute>
					</xsl:if>
				</input>
				Yes (only workspace members can see the file)
			</span>
		</div>
	</xsl:template>
	<xsl:template
		match="@widget[../@name='form.is_private' and /response/workspace/@is_private]">
		<!-- Don't show the Private? field if the workspace is private -->
	</xsl:template>

</xsl:stylesheet>

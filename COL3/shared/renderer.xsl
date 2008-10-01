<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml" version="1.0">
    <!-- 
    
    Generic rules when there is no matching screen handlers.
    
    -->
    <xsl:import href="genericviews.xsl"/>
    <xsl:import href="forms.xsl"/>
    <xsl:import href="theme.xsl"/>  

    <!-- 
    
    Screen handlers for all the types
    -->
    <xsl:import href="../types/calendar/calendar.xsl"/>
    <xsl:import href="../types/discussion/discussion.xsl"/>
    <xsl:import href="../types/profile/profile.xsl"/>
    <xsl:import href="../types/people/people.xsl"/>
    <xsl:import href="../types/documents/documents.xsl"/>
    <xsl:import href="../types/col/col.xsl"/>
    <xsl:import href="../types/workspace/workspace.xsl"/>
    <xsl:import href="../types/resetpassword/resetpassword.xsl"/>
    <xsl:import href="../types/library/libraryfile.xsl"/>    
    <xsl:import href="../types/gsa/gsa.xsl"/>
    <xsl:import href="../types/resetpassword/resetpassword.xsl"/>
    <xsl:output indent="yes" method="xml"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="/">
        <xsl:apply-templates select="response"/>
        <xsl:apply-templates select="GSP"/>
    </xsl:template>
</xsl:stylesheet>

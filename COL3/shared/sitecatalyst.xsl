<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:date="http://exslt.org/dates-and-times"
    exclude-result-prefixes="date" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:template name="sitecatalyst">
        <!-- SiteCatalyst code version: H.13.
             Copyright 1997-2007 Omniture, Inc. More info available at
             http://www.omniture.com -->
        <script language="JavaScript">
/* You may give each page an identifying name, server, and channel on the next lines. */
s.pageName=location.pathname
s.server=location.hostname
s.channel="<xsl:value-of select='view/@section'/>"
s.pageType="<xsl:value-of select='view/@type'/>"
s.prop1=""
s.prop2=""
s.prop3=""
s.prop4=""
s.prop5=""
s.prop6=""
s.prop7=""
s.prop8=""
s.prop9=""
s.prop10=""
s.prop11=""
s.prop12=""
s.prop13=""
s.prop14=""
s.prop15=""
s.prop16=""
/* Conversion Variables */
s.campaign=""
s.state=""
s.zip=""
s.events=""
s.products=""
s.purchaseID=""
s.eVar1=""
s.eVar2=""
s.eVar3=""
s.eVar4=""
s.eVar5=""
s.eVar6=""
s.eVar7=""
s.eVar8=""
s.eVar9=""
s.eVar10=""
s.eVar11=""
s.eVar12=""
/* Hierarchy Variables */
s.hier1=""
/************* DO NOT ALTER ANYTHING BELOW THIS LINE ! **************/
var s_code=s.t();if(s_code)document.write(s_code)//
        </script>
        <!-- End SiteCatalyst code version: H.13. -->

    </xsl:template>
</xsl:stylesheet>

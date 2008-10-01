<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:template
        match="formcontroller[../view/@name='reset-password.html' and ../view/@type='site']"
        mode="formhelp">
        <p class="formHelp">For security reasons your password will need to be reset. Please enter
            your username below. If you don't know your username please email the <a href="mailto:email@example.com">administrator</a>.</p>
    </xsl:template>

    <xsl:template match="view[@name='confirmreset-password.html' and @type='site']">
        <div class="formError">
            <span class="messageError">Password reset request sent.</span>
        </div>

        <p class="formHelp">Reset information sent to <code><xsl:value-of select="resetemail"/></code>. 
            Please check your email account for details on how to reset your password.</p>
    </xsl:template>

    <xsl:template
        match="formcontroller[../view/@name='completereset-password.html' and ../view/@type='site']"
        mode="formhelp">

        <p class="formHelp">Please provide a new password to reset your password.</p>
    </xsl:template>

</xsl:stylesheet>

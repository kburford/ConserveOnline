/**
CbD Gateway Navigation
 */
 
function writeGatewayNav() {

    var navContent = '<div id="gateway-navlink"><table width="600" border="0" cellpadding="0" cellspacing="0">'

    navContent += '<tr><td style="border-bottom: #ffffff 1px solid;">'    

    navContent += '<table width="100%" border="0" cellpadding="0" cellspacing="5"><tr>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center;"><span><a href="/workspaces/cbdgateway" title="Conservation by Design Gateway Homepage">Gateway Home</a></span></td>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/documents/global-conservation-science" title="Access to TNC&#8217;s global conservation science">Global Science</a></span></td>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/cap/index_html" title="Support for project-level conservation planning">Conservation Action Planning</a></span></td>'

    navContent += '<td style="text-align:center"><span><a href="/workspaces/cbdgateway/era/index_html" title="Support for regional conservation planning">Ecoregional Assessments</a></span></td>'

	navContent += '</tr></table></td></tr>'

	navContent += '<tr  bgcolor="#4e85c5"><td style="border-bottom: #ffffff 1px solid;"><table width="100%" border="0" cellpadding="0" cellspacing="2"><tr>'

	navContent += '<td width="140" style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/networks/index_html" title="Support for and access to conservation networks">Conservation Networks</a></span></td>'

	navContent += '<td width="100" style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/topics/index_html" title="Support organized by key habitats, threats or strategies">Special Topics</a></span></td>'

	navContent += '<td>&nbsp;</td>'

	navContent += '<td>&nbsp;</td>'

	navContent += '</tr></table></td></tr></table></div>'

	document.write(navContent)

	document.close()

}


function writeCAPNav() {

    var navContent = '<div id="gateway-lowernavlink"><table width="600" border="0" cellpadding="0" cellspacing="0">'

    navContent += '<tr><td style="border-bottom: #ffffff 1px solid;">'    

    navContent += '<table width="100%" border="0" cellpadding="0" cellspacing="5"><tr>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center;"><span><a href="/workspaces/cbdgateway/cap/practices/index_html">CAP Toolbox</a></span></td>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/cap/practices/cs/">Case Studies</a></span></td>'
	
    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/cap/resources/index_html">Resources</a></span></td>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/cap/efroymson_network/index_html">Efroymson Network</a></span></td>'
	
	navContent += '<td style="text-align:center"><span><a href="/workspaces/capcoaches/">CAP Coaches (login required) </a></span></td>'

	navContent += '</tr></table></td></tr></table></div>'

	document.write(navContent)

	document.close()

}



function writeERANav() {

    var navContent = '<div id="gateway-lowernavlink"><table width="600" border="0" cellpadding="0" cellspacing="0">'

    navContent += '<tr><td style="border-bottom: #ffffff 1px solid;">'    

    navContent += '<table width="100%" border="0" cellpadding="0" cellspacing="5"><tr>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center;" width="200"><span><a href="/workspaces/cbdgateway/era/standards/intro">ERA Toolbox</a></span></td>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center" width="200"><span><a href="/workspaces/cbdgateway/era/casestudies">Case Studies</a></span></td>'
	
	navContent += '<td width="300"> </td>'

	navContent += '</tr></table></td></tr></table></div>'

	document.write(navContent)

	document.close()

}



function writeConsNetNav() {

    var navContent = '<div id="gateway-lowernavlink"><table width="600" border="0" cellpadding="0" cellspacing="0">'

    navContent += '<tr><td style="border-bottom: #ffffff 1px solid;">'    

    navContent += '<table width="100%" border="0" cellpadding="0" cellspacing="5"><tr>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center;" width="150"><span><a href="/workspaces/cbdgateway/networks/standards/intro">Networks Toolbox</a></span></td>'
	
	navContent += '<td width="300"> </td>'

	navContent += '</tr></table></td></tr></table></div>'

	document.write(navContent)

	document.close()

}



function writeTopicsNav() {

    var navContent = '<div id="gateway-lowernavlink"><table width="600" border="0" cellpadding="0" cellspacing="0">'

    navContent += '<tr><td style="border-bottom: #ffffff 1px solid;">'    

    navContent += '<table width="100%" border="0" cellpadding="0" cellspacing="5"><tr>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center;"><span><a href="/workspaces/cbdgateway/topics/fire/index_html">Fire and Conservation</a></span></td>'

    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/topics/marine/index_html">Marine Conservation</a></span></td>'
	
    navContent += '<td style="border-right: #ffffff 1px solid; text-align:center"><span><a href="/workspaces/cbdgateway/documents/conservation-measures">Measures</a></span></td>'

    navContent += '<td width="200"> </td>'

	navContent += '</tr></table></td></tr></table></div>'

	document.write(navContent)

	document.close()

}

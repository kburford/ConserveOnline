function loadTinyMCE(){
   var workspace = false;

   try {
      if (document.location.href.match(/\/workspaces\//i)) {
         var workspace = document.location.href.split('/')[4];
      }
   } catch (e) {
   }
   var imgBtn = workspace ? "tnc_advimage," : "";

try {
    tinyMCE.init({
        theme: 'advanced',
        mode: 'textareas',
        editor_selector : "mceEditor",
        editor_deselector : "mceNoEditor",
        height: '400',
        width: '99%',
        submit_patch: true,
    	entity_encoding: "numeric",
        add_form_submit_trigger: true,
        add_unload_trigger: true,
        apply_source_formatting : true,
        strict_loading_mode: true,
        paste_create_paragraphs : false,
        paste_create_linebreaks : false,
        paste_use_dialog : true,
        paste_auto_cleanup_on_paste : true,
        paste_convert_middot_lists : false,
        paste_unindented_list_class : "unindentedList",
        paste_convert_headers_to_strong : true,
        theme_advanced_toolbar_location: 'top',
       // theme_advanced_buttons1: 'formatselect,bold,italic, bullist, numlist, link, code, removeformat, justifycenter, justifyleft,justifyright, justifyfull, indent, outdent, addwickedlink,delwickedlink',
        theme_advanced_buttons1: 'formatselect,bold,italic,'+imgBtn+'bullist, numlist, cite, link, unlink, code, removeformat, justifycenter, justifyleft,justifyright, justifyfull,sub,sup,pastetext,pasteword,selectall',
        theme_advanced_buttons2: '',
        theme_advanced_buttons3: '',
    	//plugins: 'paste,wicked',
    	plugins:"nbspfix,xhtmlxtras,advlink,"+imgBtn+"paste",
        //extended_valid_elements: "object[classid|codebase|width|height],param[name|value],embed[quality|type|pluginspage|width|height|src],a[name|href|target|title|onclick|rel],span[id|lang|dir],map[id,name],area[alt|coords|href|onmouseout|onmouseover|shape|title],small,ul[type],ol[type],hr[align|size|width],br[clear|style],table[border|frame|rules],th[bgcolor],col[span|width],colgroup[span|width]",
        //invalid_elements:'font[color|size],pre,address,textformat[blockindent|indent|leading|leftmargin|rightmargin|tabstops]',
        extended_valid_elements: '*[*]',
        invalid_elements: 'applet,embed,frame,iframe,input,object,param,textarea, !DOCTYPE,html,base,head,title,meta,link,style,body',
		save_callback: function (element_id, html, body) {
		    return "<div>" + html + "</div>";
		}
    });  
} catch(e) {
  //  logDebug("TinyMCE not available");
  alert(e);
}
}
loadTinyMCE();

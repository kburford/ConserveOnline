
/* Todo:

1] Code cleanup.
2] Move the grids into an array or an array of objects, all the grids are cluttering up the code.
3] Once the code is working with leo's scripts remove all the sample data code.
4] Get the tooltip code into the COL namespace.

*/


var	DEBUG=false;			// set to	false	to prevent simulated data	from being generated when	an ajax calls fail. 

URLPolicy = function () {  // Immediate
            var domain = document.location.href;

            // Private methods & properties
            var domainPolicy = function () {

               var url='';
               submitType='GET';
    
    
    // work here to add another case to fix issue  
    
               switch (true) {
                  // local file system 
                  case /^file:/i.test(domain)     	 : url="../types/!1/";
                                                       break;
                  
                  //svn file system
                  case /svn.enfold/i.test(domain) 	 : url="https://svn.enfoldsystems.com/clients/TNC/COL%203.0/tncfe/types/!1/";
                                                       break;
                  // dev system
                  case /dev\.tnc/i.test(domain)      : url='http://dev.tnc.enfoldsystems.com:82/workspaces/!1/';
                                                       submitType='POST';
                                                       break;
                  
                  // default (try relative)
                //  default                         	 : url='/types/!1/';
                default                                : url='/workspaces/'+workgroup+'/!1/';
                                                     	 break;
               }
               
               //for each argument passed to the function look for a
               //!x in the domain/path and substitute the passed argument.
               //so folder/!1/folder/!2/file.xml would replace !1 and !2 
               //with argument 0 and argument 1 respecitvely
               for(i=1; i<=arguments.length; i++) {
                  re = new RegExp('!'+i);
                  url = url.replace(re,arguments[i-1]);
               }
               return url;               
            }
             try {                  
                workgroup = /workspaces\/([^\/]+)\//.exec(document.location.href)[1];
             } catch(exc) {
                workgroup = 'wg1';
             }
             if (!workgroup) {workgroup='wg1';}
             var devEnv = true;
             if (/bjs\.enfold/i.test(domain)) {
                devEnv=true;
             }
             
                  
            return {
            
               // This area returns a public interface, the public methods and properties of the object.
               // .apply(this,arguments) passes the arguments of the current function to the new function.


               rejectRequests: function() {
                  var path=domainPolicy.apply(this,arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/rejectRequests');
                  } else {
                  	 return(path+'rejectRequests.xml');
                  }
                
               },
               acceptRequests: function() {
                  var path=domainPolicy.apply(this,arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/acceptRequests');
                  } else {
                  	 return(path+'acceptRequests.xml');
                  }
                
               },
               resend_invitations: function() {
                  var path=domainPolicy.apply(this,arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/resend-invitations.html');
                  } else {
                  	 return(path+'re-send-invitations.xml');
                  }
                
               },

               cancel_invitations: function() {
                  var path=domainPolicy.apply(this,arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/cancel-invitations.html');
                  } else {
                  	 return(path+'cancel-invitations.html.xml');
                  }
                
               },

               wsmember_listing : function () {
                  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/member-workspaces-listing.xml');
                  } else {
                  	 return(path+'workspace-list-groups.xml');
                  }
               },
            
               wsmember_searchbox : function () {
                  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/'+'member-search.xml');
                  } else {
                  	 return(path+'workspace-search-members.xml');
                  }
               },
               
               wsmember_managebox : function () {
                  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/workspace-members.xml');                                   
                  } else {
                  	 return(path+'workspace-list-members.xml');
                  }
               },
               manage_members : function () {
                  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/manage-workspace-members.html');                                   
                  } else {
                  	 return(path+'workspace-list-members.xml');
                  }
               },
               wsinvitations_manage : function () {
                  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/workspace-invitations.xml');                                   
                  } else {
                  return(path+'workspace-manage-invitations.xml');                                   
                  }
               },
               add_invitation : function() {
               	  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/add-invitation.html');                                   
                  } else {
               	     return(path+'add_invitation.html');
                  }
               },
               join_requests : function() {
               	  var path = domainPolicy.apply(this, arguments);
                  if (devEnv) {
                     return('/workspaces/'+workgroup+'/outstanding-joinrequests.xml');                                   
                  } else {
               	     return(path+'wsmembers-view.html');
                  }
               }
               
               
            }
}(); // IMMEDITE!!!!, this function executed as it's parsed.



function ajaxObject(url, callbackFunction) {
	var	that=this;			
	this.updating	=	false;
	this.abort = function()	{
		if (that.updating) {
			that.updating=false;
			that.AJAX.abort();
			that.AJAX=null;
		}
	}
	this.update	=	function(passData,postMethod)	{
		if (that.updating) { return	false; }
		that.AJAX	=	null;
	    if (window.XMLHttpRequest) {							
			   that.AJAX=new	XMLHttpRequest();							 
		   }	else {																	
			   that.AJAX=new	ActiveXObject("Microsoft.XMLHTTP");
		   }																							
           
        if (that.AJAX==null) {														 
			return false;																
		}	else {
			that.AJAX.onreadystatechange = function()	{	 
				if (that.AJAX.readyState==4) {						 
					that.updating=false;		
					XML=that.AJAX.responseXML;
					try {
   					if (DOMParser) {
                var parser = new DOMParser();
                var doc = parser.parseFromString(that.AJAX.responseText, "text/xml");          
                XML=doc;
             }
          } catch(err) {
   					XML=that.AJAX.responseXML;
          }
					that.callback(that.AJAX.responseText,that.AJAX.status,XML);	
					that.AJAX=null;																					
				}																											 
			}																												 
			that.updating	=	new	Date();		
			try {													 
			   if (/post/i.test(postMethod))	{
                    if (/\?/.test(urlCall)) {
                       urlWidget = '&';
                    } else {
                       urlWidget = '?';
                    }
					var	uri=urlCall+urlWidget+that.updating.getTime();
					that.AJAX.open("POST", uri,	true);
					that.AJAX.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
					that.AJAX.setRequestHeader("Content-Length", passData.length);
					that.AJAX.send(passData);
				}	else {
                    if (/\?/.test(urlCall)) {
                       urlWidget = '&';
                    } else {
                       urlWidget = '?';
                    }
					var	uri=urlCall+urlWidget+passData+'&timestamp='+(that.updating.getTime());	
					that.AJAX.open("GET",	uri, true);															
					that.AJAX.send(null);																					
				}
			}							 
			catch (e) {
               that.callback(null, 606, null);
               
			}
			return true;																						 
		}																																						
	}
	var	urlCall	=	url;				
	this.callback	=	callbackFunction ||	function ()	{	};
}


// Define	the	COL	namespace.	 

var	COL	=	function ()	{

	 /*	Private	properties and methods!	*/
	 
	 /*	The	basic	item record	used by	all	the	"data	store" objects.	*/
	 
	 var managerChange=false;
	 var Member	=	Ext.data.Record.create([
			{name: 'add',	type:	'string'},
			{name: 'firstName',	type:	'string'},
			{name: 'lastName', type: 'string'},
			{name: 'email',	type:	'string'},
			{name: 'remove', type: 'string'},
			{name: 'manager',	type:	'string'},
			{name: 'date',	type: 'string'},
            {name: 'iid', type: 'string'},
            {name: 'uid', type: 'string'},
            {name: 'omgr', type: 'boolean'},
			{name: 'id', type: 'string'}
	 ]);

	 var global_index=0; //	This is	an index counter,	it maintains a unique	number
											 //	assigned to	each table row created.
	 

	//	RESERVED FOR AN	ARRAY	OF DATA	TO INCLUDE IN	TABLE	GRID
	var	xmlData	=	[];

		// create	the	Data Store
		// DS	=	master submit	list.
		// DS2=	workgroup	list
		// DS3=	items	to be	imported from	workgroup	list (to be	plugged	into DS)
		// DS4=	"Members grid"
		
	var	ds = new Ext.data.Store({
						proxy: new Ext.data.MemoryProxy(xmlData),
						reader:	new	Ext.data.ArrayReader({}, Member)
				});
	
	var	ds2	=	new	Ext.data.Store({
						proxy: new Ext.data.MemoryProxy(xmlData),
						reader:	new	Ext.data.ArrayReader({}, Member)
				});

	var	ds3	=	new	Ext.data.Store({
						proxy: new Ext.data.MemoryProxy(xmlData),
						reader:	new	Ext.data.ArrayReader({}, Member)
				});
	
	var	ds4	=	new	Ext.data.Store({
						proxy: new Ext.data.MemoryProxy(xmlData),
						reader:	new	Ext.data.ArrayReader({}, Member)
				});
	
	var	ds5	=	new	Ext.data.Store({
						proxy: new Ext.data.MemoryProxy(xmlData),
						reader:	new	Ext.data.ArrayReader({}, Member)
				});
	
	var	ds6	=	new	Ext.data.Store({
						proxy: new Ext.data.MemoryProxy(xmlData),
						reader:	new	Ext.data.ArrayReader({}, Member)
				});
	

	 //	the	column model has information about grid	columns
	 //	dataIndex	maps the column	to the specific	data field in
	 //	the	data store (created	below)
	 var fm	=	Ext.form,	Ed = Ext.grid.GridEditor;	 
	 var cm	=	new	Ext.grid.ColumnModel([{
							 header: "<center>Add</center>",
							 dataIndex:	'add',
							 sortable: false,
							 width:	70
						},{	 
							 header: "First	Name",
							 dataIndex:	'firstName',
							 width:	150
						},{
							 header: "Last Name",
							 dataIndex:	'lastName',
							 width:	150
						},{
							 header: "E-Mail Address",
							 dataIndex:	'email',
							 width:	220
						}]);

		// by	default	columns	are	sortable
		cm.defaultSortable = true;
	 var cm2 = new Ext.grid.ColumnModel([{
							 header: "<center>Add</center>",
							 dataIndex:	'add',
							 sortable: false,
							 width:	70
						},{	 
							 header: "First	Name",
							 dataIndex:	'firstName',
							 width:	150
						},{
							 header: "Last Name",
							 dataIndex:	'lastName',
							 width:	150
						},{
							 header: "E-Mail Address",
							 dataIndex:	'email',
							 width:	220
						}]);
		cm2.defaultSortable	=	true;

	 var cm3 = new Ext.grid.ColumnModel([{
							 header: "<center>Add</center>",
							 dataIndex:	'add',
							 sortable: false,
							 width:	70
						},{	 
							 header: "First	Name",
							 dataIndex:	'firstName',
							 width:	150
						},{
							 header: "Last Name",
							 dataIndex:	'lastName',
							 width:	150
						},{
							 header: "E-Mail Address",
							 dataIndex:	'email',
							 width:	220
						}]);
		cm3.defaultSortable	=	true;

		
		//members	grid
		 var gridWidth = document.getElementById('grid-member');
		 if	(gridWidth)	{
				gridWidth	=	document.getElementById('grid-member').offsetWidth;
		 
				var	cm4	=	new	Ext.grid.ColumnModel([{
									header:	"<center>Remove</center>",
									dataIndex: 'remove',
								 sortable: false,
									width: Math.floor(gridWidth*.10)
							},{
									header:	"First Name",
									dataIndex: 'firstName',
									width: Math.floor(gridWidth*.25)
							 },{
									header:	"Last	Name",
									dataIndex: 'lastName',
									width: Math.floor(gridWidth*.25)
							 },{
									header:	"E-Mail	Address",
									dataIndex: 'email',
									width: Math.floor(gridWidth*.25)
							},{
								  header: '<center>Manager	<span	onMouseOver="COL.flyover(event)" onMouseOut="COL.flyout()"><img	src="/static/images/bulletInfo.gif"	alt="" border="0"/></span></center>',
									dataIndex: 'manager',
								  sortable: false,
									width: Math.floor(gridWidth*.10)
							 }]);

			 cm4.defaultSortable = true;
 	  } // if grid width


	 //	create the editor	grid

	 var grid	=	{};
	 var layout	=	{};
	 var grid2 = {};
	 var layout2=	{};
	 var grid3 = {};
	 var layout3=	{};
	 var grid4 = false;
	 var layout4=	{};
	 var grid5 = false;
	 var layout5=	{};
	 var grid6 = false;
	 var layout6=	{};

					 

/* End Private Area	*/																						
/* RETURN	PUBLIC INTERFACE */
											 
	 return	{
	 	
        
        inviteStateCheck: function(idx) {
            setState = function(rec) {
               if (rec.data.id==idx) {
                  rbox=document.getElementById('removex'+idx);
                  if (rbox.checked) {
                     ischecked='checked';
                  } else {
                     ischecked='';
                  }
                  rec.data.remove='<center><input type="checkbox" '+ischecked+' class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')" id="removex'+idx+'"></center>';
               }
            }

            ds5.each(setState);
            ds5.commitChanges() 
        },


         flagManagerChange : function() {
           COL.managerChange=true;  
         },

         verifyCheckBox: function(idx) {
	 	  	
	 	  	// All this function does is make sure both the manager and remove checkboxes aren't simultaniously checked.
	 	  	// Remove is disallowed if manager is checked. 
            
            setState = function(rec) {
               if (rec.data.id==idx) {
                  if (mbox) {
                     if (mbox.checked) {
                        ischecked1='checked';
                     } else {
                        ischecked1='';
                     }
                  }
                  if (rbox.checked) {
                     ischecked2='checked';
                  } else {
                     ischecked2='';
                  }
                  if (mbox) {
                     rec.data.manager='<center><input type="checkbox" '+ischecked1+' class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')"	id="manager'+idx+'"></center>'
                  }
                  rec.data.remove='<center><input type="checkbox" '+ischecked2+' class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')" id="removex'+idx+'"></center>';
               }
            }
	 	  	
	 	  	 mbox = document.getElementById('manager'+idx);
	 	  	 rbox = document.getElementById('removex'+idx);
	 	  	 if (mbox) {
	 	  	 	  if (mbox.checked) {
	 	  	 	     rbox.checked=false;
	 	  	 	  }
	 	  	 }
             ds4.each(setState);
 	         ds4.commitChanges() 
             ds5.each(setState);
 	         ds5.commitChanges() 
             ds6.each(setState);
 	         ds6.commitChanges() 
         },
	 	
			flyover: function(Event) {
				 // handles the "manager information" popup when mouse moves over the (i) graphic in tab header.
				 tooltipUnPop();
				 COL.flyout();
				 COL.appFlyout();
				 divId=document.getElementById('managerFlyover');
				 divId.style.left=Event.clientX-100+'px';
				 var scrollTop = 0;
				 if	(document.documentElement	&& document.documentElement.scrollTop)
						scrollTop	=	document.documentElement.scrollTop;
				 else	if (document.body)
						scrollTop	=	document.body.scrollTop				 
				 divId.style.display='block';
				 var offset=(scrollTop+Event.clientY)-(divId.offsetHeight+25);
         if (offset<document.documentElement.scrollTop) {
   	        offset=document.documentElement.scrollTop+Event.clientY+10;
         }
				 divId.style.top=offset+'px';
				 
			},

			flyout : function()	{
				 // handles the "manager information" popup when mouse moves over the (i) graphic in tab header.
				 divId=document.getElementById('managerFlyover');
				 divId.style.display='none';
			},
			
			appFlyover: function(Event,fname,lname,email,msg) {
				 // handles the applicant information when the mouse moves over the application information graphic
				 // in the request to join grid.
				 tooltipUnPop();
				 COL.flyout();
				 COL.appFlyout();
				 divId=document.getElementById('appLetter');
				 divId.innerHTML= '<strong>'+fname+' '+lname + '</strong> &nbsp; ( <A HREF="mailto:'+email+'">'+email+'</a> )<HR>'+msg;
				 divId.style.left=Event.clientX-625+'px';
				 var scrollTop = 0;
				 if	(document.documentElement	&& document.documentElement.scrollTop)
						scrollTop	=	document.documentElement.scrollTop;
				 else	if (document.body)
						scrollTop	=	document.body.scrollTop				 
				 divId.style.display='block';
				 var offset=(scrollTop+Event.clientY)-(divId.offsetHeight+25);
         if (offset<document.documentElement.scrollTop) {
   	        offset=document.documentElement.scrollTop+Event.clientY+10;
         }
				 divId.style.top=offset+'px';
				 
			},

			appFlyout : function()	{
				 // handles the applicant information when the mouse moves over the application information graphic
				 // in the request to join grid.
				 divId=document.getElementById('appLetter');
				 divId.style.display='none';
			},
			
			// User clicked the update button
			updateMembers	:	function() {
					 var totManagers=0;
                     var demote='';
                     var promote='';
                     var remove='';
					 
					 var removeMembers = function(rec) {
							id = rec.data.id;
							if (document.getElementById('removex'+id).checked) {
								if (!document.getElementById('manager'+id).checked) {
                                   remove+=rec.data.uid+',';
							    } else {
							  	 totRecs++;
							    }
						    } else {
							     totRecs++;
							}
                            currMgr = document.getElementById('manager'+id).checked;
                            if (currMgr != rec.data.omgr) {
                               if (currMgr) {
                                  promote+=rec.data.uid+',';
                               } else {
                                  demote+=rec.data.uid+',';
                               }
                            }

					 }
					 
					 var checkManager	=	function(rec)	{
							var	id = rec.data.id;
							if (document.getElementById('manager'+id).checked) {
								totManagers++;
							}
					 }

					 ds4.each(checkManager);
           var totRecs=0;
					 if	(totManagers < 1)	{
							Ext.MessageBox.alert('Error	Message',	'This	workspace	must have	at least ONE manager.	 Please	select a new manager and try to	update again.');	
					 } else	{
							 ds4.each(removeMembers);
				             document.getElementById('memberCount').innerHTML=totRecs;
                             remove=remove.replace(/,$/,'');
                             promote=promote.replace(/,$/,'');
                             demote=demote.replace(/,$/,'');
                             var submitstr="form.promoteMembers="+encodeURIComponent(promote);
                                 submitstr+="&form.demoteMembers="+encodeURIComponent(demote);
                                 submitstr+="&form.removeMembers="+encodeURIComponent(remove);
                                 submitstr+="&form.actions.manageMembership="+encodeURIComponent('Manage Membership');

                             if (COL.managerChange) {
                                 var cb= function() {document.location.reload();};
                             } else {
                                 var cb= COL.reloadMembers;
                             }
                             var submitManage = new ajaxObject(URLPolicy.manage_members(),cb);
                             submitManage.update(submitstr,submitType);
					 }
					 
			},
            
            reloadMembers: function() {
                document.getElementById('memberCount').innerHTML='<img src="/static/images/progress.gif" width="10" height="10" alt="ajax activity">';
    			 getMembersAjax	=	new	ajaxObject(URLPolicy.wsmember_managebox('workspace'),	COL.populateMembers);										 
				 getMembersAjax.update();
            },            
            reloadRequests: function() {
				document.getElementById('requestCount').innerHTML='<img src="/static/images/progress.gif" width="10" height="10" alt="ajax activity">';
                getRequestAjax	=	new	ajaxObject(URLPolicy.join_requests('workspace'),	COL.populateRequest);										 
                getRequestAjax.update();
            },            
            
            processData : function(rec) {
               
               uploader.location.href='/workspaces/csv-invitation-parser.html';
                ds3.removeAll();
                var tmp=[];
                for (var i=0; i<rec.length; i++) {
                  var fname=rec[i].firstName;
                  var lname=rec[i].lastName;    
                  var email=rec[i].email;
                  var idx = global_index++;
                  var addx='<center><input	type="checkbox"	class="formCheckbox	noBorder"	 id="addx'+idx+'"></center>';

                  var	p	=	new	Member({
                    						'firstName':	fname,
                    						'lastName': lname,
                    						'add':	addx,
                    						'email':	'<A	HREF="mailto:'+email+'">'+email+'</A>',
                    						'id':idx
                    					});
                  tmp.push(p);
                } 
                ds3.insert(0,tmp);
               
            },
            
			
			statusBox	:	function(){
											// everything	in this	space	is private and only	accessible in	the	HelloWorld block
											// define	some private variables
											var	dialog,	showBtn;
		
											// return	a	public interface
											return {
												 init	:	function(){
																	 showBtn = Ext.get('status-btn');
																	 //attach	to click event
																	 showBtn.on('click', this.showAlert, this);
																 },
			 
												 showAlert:	function(){
																	if(!dialog){ //	lazy initialize	the	dialog and only	create it	once
																		 dialog	=	new	Ext.BasicDialog("status-dlg",	{	
																								autoTabs:true,
                                                                                                draggable:false,
																								width:500,
																								height:300,
																								shadow:true,
																								modal: true,
																								minWidth:300,
																								minHeight:250,
																								proxyDrag: true
																			});
																			dialog.addKeyListener(27,	dialog.hide, dialog);
																			dialog.addButton(' CLOSE ',	dialog.hide, dialog);
																	}
																	
																	dialog.show(showBtn.dom);
															 }
											};
									}(), //	IMMEDIATE!
 
			mailBox	:	function(){
											// everything	in this	space	is private and only	accessible in	the	HelloWorld block
											// define	some private variables
											var	dialog,	showBtn;
		
											// return	a	public interface
											return {
												
												 init	:	function(){
																	 //showBtn = Ext.get('rejectApp');
																	 //attach	to click event
																	 //showBtn.on('click', this.showAlert, this);
																	 //mboxAjax=new ajaxObject('templates/rejection_letter.tpl',COL.mailBox.formLetter);
																	 //mboxAjax.update();
																 },
			                   formLetter : function(ajaxTxt, err, ajaxXML) {
                            document.getElementById('rejectLetter').value=ajaxTxt;			                   	   
			                   },
												 showAlert:	function(){
																	if(!dialog){ //	lazy initialize	the	dialog and only	create it	once
																		 dialog	=	new	Ext.BasicDialog("reject-dlg",	{	
																								autoTabs:true,
                                                                                                draggable:false,
																								width:500,
																								height:300,
																								shadow:true,
																								modal: true,
																								minWidth:500,
																								minHeight:300,
																								proxyDrag: true
																			});
																			dialog.addKeyListener(27,	dialog.hide, dialog);
																			dialog.addButton(' SEND ',	COL.mailBox.doUpdate, dialog);
																			dialog.addButton(' CLOSE ',	COL.mailBox.doUpdate, dialog);
																	}
																	
																	dialog.show(showBtn.dom);
															 }
											};
									}(), //	IMMEDIATE!
 
			searchBox	:	function(){ // Immediate.
											var	dialog,	showBtn;
		
											// return	a	public interface
											return {
												 init	:	function(){
																	 showBtn = Ext.get('doSearch');
																	 //attach	to click event
																	 showBtn.on('click', this.showAlert, this);
																	grid = new Ext.grid.EditorGrid('editor-grid',	{
																						ds:	ds,
																						cm:	cm,
																						enableColLock:false
																	});
																	layout = Ext.BorderLayout.create({
																		 center: {
																								margins:{left:3,top:3,right:3,bottom:3},
																								panels:	[new Ext.GridPanel(grid)]
																							}
																	}, 'grid-panel');
																 },
			 
												 submitData	:	function ()	{
														var	totalSubmit	=	0;
														
														var	checkSubmit	=	function(rec)	{
															 var id	=	rec.data.id;
															 try {
															    if	(document.getElementById('addx'+id).checked) {
																	   document.getElementById('emailList').value+=rec.data.email+'\n';
																	   totalSubmit++;
															    }
															 }
															 catch (err) {

															 }
														}
														ds.each(checkSubmit);
														if (totalSubmit>0) {
                                                           COL.inviteMember();
														   dialog.hide();
														   document.getElementById('emailList').value='';
														}
												 },
												 doSearch: function()	{
                                                      var searchOn = document.getElementById("searchFor").value;
                                                      if ((searchOn.length) > 1) {
														var	searchAjax = new ajaxObject(URLPolicy.wsmember_searchbox('workspace'),COL.populateSearch);
                                                        searchOn="form.name="+encodeURIComponent(searchOn);
                                                        searchOn+='&form.actions.search='+encodeURIComponent('Search For Members');
														searchAjax.update(searchOn,submitType);
                                                      } else {
                                                       Ext.MessageBox.alert('Error	Message',	'Your search must have more than one letter.');	                                                    
                                                         
                                                      }
												 },
												 showAlert:	function(){
																	if(!dialog){ //	lazy initialize	the	dialog and only	create it	once
																		 dialog	=	new	Ext.BasicDialog("search-dlg",	{	
																								autoTabs:true,
                                                                                                draggable:false,
																								width:650,
																								height:500,
																								shadow:true,
																								modal: true,
																								minWidth:650,
																								minHeight:500,
																								proxyDrag: true
																			});
																			dialog.addKeyListener(27,	dialog.hide, dialog);
																			dialog.addButton(' CANCEL ',	dialog.hide,	dialog);
																			dialog.addButton(' INVITE ',	COL.searchBox.submitData,	dialog);
																	}
																	ds.removeAll();
																	grid.render();
																	dialog.show(showBtn.dom);
															 }
											};
									}(), //	IMMEDIATE!
			uploadBox	:	function(){
											// define	some private variables
											var	dialog,	showBtn;
		
											// return	a	public interface
											return {
												 init	:	function(){
																	 showBtn = Ext.get('btnUpload');
																	 //attach	to click event
																	 showBtn.on('click', this.showAlert, this);
																	grid3	=	new	Ext.grid.EditorGrid('editor-grid3',	{
																						ds:	ds3,
																						cm:	cm3,
																						enableColLock:false
																	});
																	layout3	=	Ext.BorderLayout.create({
																		 center: {
																								margins:{left:3,top:3,right:3,bottom:3},
																								panels:	[new Ext.GridPanel(grid3)]
																							}
																	}, 'grid-panel3');
																 },
			 
                                                 selectAll : function() {
                                                    var chkBox = function(rec) {
                                                       document.getElementById('addx'+rec.data.id).checked=true;
                                                    }
                                                    ds3.each(chkBox);
                                                 },
												 submitData	:	function ()	{
														var	totalSubmit	=	0;
														
														var	checkSubmit	=	function(rec)	{
															 var id	=	rec.data.id;
															 if	(document.getElementById('addx'+id).checked) {
																	document.getElementById('emailList').value+=rec.data.email+'\n';
																	totalSubmit++;
															 }
														}
														ds3.each(checkSubmit);
														if (totalSubmit>0) {
														   COL.inviteMember();
														   dialog.hide();
														   document.getElementById('emailList').value='';
														}
												 },
												 showAlert:	function(){
																	if(!dialog){ //	lazy initialize	the	dialog and only	create it	once
																		 dialog	=	new	Ext.BasicDialog("upload-dlg",	{	
																								autoTabs:true,
                                                                                                draggable:false,
																								width:650,
																								height:500,
																								shadow:true,
																								modal: true,
																								minWidth:650,
																								minHeight:500,
																								proxyDrag: true
																			});
																			dialog.addKeyListener(27,	dialog.hide, dialog);
                                                                            dialog.addButton('SELECT ALL', COL.uploadBox.selectAll,dialog);
																			dialog.addButton(' CANCEL ',	dialog.hide,	dialog);
																			dialog.addButton(' ADD ',	COL.uploadBox.submitData,	dialog);
																	}
																	ds3.removeAll();
																	grid3.render();
																	dialog.show(showBtn.dom);
															 }
											};
									}(), //	IMMEDIATE!
 
			copyBox	:	function(){

											var	dialog,	showBtn;
		
											// return	a	public interface
											return {
												 init	:	function(){
																	 showBtn = Ext.get('btnCopy');
																	 //attach	to click event
																	 showBtn.on('click', this.showAlert, this);
																	grid2	=	new	Ext.grid.EditorGrid('editor-grid2',	{
																						ds:	ds2,
																						cm:	cm2,
																						enableColLock:false
																	});
																	layout2	=	Ext.BorderLayout.create({
																		 center: {
																								margins:{left:3,top:3,right:3,bottom:3},
																								panels:	[new Ext.GridPanel(grid2)]
																							}
																	}, 'grid-panel2');
//																	 mboxAjax=new ajaxObject(URLPolicy.wsmember_listing('workspace'),COL.copyBox.setMenu);
//																	 mboxAjax.update();


																 },
                                                 setMenu    :  function(responseTxt, err, responseXML) {
                                                    theMenu = document.getElementById('selWorkgroup');
                                                    theMenu.options[0] = new Option('Select Workgroup','xxx');
                                                    var menuIdx=1;
                                                    
                                                    var insertFields = function(result,str) {
                                                       for(var i=0; i<result.length; i++) {
                                                          el=result[i];
                                                          if (el) {
                                                             theMenu.options[menuIdx++] = new Option(el.firstChild.nodeValue+' ('+str+')',
                                                                                                       el.attributes[0].value);
                                                          thedebug=el;
                                                          }
                                                       }
                                                    }
                                                    
						                                     if (err==200||err==0)	{
                                                             debugr = responseXML;
                                                         var	result = responseXML.getElementsByTagName('managerlist');
                                                         insertFields(result,'Manager');
                                                         var   result = responseXML.getElementsByTagName('memberlist');
                                                         insertFields(result,'Member');
                                                    }
                                                 },
                                                 
                                                 grabWorkgroup : function() {
                                                    theMenu = document.getElementById('selWorkgroup');
                                                    href=theMenu.options[theMenu.selectedIndex].value;
                                                    if (!/xxx/i.test(href)) {
													                             var cboxAjax=new ajaxObject(href,COL.populateCopy);
                                                       cboxAjax.update();
                                                    } else {
                                                       Ext.MessageBox.alert('Error	Message',	'You must select a workgroup from the drop down list!');	                                                    
                                                    }
                                                 },
			 
												 submitData	:	function ()	{
                                                 
														var	totalSubmit	=	0;
														
														var	checkSubmit	=	function(rec)	{
															 var id	=	rec.data.id;
															 if	(document.getElementById('addx'+id).checked) {
																	document.getElementById('emailList').value+=rec.data.email+'\n';
																	totalSubmit++;
															 }
														}
														ds2.each(checkSubmit);
														if (totalSubmit>0) {
														   dialog.hide();
															 COL.inviteMember();
														   document.getElementById('emailList').value='';
														}
												 },
                                                 selectAll : function() {
                                                    var chkBox = function(rec) {
                                                       document.getElementById('addx'+rec.data.id).checked=true;
                                                    }
                                                    ds2.each(chkBox);
                                                 },
												 showAlert:	function(){
																	if(!dialog){ //	lazy initialize	the	dialog and only	create it	once
																		 dialog	=	new	Ext.BasicDialog("copy-dlg",	{	
																								autoTabs:true,
																								width:650,
																								height:500,
																								shadow:true,
                                                                                                draggable:false,
																								modal: true,
																								minWidth:650,
																								minHeight:500,
																								proxyDrag: true
																			});
																			dialog.addKeyListener(27,	dialog.hide, dialog);
                                                                            dialog.addButton('SELECT ALL', COL.copyBox.selectAll,dialog);
																			dialog.addButton(' CANCEL ',	dialog.hide,	dialog);
																			dialog.addButton(' INVITE ',	COL.copyBox.submitData,	dialog);
																	}
																	ds2.removeAll();
																	grid2.render();
																	dialog.show(showBtn.dom);
															 }
											};
									}(), //	IMMEDIATE!
 
	 
				 Init	:	function() {
																	
										 getMembersAjax	=	new	ajaxObject(URLPolicy.wsmember_managebox('workspace'),	COL.populateMembers);										 
										 getMembersAjax.update();
																	
								     getInvitesAjax	=	new	ajaxObject(URLPolicy.wsinvitations_manage('workspace'),	COL.populateInvites);										 
										 getInvitesAjax.update();

				    	                document.getElementById('requestCount').innerHTML='<img src="/static/images/progress.gif" width="10" height="10" alt="ajax activity">';
                                        document.getElementById('memberCount').innerHTML='<img src="/static/images/progress.gif" width="10" height="10" alt="ajax activity">';
                    		            document.getElementById('outstandingInvites').innerHTML='<img src="/static/images/progress.gif" width="10" height="10" alt="ajax activity">';

                                         getRequestAjax	=	new	ajaxObject(URLPolicy.join_requests('workspace'),	COL.populateRequest);										 
										 getRequestAjax.update();

                     COL.resizeGrid(4);										 
								},	 


				 populateMembers : function(txtDat,	err, xmlDat) {
						var	tmp	=	[];
						if ((err==200)||(err==0))	{
							var	result = xmlDat.getElementsByTagName('member');
                            dbr=result;
							for(var	i=0; i<result.length;	i++) {
								 var idx = global_index++;
                                 try {
								 var fname = result[i].getElementsByTagName('firstname')[0].firstChild.nodeValue;
                                 } catch (ex) {
                                    var fname = '';
                                 }
                                 try {
                                    var lname = result[i].getElementsByTagName('lastname')[0].firstChild.nodeValue;
                                } catch (ex) {
                                   var lname='';
                                }
                                try {
								    var email = result[i].getElementsByTagName('email')[0].firstChild.nodeValue;
                                } catch(ex) {
                                   var email = '';
                                }
                                try {
                                 var uid = result[i].attributes.getNamedItem("id").value;
                                 } catch(ex) {
                                    var uid='';
                                 }
								 try {
										var	manager	=	result[i].attributes.getNamedItem('manager').value;
                                        var omgr=true;
								 }
								 catch (err) {
										var	manager=false;
                                        omgr=false;
								 }
								 if	(manager)	{
										var	isChecked	=	'	checked	';
								 }	else {
										var	isChecked	=	'	';
								 }
                 var	profile	=	'/workspaces/'+workgroup+'/profile_by_id.xml?id='+uid;

								 var manager='<center><input type="checkbox"'+isChecked+' class="formCheckbox noBorder" onClick="COL.flagManagerChange(); COL.verifyCheckBox('+idx+')"	id="manager'+idx+'"></center>';
								 var removex='<center><input type="checkbox" class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')" id="removex'+idx+'"></center>';
                  var cmd = 'tooltipPop({firstName: "'+fname+'", lastName:"'+lname+'", email:"'+email+'"},'+idx+',this)';
                  fnameOrg = fname;
								  fname = '<div id="fname'+idx+'" onClick="tooltipPop(\''+profile+'\',this)">'+fname+'</div>';
								  lname = '<div id="lname'+idx+'" onClick="tooltipPop(\''+profile+'\',this)">'+lname+'</div>';
									p	=	new	Member({
										 'firstName':	fname,
										 'lastName': lname,
										 'manager':	manager,
										 'remove': removex,
                                         'uid':uid,
                                         'omgr':omgr,
										 'email':	'<A	HREF="mailto:'+email+'">'+email+'</A>',
										 'id':idx
									});	

								 tmp.push(p);
							}
						}
						
						var recs = 0;

						var doCount = function(rec) {
							   recs++;
						}
						
						if (tmp.length>0)	{
                             ds4.removeAll();
							 ds4.insert(0,tmp);
							 ds4.each(doCount);
						}
                        document.getElementById('memberCount').innerHTML=recs;
				 },				
				 
				 populateRequest : function(txtDat,	err, xmlDat) {
						var	tmp	=	[];
                        ds6.removeAll();
						if ((err==200)||(err==0))	{
							var	result = xmlDat.getElementsByTagName('entry');
							for(var	i=0; i<result.length;	i++) {
								 var idx = global_index++;
                                 try {
								    var fname = result[i].getElementsByTagName('firstname')[0].firstChild.nodeValue;
                                 } catch(ex) {
                                    var fname = '';
                                 }
                                 try {
								    var lname = result[i].getElementsByTagName('lastname')[0].firstChild.nodeValue;
                                 } catch(ex) {
                                    var lname = '';
                                 }
                                 try {
								    var email = result[i].getElementsByTagName('email')[0].firstChild.nodeValue;
                                 } catch(ex) {
                                    var email='';
                                 }
                                 try {
                                    var message = result[i].getElementsByTagName('message')[0].firstChild.nodeValue;
                                 } catch(ex) {
                                    var message = '';
                                 }
                                 var uid = result[i].getElementsByTagName('id')[0].firstChild.nodeValue;
								 message=message.replace(/'/g,'\\');
                                 message=message.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                                 var addx='<center><span onMouseover="COL.appFlyover(event,\'';
                                     addx+=fname+'\',\'';
                                     addx+=lname+'\',\'';
                                     addx+=email  +'\',\'';
                                     addx+=message+'\')"';
                                     addx+='onMouseOut="COL.appFlyout(event)" class="cursorHelp">';
                                     addx+='<img src="/static/images/btn_letter.gif" width="20" height="20"></span></center>';
								  
								 try {
										var	manager	=	result[i].getElementsByTagName('manager')[0].firstChild.nodeValue;
								 }
								 catch (err) {
										var	manager=false;
								 }
								 if	(manager)	{
										var	isChecked	=	'	checked	';
								 }	else {
										var	isChecked	=	'	';
								 }
								 var manager='<center><input type="checkbox"'+isChecked+' class="formCheckbox noBorder" id="manager'+idx+'"></center>';
								 var removex='<center><input type="checkbox" class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')" id="removex'+idx+'"></center>';
//								 var removex='<center><input type="checkbox" class="formCheckbox noBorder" id="removex'+idx+'"></center>';

                                 var cmd = 'tooltipPop({firstName: "'+fname+'", lastName:"'+lname+'", email:"'+email+'"},'+idx+',this)';
                                 fnameOrg = fname;
								  fname = '<div id="fname'+idx+'">'+fname+'</div>';
								  lname = '<div id="lname'+idx+'">'+lname+'</div>';
									p	=	new	Member({
										 'firstName':	fname,
										 'lastName': lname,
										 'manager':	manager,
										 'remove': removex,
										 'add':addx,
                                         'uid':uid,
										 'email':	'<A	HREF="mailto:'+email+'">'+email+'</A>',
										 'id':idx
									});	

								 tmp.push(p);
							}
						}
						var recs = 0;

						var doCount = function(rec) {
							   recs++;
						}
						
						if (tmp.length>0)	{
							 ds6.insert(0,tmp);
							 ds6.each(doCount);
						}
				    	document.getElementById('requestCount').innerHTML=recs;
   			    },				
				 
                    populateInvites : function(txtDat,	err, xmlDat) {
                        ds5.removeAll();
                    	var	tmp	=	[];
                          if ((err==200)||(err==0))	{
                    		var	result = xmlDat.getElementsByTagName('invitation');
                            
                    		for(var	i=0; i<result.length;	i++) {
                    			var idx = global_index++;
                                var iid = result[i].attributes[0].value;
                                try {
                    			   var fname = result[i].getElementsByTagName('firstname')[0].firstChild.nodeValue;
                                } catch (e) {
                                   var fname = '';
                                }
                                try {
                    			   var lname = result[i].getElementsByTagName('lastname')[0].firstChild.nodeValue;
                                } catch (e) {
                                   lname = '';
                                }
                    			try {
                    				var cdate = result[i].getElementsByTagName('lastcontact')[0].firstChild.nodeValue;
                            //cdate=/([^T]+)/.exec(cdate)[0].split('-');
                            //cdate = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][parseInt(cdate[1])-1]+ ' ' + cdate[2] + ', '+cdate[0];
                    			} catch (err) {
                    				var cdate = 'Invalid XML';
                    			}
                    			var email = result[i].getElementsByTagName('email')[0].firstChild.nodeValue;
                    			try {
                    				var	manager	=	result[i].getElementsByTagName('manager')[0].firstChild.nodeValue;
                    			}
                    			catch (err) {
                    				var	manager=false;
                    			}
                    			if	(manager)	{
                    				var	isChecked	=	'	checked	';
                    				}	else {
                    					var	isChecked	=	'	';
                    				}
                    				var manager='<center><input type="checkbox"'+isChecked+' class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')"	id="manager'+idx+'"></center>';
                    				var removex='<center><input type="checkbox" class="formCheckbox noBorder" onClick="COL.verifyCheckBox('+idx+')" id="removex'+idx+'"></center>';
                    				var cmd = 'tooltipPop({firstName: "'+fname+'", lastName:"'+lname+'", email:"'+email+'"},'+idx+',this)';
                    				fnameOrg = fname;
                    				fname = '<div id="fname'+idx+'">'+fname+'</div>';
                    				lname = '<div id="lname'+idx+'">'+lname+'</div>';
                    				p	=	new	Member({
                    					'firstName':	fname,
                    					'lastName': lname,
                    					'manager':	manager,
                    					'remove': removex,
                                        'iid':iid,
                    					'date': cdate,
                    					'email':	'<A	HREF="mailto:'+email+'">'+email+'</A>',
                    					'id':idx
                    				});
                    
                    				tmp.push(p);
                    			}
                    		}
                    
                    		var recs = 0;
                    
                    		var doCount = function(rec) {
                    			recs++;
                    		}
                    
                    		if (tmp.length>0)	{
                    			ds5.insert(0,tmp);
                    			ds5.each(doCount);
                    		}
                    		document.getElementById('outstandingInvites').innerHTML=recs;
                    
                    
                    
                    	},

                    acceptRequests : function() {
                    
                       var checkGrid = function (rec) {
							id = rec.data.id;
							if (document.getElementById('removex'+id).checked) {
                               buildStr+=rec.data.uid+',';
                            }
                       }
                    
                       var buildStr='';
                       ds6.each(checkGrid);
                       buildStr='request_ids='+encodeURIComponent(buildStr.replace(/\,$/,''));
                       var tajax = new ajaxObject(URLPolicy.acceptRequests(), function() {COL.reloadMembers(); COL.reloadRequests();});
                       tajax.update(buildStr,'POST');
                    },


                    rejectRequests : function() {
                    
                       var checkGrid = function (rec) {
							id = rec.data.id;
							if (document.getElementById('removex'+id).checked) {
                               buildStr+=rec.data.uid+',';
                            }
                       }
                    
                       var buildStr='';
                       ds6.each(checkGrid);
                       buildStr='request_ids='+encodeURIComponent(buildStr.replace(/\,$/,''));
                       var tajax = new ajaxObject(URLPolicy.rejectRequests(), function() {COL.reloadRequests();});
                       tajax.update(buildStr,'POST');
                    },

                    resendInvites : function() {
                    
                       var checkGrid = function (rec) {
							id = rec.data.id;
							if (document.getElementById('removex'+id).checked) {
                               buildStr+=rec.data.iid+',';
                            }
                       }
                    
                       var buildStr='';
                       ds5.each(checkGrid);
                       buildStr='form.invitationIds='+encodeURIComponent(buildStr.replace(/\,$/,''));
                       buildStr+='&form.actions.reSendInvitations='+encodeURIComponent('Re-send Invitations');
                       var tajax = new ajaxObject(URLPolicy.resend_invitations(), COL.resendResponse);
                       tajax.update(buildStr,'POST');
                    },

                    removeInvites : function() {
                    
                       var checkGrid = function (rec) {
							id = rec.data.id;
							if (document.getElementById('removex'+id).checked) {
                               buildStr+=rec.data.iid+',';
                            }
                       }
                    
                       var buildStr='';
                       ds5.each(checkGrid);
                       buildStr='form.invitationIds='+encodeURIComponent(buildStr.replace(/\,$/,''));
                       buildStr+='&form.actions.cancelInvitations='+encodeURIComponent('Cancel Invitations');
                       var tajax = new ajaxObject(URLPolicy.cancel_invitations(), COL.resendResponse);
                       tajax.update(buildStr,'POST');
                    },

                    resendResponse : function() {
                       var getInvitesAjax	=	new	ajaxObject(URLPolicy.wsinvitations_manage('workspace'),	COL.populateInvites);										 
							getInvitesAjax.update();
                    },

                    populateSearch	:	function(txtDat, err,	xmlDat)	{
                    	var	tmp	=	[];
                    	ds.removeAll();
                    	if ((err==200)||(err==0))	{
                    		if (xmlDat) {
                    			var	result = xmlDat.getElementsByTagName('member');
                    			if (result.length==0) {
                    				Ext.MessageBox.alert('Error', 'No results found for this search.\nPlease refine your search and try again.',	function() {return});
                    			}
                    			for(var	i=0; i<result.length;	i++) {
                    				var idx = global_index++;
                                    try {
                    				   var fname = result[i].getElementsByTagName('firstname')[0].firstChild.nodeValue;
                                    } catch (exp) {
                                       var fname = '';
                                    } 
                                    try {
                    				   var lname = result[i].getElementsByTagName('lastname')[0].firstChild.nodeValue;
                                    } catch (exp) {
                                       var lname = '';
                                    }
                    				var email = result[i].getElementsByTagName('email')[0].firstChild.nodeValue;
                    				try {
                    					var	manager	=	result[i].getElementsByTagName('manager')[0].firstChild.nodeValue;
                    				}
                    				catch (err) {
                    					var	manager=false;
                    				}
                    				if	(manager)	{
                    					var	isChecked	=	'	checked	';
                    					}	else {
                    						var	isChecked	=	'	';
                    					}
                    					manager='<center><input type="checkbox"'+isChecked+'class="formCheckbox noBorder"	id="manager'+idx+'"></center>';
                    					var addx='<center><input	type="checkbox"	class="formCheckbox	noBorder"	 id="addx'+idx+'"></center>';
                    					var	p	=	new	Member({
                    						'firstName':	fname,
                    						'lastName': lname,
                    						'manager':	manager,
                    						'add':	addx,
                    						'email':	'<A	HREF="mailto:'+email+'">'+email+'</A>',
                    						'id':idx
                    					});
                    
                    					tmp.push(p);
                    				}
                   				} else {
                    					Ext.MessageBox.alert('Error', 'No results found for this search.',	function() {return});
                   				}
                 				} else {
                    					Ext.MessageBox.alert('Error', 'Server returned error '+err+'. Please make sure you are still logged in.'+xmlDat,	function() {return});
                    		}
                    		if (tmp.length>0)	{
                    			ds.insert(0,tmp);
                    		}
				 },				

				 populateCopy	:	function(txtDat, err,	xmlDat)	{
						var	tmp	=	[];
						if (err==200||err==0)	{
							var	result = xmlDat.getElementsByTagName('member');
							for(var	i=0; i<result.length;	i++) {
								 var idx = global_index++;
                                 try {
								    var fname = result[i].getElementsByTagName('firstname')[0].firstChild.nodeValue;
                                 } catch (exp) {
                                    var fname = '';
                                 }
                                 try {
								    var lname = result[i].getElementsByTagName('lastname')[0].firstChild.nodeValue;
                                 } catch (exp) {
                                    var lname = '';
                                 }
								 var email = result[i].getElementsByTagName('email')[0].firstChild.nodeValue;
								 try {
										var	manager	=	result[i].getElementsByTagName('manager')[0].firstChild.nodeValue;
								 }
								 catch (err) {
										var	manager=false;
								 }
								 if	(manager)	{
										var	isChecked	=	'	checked	';
								 }	else {
										var	isChecked	=	'	';
								 }
								 manager='<center><input type="checkbox"'+isChecked+'class="formCheckbox noBorder"	id="manager'+idx+'"></center>';
								 var addx='<center><input	type="checkbox"	class="formCheckbox	noBorder"	 id="addx'+idx+'"></center>';
									var	p	=	new	Member({
										 'firstName':	fname,
										 'lastName': lname,
										 'manager':	manager,
										 'add':	addx,
										 'email':	'<A	HREF="mailto:'+email+'">'+email+'</A>',
										 'id':idx
									});	

								 tmp.push(p);
							}
						}
						if ((DEBUG)&&(tmp.length==0))	{
							 for (var	i=0; i<25; i++)	{
									var	dat	=	COL.fakeData();
									var	idx	=	global_index++;
									var	manager='<center><input	type="checkbox" onClick="COL.verifyCheckBox('+idx+')"	class="formCheckbox noBorder"	id="manager'+idx+'"></center>';
									var	removex='<center><input	type="checkbox" onClick="COL.verifyCheckBox('+idx+')"	class="formCheckbox noBorder"	id="removex'+idx+'"></center>';
									var	p	=	new	Member({
												'firstName': dat.firstName,
												'lastName':	dat.lastName,
												'manager': manager,
												'remove':	removex,
												'email': '<a href="mailto:'+dat.email+'">'+dat.email+'</a>',
												'id':idx
									});	
									tmp.push(p);
							}							
						}
						if (tmp.length>0)	{
							 ds2.removeAll();
							 ds2.insert(0,tmp);
						}
				 },				
								
								
				 resizeGrid	:	function (gridNo)	{
				 	  if (!gridNo) {gridNo=0;}
						var	gridWidth	=	document.getElementById('grid-member').offsetWidth;

						// the column	model	has	information	about	grid columns
						// dataIndex maps	the	column to	the	specific data	field	in
						// the data	store	(created below)
						if ((gridNo==999)||(gridNo==4)) {
							if (!grid4) {
      		        var cm4 = new Ext.grid.ColumnModel([{
      							 header: "<center>Remove</center>",
      							 dataIndex:	'remove',
      							 sortable: false,
      							 width:	Math.floor(gridWidth*.10)
      						},{
      							 header: "First	Name",
      							 dataIndex:	'firstName',
      							 width:	Math.floor(gridWidth*.25)
      							 //editor: new Ed(new	fm.TextField({ allowBlank: false }))
      						},{
      							 header: "Last Name",
      							 dataIndex:	'lastName',
      							 width:	Math.floor(gridWidth*.25)
      							 //editor: new Ed(new	fm.TextField({ allowBlank: false }))
      						},{
      							 header: "E-Mail Address",
      							 dataIndex:	'email',
      							 width:	Math.floor(gridWidth*.25)
      							 //editor: new Ed(new	fm.TextField({ allowBlank: false }))
      						},{
   								 header: '<center>Manager	<span	onMouseOver="COL.flyover(event)" onMouseOut="COL.flyout()"><img	src="/static/images/bulletInfo.gif"	alt="" border="0"/></span></center>',
      							 dataIndex:	'manager',
      							 sortable: false,
      							 width:	Math.floor(gridWidth*.10)
      						}]);
      						grid4	=	new	Ext.grid.EditorGrid('member-grid', {
      							 ds: ds4,
      							 cm: cm4,
      							 enableColLock:false});
      						cm4.defaultSortable	=	true;
   							layout4 = Ext.BorderLayout.create({
   											     center: {
   														  	   		margins:{left:3,top:3,right:3,bottom:3},
   																			panels:	[new Ext.GridPanel(grid4)]
   																	 }
   											  }, 'grid-member');
      						grid4.render();
      						grid4.stopEditing();
      				 }
					  }
					  if ((gridNo==999)||(gridNo==5)) {
					  	 if (!grid5) {
					        if (document.getElementById('tab2').style.display=='block') {
           			   	var	cm5	=	new	Ext.grid.ColumnModel([{
      						   			header:	"<center>Select</center>",
         									dataIndex: 'remove',
         								 sortable: false,
         									width: Math.floor(gridWidth*.10)
         							},{
         									header:	"First Name",
         									dataIndex: 'firstName',
         									width: Math.floor(gridWidth*.15)
         							 },{
         									header:	"Last	Name",
         									dataIndex: 'lastName',
         									width: Math.floor(gridWidth*.15)
         							 },{
         									header:	"E-Mail	Address",
         									dataIndex: 'email',
         									width: Math.floor(gridWidth*.35)
         							},{
         								 header: 'Last Contact',
         									dataIndex: 'date',
         								  sortable: true,
         									width: Math.floor(gridWidth*.20)
         							 }]);
         						
         	   					cm5.defaultSortable	=	true;
           	 					grid5	=	new	Ext.grid.EditorGrid('outstanding-grid', {
         				   			 ds: ds5,
         						   	 cm: cm5,
         							   enableColLock:false});
             						grid5.stopEditing();
   										 layout5 = Ext.BorderLayout.create({
   																		 center: {
   																								margins:{left:3,top:3,right:3,bottom:3},
   																								panels:	[new Ext.GridPanel(grid5)]
   																							}
   																	}, 'grid-outstanding');
             						
         						   grid5.render();
         						}
   						 }
   					}
					  if ((gridNo==999)||(gridNo==6)) {
					  	 if (!grid6) {
   					     if (document.getElementById('tab1').style.display=='block') {
              				var	cm6	=	new	Ext.grid.ColumnModel([{
         									header:	"<center>Select</center>",
         									dataIndex: 'remove',
         								 sortable: false,
         									width: Math.floor(gridWidth*.10)
         							},{
         									header:	"First Name",
         									dataIndex: 'firstName',
         									width: Math.floor(gridWidth*.15)
         							 },{
         									header:	"Last	Name",
         									dataIndex: 'lastName',
         									width: Math.floor(gridWidth*.15)
         							 },{
         									header:	"E-Mail	Address",
         									dataIndex: 'email',
         									width: Math.floor(gridWidth*.40)
         							},{
         								 header: '<center>Message</center>',
         									dataIndex: 'add',
         								  sortable: false,
         									width: Math.floor(gridWidth*.15)
         							 }]);
         						
         	   					cm6.defaultSortable	=	true;
           	 					grid6	=	new	Ext.grid.EditorGrid('request-grid', {
         				   			 ds: ds6,
         						   	 cm: cm6,
         							   enableColLock:false});
             						grid6.stopEditing();
   										 layout6 = Ext.BorderLayout.create({
   																		 center: {
   																								margins:{left:3,top:3,right:3,bottom:3},
   																								panels:	[new Ext.GridPanel(grid6)]
   																							}
   																	}, 'grid-request');
             						
         						   grid6.render();
         						}
   						 }
   					}
				 },

								

				 //	Temporary	function --	replace	with true	ajax calls.								
				 fakeData	:	function() {
						var	firstNamesArray	=	["Hannah","Monique","Tristan","David","Kyle","Jenna","Madison","Noah","Alyssa","Alex","Jacob","Ethan","Ryan","Matthew","Jack","Noah","Nicholas","Joshua","Logan","Andrew","Michael","Caden","Dylan","Tyler","Connor","Jackson"];
						var	lastNamesArray = ["Caleb","Jayden","Alexander","Nathan","Brayden","Zachary","Benjamin","William","James","Daniel","Gavin","Evan","Luke","Joseph","Landon","Christopher","Mason","Cameron","Anthony","Owen","Gabriel","Austin","Lucas","Christian","John","Sean"];
						var	first	=	firstNamesArray[Math.floor(Math.random()*26)];
						var	last = lastNamesArray[Math.floor(Math.random()*26)];
						var	email	=	first+'.'+last+'@somedomain.org';
						var	bld	=	{
										 'firstName':	first, 
										 'lastName'	:	last,
										 'email'		:	email
									}
						return(bld);
				 },
				 
				 toggle	:	function(divId)	{
						var	div	=	document.getElementById(divId);
						if (div) {
							 if	(div.style.display=='none')	{
									div.style.display='block';
							 } else	{
									div.style.display='none';
							 }
						}
				 },				

				 //	Populates	the	search-box grid	with data	returned from	ajax call							
				 populateGrid2: function() {
				 	   COL.populateGrid(2);
				 	   return false;
				 },
				 populateGrid3: function() {
             COL.populateGrid(3);
             return false;
				 },
				 populateGrid	:	function(dsIdx)	{
						switch(dsIdx)	{
							 case	1: tmpDS=ds;
									break;
							 case	2: tmpDS=ds2;
									break;
							 case	3: tmpDS=ds3;
									break;
						}
						tmpDS.removeAll();
						return false;
				 },

// This	is the "workspace	dialog"				 
				 
				 addAlert : function(ajaxTxt, ajaxErr, ajaxXML) {
                       document.getElementById("errorList").innerHTML='';
                       var getInvitesAjax	=	new	ajaxObject(URLPolicy.wsinvitations_manage('workspace'),	COL.populateInvites);										 
							getInvitesAjax.update();
                 
				 	  if ((DEBUG==true)&&(ajaxErr==606)) {
						  document.getElementById("namesAdded").innerHTML=5;
                 var str='The following	people are already members of the	workspace or have pending invitations, so	they will not be added.<ol>'							
                 str+='<li>name@domain.com</li>';
                 str+='<HR>This alert is using sample data<HR>';
                 str+='</OL>';
						     document.getElementById("errorList").innerHTML=str;
   						   COL.statusBox.showAlert();
   						   return;
				 	  }
				    if ((!ajaxXML)||(ajaxErr!=200)) {
 						   document.getElementById("namesAdded").innerHTML='0 ';
                           errMsg='Error Communicating With The Server. '+ajaxErr;
                           if (ajaxErr==200) { 
                              errMsg+=' Because of the error message (200) it is likely that you are not logged into the website.  Please ensure you are logged in when using these features.';
                           }
				       document.getElementById("errorList").innerHTML=errMsg;
				    } else {
              var	result = ajaxXML.getElementsByTagName('accepted');
              if (result[0]) {
                 result = result[0].firstChild.nodeValue;
              } else {
              	 result = 0;
              } 
						  document.getElementById("namesAdded").innerHTML=result;
              var str = '';
              try {
                 errors = ajaxXML.getElementsByTagName('member');
              } catch (exp) {
              	 errors=[];
              }
              if (errors.length>0) {
                 str+='The following	people are already members of	the	workspace, so	they will	not	receive	an invitation.<ol>'							
                 for(var	i=0; i<errors.length;	i++) {
                 	 str+='<li>'+errors[i].firstChild.nodeValue+'</li>';
                 }
                 str+='</OL><br/>';
						     document.getElementById("errorList").innerHTML=str;
              }	
              try {			    	
                 errors = ajaxXML.getElementsByTagName('invite');
              } catch (exp) {
              	 errors = [];
              }
              if (errors.length>0) {
                 str+='The following	people already have outstanding invitations, so	they will	not	receive	an invitation.<ol>'							
                 for(var	i=0; i<errors.length;	i++) {
                 	 str+='<li>'+errors[i].firstChild.nodeValue+'</li>';
                 }
                 str+='</OL>';
						     document.getElementById("errorList").innerHTML=str;
              }				    	
				    }
						COL.statusBox.showAlert();
				 },
				 
				 //Add member	by email (reads	the	email	box	and	talks	to server).					
				 inviteMember	:	function() {
		
     						var	checkMail	=	'';
     						var	firstNamesArray	=	["Hannah","Monique","Tristan","David","Kyle","Jenna","Madison","Noah","Alyssa","Alex","Jacob","Ethan","Ryan","Matthew","Jack","Noah","Nicholas","Joshua","Logan","Andrew","Michael","Caden","Dylan","Tyler","Connor","Jackson"];
     						var	lastNamesArray = ["Caleb","Jayden","Alexander","Nathan","Brayden","Zachary","Benjamin","William","James","Daniel","Gavin","Evan","Luke","Joseph","Landon","Christopher","Mason","Cameron","Anthony","Owen","Gabriel","Austin","Lucas","Christian","John","Sean"];
     		
     						var	checkDup = function(rec) {
     							 if	(rec.data.email==checkMail)	{
     									isDup=true;
     							 }
     						}		 
     		
     	
     						var	email	=	Ext.get('emailList').dom.value;
     						if (email.replace(/^\s+|\s+$/g,"") ==	'')	{
     							 Ext.MessageBox.alert('Error', 'Please enter at	least	one	email	address	in the textbox.',	function() {return});
     							 return;
     						}
     						Ext.get('emailList').dom.value='';
     						email	=	email.replace(/\n/g,',');
     						email	=	email.replace(/&lt;/g,'&lt;').replace(/&gt;/g,'&gt;');
     						email	=	email.replace(/<([^>]+)>/g,'');
     						email	=	email.replace(/\s/g,',');
     						email	=	email.split(',');
     						var	isDup	=	false;
     						global_index++;
     						var	tempBuild	=	[];
     						var	error2Build	=	'The following email addresses were	not	formatted	properly and have	not	been submitted to	the	workspace.<OL>';
     						var	err2=0;
     						var	errorBuild = 'The	following	people are already members of	the	workspace, so	they will	not	receive	an invitation.<OL>';
     						var	err1 = 0;
     						for	(var i=0;	i<email.length;	i++) {
     						 if	(!/^[\w-]+(?:\.[\w-]+)*(@|#)(?:[\w-]+\.)+[a-zA-Z]{2,7}$/i.test(email[i]))	{
     								if (email[i].length>1) {
     									 Ext.get('emailList').dom.value+=email[i]+'	<Improper	Format>\n';
     									 error2Build+="<LI>	"+email[i]+"</LI>";
     									 err2++;
     								}
     								email[i]='';
     						 }						
     						 if	(email[i].length>3)	{
     								tempBuild.push(email[i]);
     						 }
     					}
     					if (tempBuild.length>0) {
     						 var memberList=[];
     						 var managerList=[];
     						 for (i=0; i<tempBuild.length; i++) {
     						 	  if (/#/i.test(tempBuild[i])) {
     						 	  	 managerList.push(tempBuild[i].replace(/#/,'@'));
     						 	  } else {
     						 	  	 memberList.push(tempBuild[i]);
     						 	  }
     						 }
     					   var emailList='form.memberEmails='+encodeURIComponent(memberList.join(','));
     					   emailList+='&form.managerEmails='+encodeURIComponent(managerList.join(','));
     					   emailList+='&form.actions.invite='+encodeURIComponent('Add Invitations');
     						 var	addAjax = new ajaxObject(URLPolicy.add_invitation('workspace'),COL.addAlert);
     						 addAjax.update(emailList,submitType);
     					}

				 }, //	Invite Member.
				 
				 toggles : {
				 	
				 	   toggle1 : function () {
				 	   	            // Toggle visibility of the request to join grid
	                        showHide('tabs1', 'tab1');
	                        COL.resizeGrid(6);
				 	   },
				 	   
				 	   toggle2 : function() {
				 	   	            // Toggle visibility of the manage invites grid
				 	   	            showHide('tabs1', 'tab2');
				 	   	            COL.resizeGrid(5);
				 	   	            
				 	   },
				 	   toggle3 : function() {
				 	   	            // Toggle visibility of the manage members grid
				 	   	            showHide('tabs1', 'tab3')
				 	   	            
				 	   }
				 	
				 }
				 
			}	 //	End	return
}(); //	Immediate	function!


function resize999() {
	COL.resizeGrid(999);
}

function testkey(e) {
   if (!e) { e = window.event } 
   if(e.keyCode == 13) {
      COL.searchBox.doSearch();
      return false;
   }   ;
}

Ext.onReady(function(){

   //var closeTooltip = Ext.get('closeImg');
   //closeTooltip.on('click',  function(){alert('ding');});
   
   
	 var btn = Ext.get('addBtn');
	 if (btn) {
	    btn.on('click', COL.inviteMember);
	 }
	     
     var btn1 = Ext.get('rejectApp');
     if (btn1) {
        btn1.on('click', COL.rejectRequests);
     }
     
	 var btn2	=	Ext.get('doUpdate');
	 if (btn2) {
	    btn2.on('click',COL.updateMembers);
	 }

   var btn3 = Ext.get('toggle1');
   if (btn3) {
      btn3.on('click',COL.toggles.toggle1);
   }

   var btn4 = Ext.get('toggle2');
   if (btn4) {
      btn4.on('click',COL.toggles.toggle2);
   }
   
   var btn5 = Ext.get('toggle3');
   if (btn5) {
      btn5.on('click',COL.toggles.toggle3);
   }

   var btn6 = Ext.get('search-btn');
   if (btn6) {
      btn6.on('click',COL.searchBox.doSearch);
   }
   
   var btn7 = Ext.get('grabWorkgroup');
   if (btn7) {
      btn7.on('click', COL.copyBox.grabWorkgroup);
   }
   
   var btn9 = Ext.get('btnUpload');
   if (btn9) {
      btn9.on('click',COL.populateGrid3);
   }
   
/*   var btn10 = Ext.get('inviteResend');
   if (btn10) {
      btn10.on('click',COL.resendInvites);
   } 
*/
    document.getElementById('inviteResend').onclick=COL.resendInvites;
    document.getElementById('inviteRemove').onclick=COL.removeInvites;
    document.getElementById('requestUpdate').onclick=COL.acceptRequests;


   if (document.getElementById('searchFor')) {
      document.getElementById('searchFor').onkeypress=testkey;
   }

	 //	using	onDocumentReady	instead	of window.onload initializes the application
	 //	when the DOM is	ready, without waiting for images	and	other	resources	to load
	 Ext.onReady(COL.statusBox.init, COL.statusBox,	true);
	 Ext.onReady(COL.searchBox.init, COL.searchBox,	true);
	 Ext.onReady(COL.copyBox.init, COL.copyBox,	true);
	 Ext.onReady(COL.uploadBox.init, COL.uploadBox,	true);
   
	 //	Initialize the items in	the	COL	namespace.					 
	 COL.Init();
     
     
     
//     COL.mailBox.init();
	 document.onmousemove=globalMouse;
   _tooltipId=document.getElementById('toolTip1');
	 _template=_tooltipId.innerHTML;
	 document.getElementById('reject-dlg').style.display='none';
	 document.getElementById('status-dlg').style.display='none';

    document.getElementById('search-dlg').style.display='block';
    document.getElementById('search-dlg').style.visibility='hidden';
    document.getElementById('copy-dlg').style.display='block';
    document.getElementById('copy-dlg').style.visibility='hidden';
    document.getElementById('upload-dlg').style.display='block';
    document.getElementById('upload-dlg').style.visibility='hidden';

//    var loader=setInterval(COL.checkUpload,500);

    var el = Ext.select('[class=searchLine]')[0];
    if (el) {
       el.innerHTML='Spreadsheet Format: First Name, Last Name, Email Address<BR>'+el.innerHTML;
    }
//    document.getElementById('grid-panel').style.display='
	 
	 window.onresize=resize999;
});	 //	ext.onReady





/* Tooltip Manager */


/* Global -- For the time being. */

var _tooltipId = false;
var _mouseX = 0;
var _mouseY = 0;
var _layerId= '';
var _template = '';
var _lastTooltip = '';
var globalDebug={};


function globalMouse(e) {
	
	// This function is fired whenever the mouse is moved on this document.
	// It allows _mouseX, _mouseY and _layerID to always contain information
	// about what is under the mouse.  _layerID is whatever layer the mouse
	// happens to be over (if any).
	
   if (e == null) { e = window.event; }
   _mouseX = e.clientX;
   _mouseY = e.clientY;
   var target = e.target != null ? e.target : e.srcElement;    
   _layerId= target.id;
}



/*
function popTimer(firstName, lastName, email, idx, divId, obj) {
	   cmd='popAuth("'+firstName+'","'+lastName+'","'+email+'",'+idx+',"'+divId+'","'+obj.id+'")';
	   setTimeout(cmd,500);
}
function popAuth(firstName, lastName, email, idx, divId, obj) {
	   if (obj==_layerId) {
	   	   tooltipPop(firstName, lastName, email, idx, divId, obj);
	   } 
}
*/

function populateTooltip(responseTxt, err, responseXML) {

    var str = 'There was an error processing this request';
    if ((err==200)) {
       results= responseXML.getElementsByTagName('profile');
       var i=0;
       if (results.length>0) {
          try {
             var loc = results[i].getElementsByTagName('location')[0].firstChild.nodeValue;
          } catch (ex) {
             var loc = '';
          }
          try {
             var firstname = results[i].getElementsByTagName('firstname')[0].firstChild.nodeValue;
          } catch (ex) {
             var firstname = '';
          }
          try {
             var lastname = results[i].getElementsByTagName('lastname')[0].firstChild.nodeValue;
          } catch (ex) {
             var lastname = '';
          }
          try {
             var org = results[i].getElementsByTagName('organization')[0].firstChild.nodeValue;
          } catch (ex) {
             var org = '';
          }
//          try {
             var tmp = results[i].getElementsByTagName('workspace');
             ws='<ul>';
             for (var ii=0; ii<tmp.length; ii++) {
                    url = tmp[ii].getElementsByTagName('url')[0].firstChild.nodeValue;
                   titlex = tmp[ii].getElementsByTagName('title')[0].firstChild.nodeValue;
                   ws+='<li><a href="'+url+'">'+titlex+'</a></li>';
             }
             ws+='</ul>';
//          } catch (ex) {
             //var ws = '';
          //}
          try {
             var profile = results[i].getElementsByTagName('profile_url')[0].firstChild.nodeValue;
          } catch (ex) {
             var profile = '';
          }
          try {
             var history = results[i].getElementsByTagName('history_url')[0].firstChild.nodeValue;
          } catch (ex) {
             var history = '';
          }
          try {
             var img = '<img width="75px" height="99px alt="Member Image" src="'+results[i].getElementsByTagName('image_url')[0].firstChild.nodeValue+'">';
          } catch (ex) {
             var img = '';
          }
          var str=_template.replace(/%firstName/ig,firstname);
              str=str.replace(/%lastName/ig,lastname);
//              str=str.replace(/%email/ig,email);
              str=str.replace(/%org/ig,org);
              str=str.replace(/%loc/ig,loc);
              str=str.replace(/%img/ig,img);
              str=str.replace(/%ws/ig,ws);
              str=str.replace(/%history/ig,history);
              str=str.replace(/%profile/ig,profile);
        }
    }
    if (_lastTooltip==str) {
        tooltipUnPop();
        _lastTooltip=_template;
    } else {
        _tooltipId.innerHTML=str;
          _lastTooltip=str;
    }
}

function tooltipPop(href, obj) {
	 obj=obj.id;
	 if (!_tooltipId) {
	    _tooltipId=document.getElementById('toolTip1');
	    _template=_tooltipId.innerHTML;
	 }
	 
   _tooltipId.style.height='auto';
   _tooltipId.style.overflow='visible';
   _tooltipId.style.overflow='hidden';
   _tooltipId.style.MozBorderRadius='5px';
   _tooltipId.style.left=_mouseX+10+'px';
   _tooltipId.style.display='block';
   _tooltipId.style.visibility='visible';
   var offset = document.documentElement.scrollTop;
   offset=offset+25+_mouseY;
   offset=offset-_tooltipId.offsetHeight-23;
   if (offset<document.documentElement.scrollTop) {
   	   offset=document.documentElement.scrollTop+10;
   }
   _tooltipId.style.top=offset+'px';
   _tooltipId.innerHTML='';
   var pajax = new ajaxObject(href,populateTooltip);
   pajax.update();
   return false;
}

function tooltipUnPop() {
	 if (!_tooltipId) {
	    _tooltipId=document.getElementById('toolTip1');
	    _template=_tooltipId.innerHTML;
	 }
   _tooltipId.style.display='none';
   _lastTooltip=_template;
}

Date.prototype.getMonthName = function() {
   return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][this.getMonth()]; 
}
      	 

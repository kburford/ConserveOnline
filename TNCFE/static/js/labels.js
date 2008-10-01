

var labeldata;


// This object handles the ajax calls.
// Slightly modified from the original to prevent flooding.
function ajaxObject(callbackFunction) {
    var that = this;
    this .updating = false;
    this .lastRequest = 0;
    this .lastData = '';
    this .abort = function () {
        if (that.updating) {
            that.updating = false;
            that.AJAX.abort();
            that.AJAX = null;
        }
    }
    this .update = function (passData, postMethod, noCache) {
        that.callback(false, false, false);
        return;        
    }
    this .callback = callbackFunction || function () {
    };
}

// This function returns the top and left values of the object.
// a somewhat non-trivial task.
function findPos(obj) {
    // This function copyleft quirksmode.org
    var curleft = curtop = 0;
    if (obj.offsetParent) {
        curleft = obj.offsetLeft
        curtop = obj.offsetTop
        while (obj = obj.offsetParent) {
            curleft += obj.offsetLeft
            curtop += obj.offsetTop
        }
    }
    return [curleft, curtop];
}


// This is the actual code for the page, placed inside a LABELS namespace
// to prevent name collisions.

 var LABELS = function() {
           
            // initialize the dropdown box & popup add box
            var dropDown = false;
            var popBox = false;
            var nameField = 'form.labels'; 
            var labels = null;         // The label data.
            var elementFocus = null;   // which element has the focus?
            var labelId=0;             // Unique label ID counter
            
            return {
              
               trapEnter: function(ev) {
                 // If the user is inside the drop-down select box and hits enter, this is what we do.
                 if (ev == null) { ev = window.event }                
                 if (ev.keyCode==13) {
				           dropDown.theTarget.focus();
                   setTimeout("document.getElementById('keySearchDiv').style.display='none'",10);
                 }
               },
               trapBlur : function() {
                 // Called by a set-timeout when an as you type lookup element loses focus.
                 // if after a fraction of a second no other lookup element has obtained the
                 // focus, close the results drop-down.
                 if (!LABELS.elementFocus) {
                   document.getElementById('keySearchDiv').style.display='none';
                 }
               },
         
               closeSearch: function() {
                  // Closes the search drop-down division
                  document.getElementById('keySearchDiv').style.display='none';
                  LABELS.addLabel();
               },
               
			   labelsInfo : function(url) {
			       /* Deprecated, popup a warning if it gets used accidentally. */
			       alert("This is using a deprecated function 'labelsInfo'.");
				},
			   
               addLabel : function() {
                 var poplist = document.getElementById('popListID');
                 if (poplist) dropDown.theTarget.value=poplist.value;
                 return
               },
			   
			   setNameField : function(nf) {
				   nameField=nf;
			   },
               
               
               keySearch : function (obj, ev) {
                 var xy='';
                 var posLeft=0;
                 var posTop=0;
                                  
                 // Sets up and displays the as-you-type drop-down lookup select box.
                 
                 var i; // simple counter
                 if (obj.value==null) {
                   return;
                 }
                 
                 if (ev.keyCode == "188") {
                     // Note that this is for issue1227, don't allow
                     // commas in keyword/label values.
                     var msg = "Please remember that entering special " + 
                        "characters such as a comma become part of the " + 
                        "keyword's name.  \n\nIf you are trying to " + 
                        "enter multiple keywords, use the next keyword field.";
                     alert(msg);
                     return;
                 };
                 
                 if (ev == null) { ev = window.event }
                 if ((ev.keyCode==40)&&(dropDown.style.display=='block')) {
                   // 40= down arrow.
                   dropDown.style.display='block';
                   document.getElementById('popListID').focus();
                   return;
                 }
                 if (ev.keyCode==9) {
                   if (dropDown) {
                     if (dropDown.style.display=='none') { return true }
                     dropDown.style.display='block';
                   }
                   //LABELS.addLabel();
                   return false;
                 }
                 if (ev.keyCode==13) {
                   // 13 = enter
                   LABELS.addLabel();
                   if (dropDown) {
                     dropDown.style.display='none';
                   }
                   //LABELS.keySearch(obj,{});
                   return false;
                 }
				 
				
                 
                 if (!dropDown) {
                    // the drop down division isn't created, so create and style it.
                    dropDown = document.createElement('div');
                    dropDown.style.display='none';
                    dropDown.style.border='none';
                    dropDown.style.maxHeight='200px';
                    dropDown.style.width=obj.offsetWidth-2+'px';
                    dropDown.style.position='absolute';
                    dropDown.style.overflowX='hidden';
                    dropDown.style.overflowY='auto';
                    dropDown.className='ajaxSearchBox';
                    dropDown.id='keySearchDiv';
                    dropDown.style.whiteSpace='nowrap';
                    dropDown.style.zIndex='200';
                    document.getElementsByTagName("body")[0].appendChild(dropDown);
                    dropDown.innerHTML='';
                    xy=findPos(obj);
                    posLeft=xy[0];
                    posTop=xy[1]+obj.offsetHeight-1;
                    dropDown.style.left=posLeft+'px';
                    dropDown.style.top=posTop+'px';
                    dropDown.style.display='none';
                 }
                 dropDown.style.display='none';
                 
                 if (!labels) {
                    // we've never imported the workspace labels so do it.
                    var lid = document.getElementById('labels-list');
                    if (lid) {
                      labels=lid.innerHTML.split('||');
                      for (i=0; i<labels.length; i++) {
                        labels[i]=labels[i].trim();
                      }
                    }
                 }
                 
                   xy=findPos(obj);
                   posLeft=xy[0];
                   posTop=xy[1]+obj.offsetHeight-1;
                    dropDown.style.left=posLeft+'px';
                    dropDown.style.top=posTop+'px';
                 // filter the drop down list to exclude already selected labels
                 var results=[];
//                 if (obj.value=='') {
//                   results=labels;
//                 } else {
                    var rexp=new RegExp('^'+obj.value,'i');
                    for (i=0; i<labels.length; i++) {
                      if (rexp.test(labels[i])) {
                        results.push(labels[i]);
                      }
                    }
//                 }

                 // Build the drop down list.
                 dropDown.style.display='none';
                 if (results.length>0) {
                   fields=document.getElementsByName(nameField);
                   var pageLabels=[];
                   for (i=0; i<fields.length; i++) {
                      pageLabels.push(fields[i].value);
                   } 
                   dropDown.style.display='block';
                   var tmp='<select  onclick="document.getElementById(\''+obj.id+'\').value=this.value;LABELS.closeSearch();" onkeyup="document.getElementById(\''+obj.id+'\').value=this.value; LABELS.trapEnter(event)" id="popListID" onfocus="LABELS.elementFocus=1; document.getElementById(\''+obj.id+'\').value=this.value;" onblur="LABELS.elementFocus=0; LABELS.closeSearch()" name="popList" style="width:'+(dropDown.offsetWidth+2)+'px;" size="';
                   if (results.length>10) {
                      tmp+='10';
                   } else { 
                      tmp+=results.length;
                   }
                   tmp+='">';
                   made=0;
                   for (i=0; i<results.length; i++) {
                     if (!pageLabels.find(results[i])) {
                        tmp+='<option ';
                        made++;
                        if (i==0) { tmp+= ' selected'; }
                        tmp+= ' value="'+results[i]+'"';
                        tmp+='>'+results[i]+'</option>';
                     }
                   }
                   tmp+='</select>';
                   dropDown.style.height='200px';
                   dropDown.style.display='block';
                   if (made < 1) {
                      dropDown.style.display='none';
                   }
                   dropDown.innerHTML=tmp;
                   dropDown.theTarget=obj;
                   if (dropDown.offsetHeight>200) {
                      dropDown.style.height='200px';
                   }
                 } else {
                   dropDown.innerHTML='';
                   dropDown.style.display='none';
                 }
                 
               },
               insertLabel : function(obj) {            
                  var lastLabel    = document.getElementById('last-label-box');
                  var labelExample = document.getElementById('example-label');
            
                  // create the element to insert
                     var newLabelContainer = document.createElement('div');
                     newLabelContainer.className = 'formFieldBox';
					 var newInputBox = document.createElement('div');
					 newInputBox.className = 'labelInputField';
					 newLabelContainer.appendChild(newInputBox);
                     var newLabel = labelExample.cloneNode(false);
                    
            
                     newInputBox.appendChild(newLabel);
					 var labelButton = document.getElementById("addLabelsBtn");
					 var lastBox = document.getElementById("last-label-box");	
					 var removeNode = lastBox.removeChild(labelButton);
					 
					 newLabelContainer.appendChild(removeNode);
					 lastBox.id="";
					 newLabelContainer.id="last-label-box";
					 
					 newLabel.id="labelId"+(labelId++);
                     newLabel.value="";
            
                     document.getElementById("labels-container").insertBefore(newLabelContainer, lastLabel.nextSibling);
					 
        }               
               
            }
         }();

         String.prototype.trim = function() {
           // public domain function
           return this.replace(/^\s+|\s+$/g,"");
         }         

         Array.prototype.find = function(searchStr) {
           // public domain function
           var returnArray = false;
           for (i=0; i<this.length; i++) {
             if (typeof(searchStr) == 'function') {
               if (searchStr.test(this[i])) {
                 if (!returnArray) { returnArray = [] }
                 returnArray.push(i);
               }
             } else {
               if (this[i]===searchStr) {
                 if (!returnArray) { returnArray = [] }
                 returnArray.push(i);
               }
             }
           }
           return returnArray;
         }

window.onclick = LABELS.disp;

// Globals (these are global to aid set-timeout commands).
var ajaxObj = new ajaxObject(LABELS.populateDropdown);
var ajaxEdit = new ajaxObject(LABELS.populateEditBox);



function initLabels () {
    var labelnodes = document.getElementById("labels-list");
    // Assign to a global variable
    if (labelnodes.firstChild) {
        labeldata = labelnodes.firstChild.nodeValue.split("||");
    }
}

function autocompleteOff() {
    document.querySelectorAll("input.labelField").forEach(function(element) {
        element.setAttribute("autocomplete", "off");
    });
}

base2.DOM.bind(document);
document.addEventListener("DOMContentLoaded", initLabels, false);
document.addEventListener("DOMContentLoaded", autocompleteOff, false);
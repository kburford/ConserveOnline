
/* ----------------------------------------

COL3 JS API

These functions and structures are available to end users.  Most
exhibit themselves by injecting behavior into specially-named
DOM nodes, not by being used directly from HTML <script>.

*/

function colShowHide (evt) {

    // This handler is on each portlet box
    var parent = evt.target.parentNode;
    this.querySelectorAll(".content").forEach(function(element) {
        // Toggle display of the box, and reverse the +/-
        if (element.style.display == "none") {
            element.style.display = "block";
            parent.className = "closeButton";
        } else {
            element.style.display = "none";
            parent.className = "openButton";
        };
    });

    // Cancel the default action for clickin an <a>
	evt.preventDefault();
	return false;
};


function colShowPopup (evt) {
    // Simple system for doing popup windows.  It's expected
    // that the @href on the <a> has the URL that should be
    // set for the popup window.
    var url = evt.target.getAttribute("href");
    var title = evt.target.getAttribute("title");
    newwindow=window.open(url,null,"height=500,width=500,scrollbars=yes");
	if (window.focus) {newwindow.focus()}

    // Cancel the default action for clickin an <a>
	evt.preventDefault();
	return false;
};


function colAddAuthor (evt) {
    /* On the Authors widget, add another row for a new author */

    // Grab the container and clone the existing last-author
    var authorsContainer = document.getElementById("authors-container");
    var lastAuthor = document.getElementById('last-author-box');
    var cloneAuthor =  lastAuthor.cloneNode(true);
    base2.DOM.bind(cloneAuthor);

    // Clean up the clone: remove the Add Author button, make it not
    // be an id of last-author.
    var cloneButton = cloneAuthor.querySelector("input[name=submit]");
    cloneAuthor.removeChild(cloneButton);
    cloneAuthor.removeAttribute("id");

    // The last row should now be emptied, as its clone has
    // whatever data was in it
    base2.DOM.bind(lastAuthor);
    var lastHidden = lastAuthor.querySelector("input.hidden");
    lastHidden.value = "";
    lastAuthor.querySelectorAll("input[type=text]").forEach(function(element) {
        element.value = "";
    });

    // Now insert it
    authorsContainer.insertBefore(cloneAuthor, lastAuthor);
};


function colUpdateAuthor (evt) {
    // Update the author lastname/firstname fields from/to
    // a hidden form field.

    // Grab which field changed, plus its parent
    var target = evt.target;
    var parent = target.parentNode;
    base2.DOM.bind(parent);

    // Next, grab the hidden field and its value, and split into
    // lastname/firstname parts
    hidden = parent.querySelector("input.hidden");
    var hiddenvalue = hidden.value;
    var hiddenvalues = hiddenvalue.split(", ");
    var hiddenlast = hiddenvalues[0];
    var hiddenfirst = hiddenvalues[1];
    
    // Based on which visible field we are on, do an update
    var whichpart = target.getAttribute("name").split("-")[1];
    if (whichpart == "lastname") {
        if (target.value == '' && hiddenlast) {
            // If the current value is empty, that means this function 
            // is called on page load.  Thus, read *from* the hidden field 
            // and *into* the visible field.
            target.value = hiddenlast;
        } else {
            // If there is a @value attribute, that means we are
            // called after pageload, when onchange is called. Therefore,
            // assign *from* the target *to* the hidden field.
            // If hiddenfirst is undefined, we are an on add screen,
            // not an edit.
            if (target.value.length > 0) {
            hidden.value = target.value + ", " + hiddenfirst;
            } else {
            hidden.value=hiddenfirst;
            };
        };
    } else if (whichpart == "firstname") {
        if (target.value == '' && hiddenfirst) {
            // If the current value is empty, that means this function 
            // is called on page load.  Thus, read *from* the hidden field 
            // and *into* the visible field.
            // If hiddenfirst is undefined, we are an on add screen,
            // not an edit.
            target.value = hiddenfirst;
        } else {
            // If there is a @value attribute, that means we are
            // called after pageload, when onchange is called. Therefore,
            // assign *from* the target *to* the hidden field.
            if (target.value.length > 0){
            hidden.value = hiddenlast + ", " + target.value;
            } else {
            hidden.value=hiddenlast;
            };
        };   
    };
};



function colShowDiv (evt) {
    // Show the box identified in the node clicked on. For example,
    // a <a id="show-d27"> will show a <div id="d27">

    var toshowid = evt.target.id;
    toshowid = toshowid.substring(5, toshowid.length);
    document.querySelectorAll("#" + toshowid).forEach(function(element) {
        element.style.display = "block";
    });

	evt.preventDefault();
	return false;
};


function colHideDiv (evt) {
    // Hide the box identified in the node clicked on. For example,
    // a <a id="hide-d27"> will hide a <div id="d27">

    var tohideid = evt.target.id;
    tohideid = tohideid.substring(5, tohideid.length);
    document.querySelectorAll("#" + tohideid).forEach(function(element) {
        element.style.display = "none";
    });
	evt.preventDefault();
	return false;
};


function colShowAll (evt) {
	var tags = document.getElementsByTagName('a');
	
	for (var i = 0; i < tags.length; i++)
	{
		var tag = tags[i];
		id = tag.id;
		if(id != "showall" && id != 'hideall')
		{
			var showid =(id.substring(5, id.length));
			var elem = document.getElementById(showid);
			if (elem != null){
				elem.style.display='block';
			}
                                           
                  };
	};
	evt.preventDefault();
	return false;


};


function colHideAll (evt){
	var tags = document.getElementsByTagName('a');
	
	for (var i = 0; i < tags.length; i++)
	{
		var tag = tags[i];
		id = tag.id;
		if(id != "showall" && id != 'hideall')
		{
			var hideid =(id.substring(5, id.length));
			var elem = document.getElementById(hideid);
			if (elem != null) {
				elem.style.display='none';
			}
		};
	};
	evt.preventDefault();
	return false;
};


/* Now wire up functions to nodes by scannning the DOM.
This is called on page load. */

function colInit () {

    // First do popup handlers
    document.querySelectorAll("a.col-showpopup").forEach(function(element) {
        element.addEventListener("click", colShowPopup, false);
    });

    // See if we're on a form, and if so, do some things
    var isform = document.querySelector("head meta[name=formcontroller]");
    if (isform) {

        // Register some handlers based on which form type
        var formtype = isform.getAttribute("content");
        if (formtype == 'file' || formtype == 'libraryfile') {
            document.querySelectorAll("#authors-container input[type=text]").forEach(function(element) {
                // Handle T1236, split Authors into lastname/firstname
                element.addEventListener("change", colUpdateAuthor, false);
                // Simulate the first update by pretending to fire the event
                var evt = new Object();
                evt.target = element;
                colUpdateAuthor(evt);
            });
        };

    };



    // Show/hide toggles on portlets.
    // Put a click handler on the portlet boxes in right column container.
    // All clicks within a particular portlet box
    // will route through this handler.  If the click is on
    // a +/- then we find the content element and toggle its display.
    document.querySelectorAll("#right .show-hide").forEach(function(element) {
        element.addEventListener("click", colShowHide, false);
    });

    // Now do show-hide handlers based.  Do these only in the "content"
    // well, meaning, the middle column.  This is where user-generated
    // content lies.  We use a different, better (toggle-based) facility
    // for the "software.  Unfortunately, we have to live with
    // backwards-compatibility for the CBD workspace.
    var cn;
    var nid;
    var subnid;
    document.querySelectorAll("div.content a").forEach(function(element) {
        cn = element.className;
        nid = element.id;
        subnid = nid.substring(0,5);
        if (subnid == 'show-') {
            element.addEventListener("click", colShowDiv, false);
        } else if (subnid == "hide-") {
            element.addEventListener("click", colHideDiv, false);
        } else if (nid == "showall") {
            element.addEventListener("click", colShowAll, false);
        } else if (nid == "hideall") {
            element.addEventListener("click", colHideAll, false);
        };
    });


    }
base2.DOM.bind(document);
document.addEventListener('DOMContentLoaded', colInit, false);


/* ----------    End COL3 JS API ------------- */



function hideHelpBox(target) {
	var box = document.getElementById(target);
	box.style.display= 'none';
}

//	Text Input

function formInputBlur(target, targetValue)
{
	var elem = document.getElementById(target).value;

	if ((elem.length == 0) || (elem == null))
	{
		if(target == "username")
		{
			document.formLogin.username.value = targetValue;
		}
		else if(target == "password")
		{
			document.formLogin.password.value = targetValue;
		}
	}

}

function formInputFocus(target, targetValue){

	var elem = document.getElementById(target).value;

	if (elem == targetValue)
	{
		if(target == "username")
		{
			document.formLogin.username.value = "";
		}
		else if(target == "password")
		{
			document.formLogin.password.value = "";
		}
	}
}

function showHideRightColumn(target){

	var elem = document.getElementById(target);
	var trigger = document.getElementById(target + "Trigger");

	if (elem.style.display == 'none')
	{
		elem.style.display = 'block';
		trigger.className = "closeButton";
	}
	else
	{
		elem.style.display = 'none';
		trigger.className = "openButton";
	}
}

function showHideVisibility(target){

	var elem = document.getElementById(target);

	if (elem.style.visibility == 'hidden')
	{
		elem.style.visibility = 'visible';
	}
	else
	{
		elem.style.visibility = 'hidden';
	}

}

function showHide(id, target){

	var elem = document.getElementById(target);
	var trigger = document.getElementById(target + "Trigger");

	if(id == "tabs1")
	{
		if (elem.style.display == 'block')
		{
			elem.style.display = 'none';
			trigger.className = 'tab tabClose';
		}
		else
		{
			elem.style.display = 'block';
			trigger.className = 'tab tabOpen';
		}
	}
}

function summariesSwitch(condition)
{
	var images = document.getElementById('listWorkgroup').getElementsByTagName('dt');
	var descriptions = document.getElementById('listWorkgroup').getElementsByTagName('span');

	if(condition == 'hide')
	{
		for (var i = 0; i < images.length; i++)
		{
			var image = images[i];
			var description = descriptions[i];

			idImage = image.id;
			idDescription = description.id;

			document.getElementById(idImage).style.display = 'none';
			document.getElementById(idDescription).style.display = 'none';
			document.getElementById('hideSwitch').style.display = 'none';
			document.getElementById('showSwitch').style.display = 'inline';
		}
	}
	else
	{
		for (var i = 0; i < images.length; i++)
		{
			var image = images[i];
			var description = descriptions[i];

			idImage = image.id;
			idDescription = description.id;

			document.getElementById(idImage).style.display = 'inline';
			document.getElementById(idDescription).style.display = 'inline';
			document.getElementById('hideSwitch').style.display = 'inline';
			document.getElementById('showSwitch').style.display = 'none';
		}
	}

}


var STATEMENT = function () {
	return {
		charCount : function(obj) {
			var chars = new String(obj.value);
			var charsLeft = 1000 - chars.length;
			var charText = document.getElementById('charText');
			if(charsLeft < 0) {
				charsLeft = 0;
			}
			charText.innerHTML = "You have " + charsLeft + " characters remaining.";
		}

	}
}();

function limitText (limitField, limitNum) {
	if (limitField.value.length > limitNum) {
		limitField.value = limitField.value.substring(0, limitNum);
	}
}

/*  New Show/Hide Code */

function toggleLayer(whichLayer) {
  var elem, vis;
  if(document.getElementById) // this is the way the standards work
    elem = document.getElementById(whichLayer);
  else if(document.all) // this is the way old msie versions work
      elem = document.all[whichLayer];
  else if(document.layers) // this is the way nn4 works
    elem = document.layers[whichLayer];
  vis = elem.style;
  // if the style.display value is blank we try to figure it out here
  if(vis.display==''&&elem.offsetWidth!=undefined&&elem.offsetHeight!=undefined)
    vis.display = (elem.offsetWidth!=0&&elem.offsetHeight!=0)?'block':'none';
  vis.display = (vis.display==''||vis.display=='block')?'none':'block';
}

function toggleSub(submenu) {
	    if (document.getElementById(submenu).style.display == 'none') {
	        document.getElementById(submenu).style.display = 'block';
	    } else {
	        document.getElementById(submenu).style.display = 'none';
	    }
	}
	
function switchMenu(obj1, obj2) {
    var el1 = document.getElementById(obj1);
    var el2 = document.getElementById(obj2);
        if ( el1.style.display != 'none' ) {
	    el1.style.display = 'none';
	    el2.src="/static/images/arrowright.gif"
	    } else {
	    el1.style.display = '';
            el2.src="/static/images/arrowdown.gif"
	}
    }





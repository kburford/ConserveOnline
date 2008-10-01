// cross browser function for registering event handlers
var registerEventListener = undefined;

if (typeof addEvent != 'undefined') {
    // use Dean Edwards' function if available
    registerEventListener = function (elem, event, func) {
        addEvent(elem, event, func);
        return true;
    }
} else if (window.addEventListener) {
    registerEventListener = function (elem, event, func) {
        elem.addEventListener(event, func, false);
        return true;
    }
} else if (window.attachEvent) {
    registerEventListener = function (elem, event, func) {
        var result = elem.attachEvent("on"+event, func);
        return result;
    }
} else {
    registerEventListener = function (elem, event, func) {
        // maybe we could implement something with an array
        return false;
    }
}

// cross browser function for unregistering event handlers
var unRegisterEventListener = undefined;

if (typeof removeEvent != 'undefined') {
    // use Dean Edwards' function if available
    unRegisterEventListener = function (elem, event, func) {
        removeEvent(element, event, func);
        return true;
    }
} else if (window.removeEventListener) {
    unRegisterEventListener = function (elem, event, func) {
        elem.removeEventListener(event, func, false);
        return true;
    }
} else if (window.detachEvent) {
    unRegisterEventListener = function (elem, event, func) {
        var result = elem.detachEvent("on"+event, func);
        return result;
    }
} else {
    unRegisterEventListener = function (elem, event, func) {
        // maybe we could implement something with an array
        return false;
    }
}

var registerFunction = undefined;

if (typeof addDOMLoadEvent != 'undefined') {
    registerFunction = function (func) {
        // registers a function to fire ondomload.
        addDOMLoadEvent(func);
    }
} else {
    registerFunction = function (func) {
        // registers a function to fire onload.
        registerEventListener(window, "load", func);
    }
}

// getElementsByClassName()
function getEleentsByClassName(root, classname, tag) {
    var startDateContainer = document.getElementById(root);
    containers = startDateContainer.getElementsByTagName(tag);
    for(var i=0; i < containers.length; i++){
        if (containers[i].className == classname) {
            return containers[i];
        }
    }            
}

// containing package - all our JS will go in here.
var TNC = {};

TNC.initDatePicker = function(){
    // select values from hidden divs and initialize datepickers for 
    // startDate and EndDate for Events get startDate's values from 
    // hidden div on page
    var fieldType = document.getElementById("fieldType").innerHTML;
	if (fieldType == "form.dateauthored") {
		var aDate = getEleentsByClassName("form.dateauthored-wrapper", "DateVal-form.dateauthored", "DIV");
		var sDate = '';
		var eDate = '';
	}
	else {
		var sDate = getEleentsByClassName("form.startDate-wrapper", "DateVal-form.startDate", "DIV");
		var eDate = getEleentsByClassName("form.endDate-wrapper", "DateVal-form.endDate", "DIV");
		var aDate = '';
	}
	
    if(sDate != ''){
        var div1Values = sDate.firstChild.nodeValue.split("::");
        if (div1Values != ''){
	    // Set AM/PM based on value of 24-hour hour
	    var ampmvalue;
	    var oldhourvalue = Number(div1Values[4]);
	    var newhourvalue = div1Values[4];
	    if ((oldhourvalue > 1) && (oldhourvalue < 12)) {
		ampmvalue = 0;
	    } else if (oldhourvalue == 0) {
		ampmvalue = 0;
		newhourvalue = "12";
	    } else if (oldhourvalue == 12) {
		ampmvalue = 1;
	    } else if (oldhourvalue > 12) {
		ampmvalue = 1;
		newhourvalue = String(oldhourvalue - 12);
	    };
            var settings = {
                yfield: div1Values[0] + "-year", 
                yvalue:div1Values[1],
                mfield:div1Values[0] + "-month",    
                mvalue: div1Values[2], 
                dfield: div1Values[0] + "-day", 
                dvalue: div1Values[3], 
                hfield: div1Values[0] + "-hour", 
                hvalue: newhourvalue, //div1Values[4], 
                minfield: div1Values[0] + "-minute", 
                minvalue: div1Values[5],
                ampmfield: div1Values[0] + "-ampm", 
                ampmvalue: ampmvalue
            };
            Calendar.setInitValues(settings); 
            var settings2 = {
                inputField : div1Values[0],
                ifFormat : "%Y-%m-%d %H:%M", 
                onUpdate: catcalc, 
                button : "trigger-"+div1Values[0], 
                yfield :div1Values[0]+"-year", 
                mfield : div1Values[0]+"-month", 
                dfield : div1Values[0]+"-day",
                hfield : div1Values[0]+"-hour", 
                minfield : div1Values[0]+"-minute",  
                showsTime: false
            }
            Calendar.setup(settings2);

        }
    };

    // start initializing Calendar's end date
    if(eDate != ''){
        var div2Values = eDate.firstChild.nodeValue.split("::");
        if (div2Values != ''){
	    // Set AM/PM based on value of 24-hour hour
	    var ampmvalue;
	    var oldhourvalue = Number(div2Values[4]);
	    var newhourvalue = div2Values[4];
	    if ((oldhourvalue > 1) && (oldhourvalue < 12)) {
		ampmvalue = 0;
	    } else if (oldhourvalue == 0) {
		ampmvalue = 0;
		newhourvalue = "12";
	    } else if (oldhourvalue == 12) {
		ampmvalue = 1;
	    } else if (oldhourvalue > 12) {
		ampmvalue = 1;
		newhourvalue = String(oldhourvalue - 12);
	    };
            var settings = {
                yfield: div2Values[0] + "-year", 
                yvalue:div2Values[1],
                mfield:div2Values[0] + "-month", 
                mvalue: div2Values[2], 
                dfield: div2Values[0] + "-day", 
                dvalue: div2Values[3], 
                hfield: div2Values[0] + "-hour", 
                hvalue: newhourvalue, //div2Values[4], 
                minfield: div2Values[0] + "-minute", 
                minvalue: div2Values[5],
                ampmfield: div2Values[0] + "-ampm", 
                ampmvalue: ampmvalue
            };
            Calendar.setInitValues(settings); 
            var settings2 = {
                inputField : div2Values[0],
                ifFormat : "%Y-%m-%d %H:%M", 
                onUpdate: catcalc, 
                button : "trigger-"+div2Values[0], 
                yfield :div2Values[0]+"-year", 
                mfield : div2Values[0]+"-month", 
                dfield : div2Values[0]+"-day",
                hfield : div2Values[0]+"-hour", 
                minfield : div2Values[0]+"-minute",  
                showsTime: false
            }
            Calendar.setup(settings2);
        }
    };
	if(aDate != ''){
        var div2Values = aDate.firstChild.nodeValue.split("::");
        if (div2Values != ''){
            var settings = {
                yfield: div2Values[0] + "-year", 
                yvalue:div2Values[1],
                mfield:div2Values[0] + "-month", 
                mvalue: div2Values[2], 
                dfield: div2Values[0] + "-day", 
                dvalue: div2Values[3], 
                hfield: div2Values[0] + "-hour", 
                hvalue: div2Values[4], 
                minfield: div2Values[0] + "-minute", 
                minvalue: div2Values[5]              
            };
            Calendar.setInitValues(settings); 
            var settings2 = {
                inputField : div2Values[0],
                ifFormat : "%Y-%m-%d %H:%M", 
                onUpdate: catcalc, 
                button : "trigger-"+div2Values[0], 
                yfield :div2Values[0]+"-year", 
                mfield : div2Values[0]+"-month", 
                dfield : div2Values[0]+"-day",
                hfield : div2Values[0]+"-hour", 
                minfield : div2Values[0]+"-minute",  
                showsTime: false
            }
            Calendar.setup(settings2);
        }
    };
}
// end of calendar intialization

// Initialize everything
registerFunction(TNC.initDatePicker);
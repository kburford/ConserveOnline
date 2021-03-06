/*
 * Ext JS Library 1.0.1
 * Copyright(c) 2006-2007, Ext JS, LLC.
 * licensing@extjs.com
 * 
 * http://www.extjs.com/license
 */

/* Fix for Opera, which does not seem to include the map function on Array's */
if(!Array.prototype.map){
    Array.prototype.map = function(fun){
	var len = this.length;
	if(typeof fun != "function"){
	    throw new TypeError();
	}
	var res = new Array(len);
	var thisp = arguments[1];
	for(var i = 0; i < len; i++){
	    if(i in this){
		res[i] = fun.call(thisp, this[i], i, this);
	    }
	}
        return res;
     };
}

/* Paging Memory Proxy, allows to use paging grid with in memory dataset */
Ext.data.PagingMemoryProxy = function(data) {
	Ext.data.PagingMemoryProxy.superclass.constructor.call(this);
	this.data = data;
};

Ext.extend(Ext.data.PagingMemoryProxy, Ext.data.MemoryProxy, {
	load : function(params, reader, callback, scope, arg) {
		params = params || {};
		var result;
		try {
			result = reader.readRecords(this.data);
		}catch(e){
			this.fireEvent("loadexception", this, arg, null, e);
			callback.call(scope, null, arg, false);
			return;
		}
		if ( (params.start!==undefined) && (params.limit!==undefined) ) {
			result.records = result.records.slice(params.start, params.start+params.limit);
		}
		callback.call(scope, result, arg, true);
	}
});

/* multi-lang.js extscript */
Ext.onReady(function(){
	Ext.QuickTips.init();
	Ext.form.Field.prototype.msgTarget = 'side';
	
	/* Language chooser combobox  */
    var store = new Ext.data.SimpleStore({
        fields: ['code', 'language', 'charset'],
        data : Ext.exampledata.languages // from languages.js
    });
    var combo = new Ext.form.ComboBox({
        store: store,
        displayField:'language',
        typeAhead: true,
        mode: 'local',
        triggerAction: 'all',
        emptyText:'Select a language...',
        selectOnFocus:true,
	onSelect: function(record) {
	    window.location.search = Ext.urlEncode({"lang":record.get("code"),"charset":record.get("charset")});
	}
    });
    combo.applyTo('languages');

    // get the selected language code parameter from url (if exists)
    var params = Ext.urlDecode(window.location.search.substring(1));
    if (params.lang) {
	// check if there's really a language with that language code
	record = store.data.find(function(item, key) {
	    if (item.data.code==params.lang){
		return true;
	    }
	});
	// if language was found in store assign it as current value in combobox
	if (record) {
	    combo.setValue(record.data.language);
	}
    }

	/* Email field */
	var efield = new Ext.form.Form({ labelWidth: 75 });
	efield.add(new Ext.form.TextField({
		fieldLabel: 'Email',
		name: 'email',
		vtype: 'email',
		width: 175
	}));
	efield.render('form-ct');

	/* Datepicker */
	var efield = new Ext.form.Form({ labelWidth: 75 });
	efield.add(new Ext.form.DateField({
		fieldLabel: 'Date',
		name: 'date',
		width: 175
	}));
	efield.render('form-ct2');
});

Ext.onReady(function(){
    // shorthand alias
    var fm = Ext.form, Ed = Ext.grid.GridEditor;
    // the column model has information about grid columns
    // dataIndex maps the column to the specific data field in
    // the data store (created below)
    var cm = new Ext.grid.ColumnModel([{
           header: "Months of the year",
           dataIndex: 'month',
           editor: new Ed(new fm.TextField({
               allowBlank: false
           })),
           width: 240
        }]);

    // by default columns are sortable
    cm.defaultSortable = true;

	var monthArray = Date.monthNames.map(function (e) { return [e]; });

    // create the Data Store
    var ds = new Ext.data.Store({
		proxy: new Ext.data.PagingMemoryProxy(monthArray),
		reader: new Ext.data.ArrayReader({}, [
			{name: 'month'}
		])
    });

    // create the editor grid
    var grid = new Ext.grid.EditorGrid('editor-grid', {
        ds: ds,
        cm: cm,
        selModel: new Ext.grid.RowSelectionModel(),
        enableColLock:false
    });

    var layout = Ext.BorderLayout.create({
        center: {
            margins:{left:3,top:3,right:3,bottom:3},
            panels: [new Ext.GridPanel(grid)]
        }
    }, 'grid-panel');

    // render it
    grid.render();

    var gridFoot = grid.getView().getFooterPanel(true);

    // add a paging toolbar to the grid's footer
    var paging = new Ext.PagingToolbar(gridFoot, ds, {
        pageSize: 6,
        displayInfo: false
    });

    // trigger the data store load
    ds.load({params:{start:0, limit:6}});
});

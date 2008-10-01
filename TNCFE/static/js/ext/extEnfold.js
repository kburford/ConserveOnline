
function delMember() {

   // this function will call the each method of the data store (ds), 
	 // a global variable created by onReady, the each method calls the checkEach
	 // function.   If the data record (p)'s index matches the passed index,
	 // a confirm delete box is displayed, and if 'yes' is selected, the 
	 // processYesNo function will remove the requested record.

   var checkEach = function(p) {
	    // called by ds.each for each record in the data store.
			idx = p.data.id;
			cbox = document.getElementById('remove'+idx);
			if (cbox.checked) {
            ds.remove(p);
      }			   
	 }
	 
	 // For each record in the data store (ds) pass that record to checkEach.
   grid.stopEditing();
   ds.each(checkEach);
   grid.startEditing(0, 0);
}


var _enfoldGlobal_indx=0; // This is an index counter, it maintains a unique number
                          // assigned to each table row created.

Ext.onReady(function(){
					 
	var btn;
	
	var html = '<input type="hidden" name="roster.{id}" value="{lastName}"><input type="hidden" name="roster.{id}" value="{firstName}"><input type="hidden" name="roster.{id}" value="{email}"><input type="hidden" name="roster.indexes:list" value="{id}">';
	
    
  function inviteMember(){
    
	  var idx = _enfoldGlobal_indx;  // Global variable reference
	
		var firstName = Ext.get('firstName').dom.value;
		var lastName = Ext.get('lastName').dom.value;
		var email = Ext.get('email').dom.value;
		var remove = '<center><input type="checkbox" id="remove'+idx+'"></center>';
		
			
		if(firstName == "" || lastName == "" || email == "")
		{
			Ext.MessageBox.alert('Error Message', 'Please Provide a First Name, Last Name and E-Mail Address');
		}		
//		else if (!/[+\w\.-]*\@[\w\.-]*\.+[a-zA-Z][a-zA-Z\.]+[a-zA-Z]/i.test(email))
		else if (!/^[\w-]+(?:\.[\w-]+)*@(?:[\w-]+\.)+[a-zA-Z]{2,7}$/i.test(email))

		{
			Ext.MessageBox.alert('Error Message', 'Please Provide a Valid E-Mail Address');
		}
		else
		{
		  _enfoldGlobal_indx++;
			var p = new Member({
				firstName: firstName,
				lastName: lastName,
				email: email,
				remove: remove,
				id: idx
			});
			grid.stopEditing();     
			ds.insert(0, p);
			grid.startEditing(0, 0);

			var tpl = new Ext.Template(html);
			tpl.compile();
		
			tpl.append('inputValues', {
				firstName: firstName,
				lastName: lastName,
				email: email,
				id: idx
			});
			
   	}
	};
	
	function formatBoolean(value){
        return value ? 'Yes' : 'No';  
    };
	
    // shorthand alias
    var fm = Ext.form, Ed = Ext.grid.GridEditor;

    // this could be inline, but we want to define the Member record
    // type so we can add records dynamically
    var Member = Ext.data.Record.create([
           // the "name" below matches the tag name to read, except "availDate"
           // which is mapped to the tag "availability"
           {name: 'firstName', type: 'string'},
           {name: 'lastName', type: 'string'},
           {name: 'email', type: 'string'},
           {name: 'remove', type: 'string'}
      ]);

	//	RESERVED FOR AN ARRAY OF DATA TO INCLUDE IN TABLE GRID
	var xmlData = [];

    // create the Data Store
		
		// We're leaving off the var so this becomes a global variable thru closures.
    ds = new Ext.data.Store({
		        proxy: new Ext.data.MemoryProxy(xmlData),
		        reader: new Ext.data.ArrayReader({}, Member)
        });
	
	 // the column model has information about grid columns
    // dataIndex maps the column to the specific data field in
    // the data store (created below)
    var cm = new Ext.grid.ColumnModel([{
           header: "First Name",
           dataIndex: 'firstName',
           width: 175
        },{
           header: "Last Name",
           dataIndex: 'lastName',
           width: 175
        },{
           header: "E-Mail Address",
           dataIndex: 'email',
           width: 175
        },{
           header: "Remove",
           dataIndex: 'remove',
           width: 65
        }]);

    // by default columns are sortable
    cm.defaultSortable = true;

    // create the editor grid


		// We're leaving off the var so this becomes a global variable thru closures.
    grid = new Ext.grid.EditorGrid('editor-grid', {
        ds: ds,
        cm: cm,
        //selModel: new Ext.grid.RowSelectionModel(),
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

    // trigger the data store load
    ds.load();
	
	//	var btn = document.getElementById('btnInvite');
	btn = Ext.get('btnInvite');
	btn.on('click', inviteMember);
	//	btn.onClick = inviteMember;
	var btn2 = Ext.get('btnRemove');
	btn2.on('click', delMember);
	
});
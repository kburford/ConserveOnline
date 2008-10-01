Ext.onReady(function(){

	var btn;
    
    function inviteMember(){
	
		var firstName = Ext.get('firstName').dom.value;
		var lastName = Ext.get('lastName').dom.value;
		var email = Ext.get('email').dom.value;
		var id = Ext.id();
		
		if(firstName == "" || lastName == "" || email == "")
		{
			Ext.MessageBox.alert('Error Message', 'Please Provide a First Name, Last Name and E-Mail Address');
		}		
		else
		{
		
			var p = new Member({
				firstName: firstName,
				lastName: lastName,
				email: email,
				remove: false
			});
			
			grid.stopEditing();
			ds.insert(0, p);
			grid.startEditing(0, 0);
		}
		
	};
	
	function formatBoolean(value){
        return value ? 'Yes' : 'No';  
    };
	
    // shorthand alias
    var fm = Ext.form, Ed = Ext.grid.GridEditor;

    // the column model has information about grid columns
    // dataIndex maps the column to the specific data field in
    // the data store (created below)
    var cm = new Ext.grid.ColumnModel([{
           header: "First Name",
           dataIndex: 'firstName',
           width: 175,
           editor: new Ed(new fm.TextField({
               allowBlank: false
           }))
        },{
           header: "Last Name",
           dataIndex: 'lastName',
           width: 175,
           editor: new Ed(new fm.TextField({
               allowBlank: false
           }))
        },{
           header: "E-Mail Address",
           dataIndex: 'email',
           width: 175,
           editor: new Ed(new fm.TextField({
               allowBlank: false
           }))
        },{
           header: "Remove",
           dataIndex: 'remove',
           width: 65,
           renderer: formatBoolean,
           editor: new Ed(new fm.Checkbox())
        }]);

    // by default columns are sortable
    cm.defaultSortable = true;

    // this could be inline, but we want to define the Member record
    // type so we can add records dynamically
    var Member = Ext.data.Record.create([
           // the "name" below matches the tag name to read, except "availDate"
           // which is mapped to the tag "availability"
           {name: 'firstName', type: 'string'},
           {name: 'lastName', type: 'string'},
           {name: 'email', type: 'string'},
           {name: 'remove', type: 'bool'}
      ]);

    // create the Data Store
    var ds = new Ext.data.Store({
        // load using HTTP
        proxy: new Ext.data.HttpProxy({url: 'js/ext-1.0.1/tutorial/inviteMembers.xml'}),

        // the return will be XML, so lets set up a reader
        reader: new Ext.data.XmlReader({
               // records will have a "plant" tag
               record: 'plant'
           }, Member)
    });

    // create the editor grid
    var grid = new Ext.grid.EditorGrid('editor-grid', {
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
	
	btn = Ext.get('btnInvite');
	btn.on('click', inviteMember)
	
});
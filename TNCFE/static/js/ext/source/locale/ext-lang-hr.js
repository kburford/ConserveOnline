/*
 * Ext JS Library 1.0.1
 * Copyright(c) 2006-2007, Ext JS, LLC.
 * licensing@extjs.com
 * 
 * http://www.extjs.com/license
 */

/*
 * Croatian translation
 * By Ylodi (utf8 encoding)
 * 10 April 2007
 */
 
Ext.UpdateManager.defaults.indicatorText = '<div class="loading-indicator">Učitavanje...</div>';

if(Ext.View){
   Ext.View.prototype.emptyText = "";
}

if(Ext.grid.Grid){
   Ext.grid.Grid.prototype.ddText = "{0} odabranih redova";
}

if(Ext.TabPanelItem){
   Ext.TabPanelItem.prototype.closeText = "Zatvori ovaj tab";
}

if(Ext.form.Field){
   Ext.form.Field.prototype.invalidText = "Vrijednost u ovom polju je neispravna";
}

Date.monthNames = [
   "Siječanj",
   "Veljača",
   "Ožujak",
   "Travanj",
   "Svibanj",
   "Lipanj",
   "Srpanj",
   "Kolovoz",
   "Rujan",
   "Listopad",
   "Studeni",
   "Prosinac"
];

Date.dayNames = [
   "Nedelja",
   "Ponedeljak",
   "Utorak",
   "Srijeda",
   "Četvrtak",
   "Petak",
   "Subota"
];

if(Ext.MessageBox){
   Ext.MessageBox.buttonText = {
      ok     : "U redu",
      cancel : "Odustani",
      yes    : "Da",
      no     : "Ne"
   };
}

if(Ext.util.Format){
   Ext.util.Format.date = function(v, format){
      if(!v) return "";
      if(!(v instanceof Date)) v = new Date(Date.parse(v));
      return v.dateFormat(format || "d/m/Y");
   };
}

if(Ext.DatePicker){
   Ext.apply(Ext.DatePicker.prototype, {
      todayText         : "Danas",
      minText           : "Taj datum je prije najmanjeg datuma",
      maxText           : "Taj datum je poslije najvećeg datuma",
      disabledDaysText  : "",
      disabledDatesText : "",
      monthNames	: Date.monthNames,
      dayNames		: Date.dayNames,
      nextText          : 'Slijedeći mjesec (Control+Desno)',
      prevText          : 'Prethodni mjesec (Control+Lijevo)',
      monthYearText     : 'Odaberite mjesec (Control+Gore/Dolje za promjenu godine)',
      todayTip          : "{0} (Razmaknica)",
      format            : "d/m/y",
      startDay 		 : 1
   });
}

if(Ext.PagingToolbar){
   Ext.apply(Ext.PagingToolbar.prototype, {
      beforePageText : "Stranica",
      afterPageText  : "od {0}",
      firstText      : "Prva stranica",
      prevText       : "Prethodna stranica",
      nextText       : "Slijedeća stranica",
      lastText       : "Zadnja stranica",
      refreshText    : "Obnovi",
      displayMsg     : "Prikazujem {0} - {1} od {2}",
      emptyMsg       : 'Nema podataka za prikaz'
   });
}

if(Ext.form.TextField){
   Ext.apply(Ext.form.TextField.prototype, {
      minLengthText : "Minimalna dužina za ovo polje je {0}",
      maxLengthText : "Maksimalna dužina za ovo polje je {0}",
      blankText     : "Ovo polje je obavezno",
      regexText     : "",
      emptyText     : null
   });
}

if(Ext.form.NumberField){
   Ext.apply(Ext.form.NumberField.prototype, {
      minText : "Minimalna vrijednost za ovo polje je {0}",
      maxText : "Maksimalna vrijednost za ovo polje je {0}",
      nanText : "{0} is not a valid number"
   });
}

if(Ext.form.DateField){
   Ext.apply(Ext.form.DateField.prototype, {
      disabledDaysText  : "Neaktivno",
      disabledDatesText : "Neaktivno",
      minText           : "Datum u ovom polje mora biti poslije {0}",
      maxText           : "Datum u ovom polju mora biti prije {0}",
      invalidText       : "{0} nije ispravan datum - mora biti u obliku {1}",
      format            : "d/m/y"
   });
}

if(Ext.form.ComboBox){
   Ext.apply(Ext.form.ComboBox.prototype, {
      loadingText       : "Učitavanje...",
      valueNotFoundText : undefined
   });
}

if(Ext.form.VTypes){
   Ext.apply(Ext.form.VTypes, {
      emailText    : 'Ovo polje treba biti e-mail adresa u obliku "korisnik@domena.com"',
      urlText      : 'Ovo polje treba biti URL u obliku "http:/'+'/www.domena.com"',
      alphaText    : 'Ovo polje treba sadržavati samo slova i znak _',
      alphanumText : 'Ovo polje treba sadržavati samo slova, brojeve i znak _'
   });
}

if(Ext.grid.GridView){
   Ext.apply(Ext.grid.GridView.prototype, {
      sortAscText  : "Sortiraj rastućim redoslijedom",
      sortDescText : "Sortiraj padajućim redoslijedom",
      lockText     : "Zaključaj stupac",
      unlockText   : "Otključaj stupac",
      columnsText  : "Stupci"
   });
}

if(Ext.grid.PropertyColumnModel){
   Ext.apply(Ext.grid.PropertyColumnModel.prototype, {
      nameText   : "Naziv",
      valueText  : "Vrijednost",
      dateFormat : "j/m/Y"
   });
}

if(Ext.SplitLayoutRegion){
   Ext.apply(Ext.SplitLayoutRegion.prototype, {
      splitTip            : "Povuci za promjenu veličine.",
      collapsibleSplitTip : "Povuci za promjenu veličine. Dvostruki klik za skrivanje."
   });
}

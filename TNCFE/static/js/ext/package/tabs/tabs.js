/*
 * Ext JS Library 1.0.1
 * Copyright(c) 2006-2007, Ext JS, LLC.
 * licensing@extjs.com
 * 
 * http://www.extjs.com/license
 */

Ext.TabPanel=function(_1,_2){this.el=Ext.get(_1,true);if(_2){if(typeof _2=="boolean"){this.tabPosition=_2?"bottom":"top";}else{Ext.apply(this,_2);}}if(this.tabPosition=="bottom"){this.bodyEl=Ext.get(this.createBody(this.el.dom));this.el.addClass("x-tabs-bottom");}this.stripWrap=Ext.get(this.createStrip(this.el.dom),true);this.stripEl=Ext.get(this.createStripList(this.stripWrap.dom),true);this.stripBody=Ext.get(this.stripWrap.dom.firstChild.firstChild,true);if(Ext.isIE){Ext.fly(this.stripWrap.dom.firstChild).setStyle("overflow-x","hidden");}if(this.tabPosition!="bottom"){this.bodyEl=Ext.get(this.createBody(this.el.dom));this.el.addClass("x-tabs-top");}this.items=[];this.bodyEl.setStyle("position","relative");this.active=null;this.activateDelegate=this.activate.createDelegate(this);this.addEvents({"tabchange":true,"beforetabchange":true});Ext.EventManager.onWindowResize(this.onResize,this);this.cpad=this.el.getPadding("lr");this.hiddenCount=0;Ext.TabPanel.superclass.constructor.call(this);};Ext.extend(Ext.TabPanel,Ext.util.Observable,{tabPosition:"top",currentTabWidth:0,minTabWidth:40,maxTabWidth:250,preferredTabWidth:175,resizeTabs:false,monitorResize:true,addTab:function(id,_4,_5,_6){var _7=new Ext.TabPanelItem(this,id,_4,_6);this.addTabItem(_7);if(_5){_7.setContent(_5);}return _7;},getTab:function(id){return this.items[id];},hideTab:function(id){var t=this.items[id];if(!t.isHidden()){t.setHidden(true);this.hiddenCount++;this.autoSizeTabs();}},unhideTab:function(id){var t=this.items[id];if(t.isHidden()){t.setHidden(false);this.hiddenCount--;this.autoSizeTabs();}},addTabItem:function(_d){this.items[_d.id]=_d;this.items.push(_d);if(this.resizeTabs){_d.setWidth(this.currentTabWidth||this.preferredTabWidth);this.autoSizeTabs();}else{_d.autoSize();}},removeTab:function(id){var _f=this.items;var tab=_f[id];if(!tab){return;}var _11=_f.indexOf(tab);if(this.active==tab&&_f.length>1){var _12=this.getNextAvailable(_11);if(_12){_12.activate();}}this.stripEl.dom.removeChild(tab.pnode.dom);if(tab.bodyEl.dom.parentNode==this.bodyEl.dom){this.bodyEl.dom.removeChild(tab.bodyEl.dom);}_f.splice(_11,1);delete this.items[tab.id];tab.fireEvent("close",tab);tab.purgeListeners();this.autoSizeTabs();},getNextAvailable:function(_13){var _14=this.items;var _15=_13;while(_15<_14.length){var _16=_14[++_15];if(_16&&!_16.isHidden()){return _16;}}_15=_13;while(_15>=0){var _16=_14[--_15];if(_16&&!_16.isHidden()){return _16;}}return null;},disableTab:function(id){var tab=this.items[id];if(tab&&this.active!=tab){tab.disable();}},enableTab:function(id){var tab=this.items[id];tab.enable();},activate:function(id){var tab=this.items[id];if(!tab){return null;}if(tab==this.active){return tab;}var e={};this.fireEvent("beforetabchange",this,e,tab);if(e.cancel!==true&&!tab.disabled){if(this.active){this.active.hide();}this.active=this.items[id];this.active.show();this.fireEvent("tabchange",this,this.active);}return tab;},getActiveTab:function(){return this.active;},syncHeight:function(_1e){var _1f=(_1e||this.el.getHeight())-this.el.getBorderWidth("tb")-this.el.getPadding("tb");var bm=this.bodyEl.getMargins();var _21=_1f-(this.stripWrap.getHeight()||0)-(bm.top+bm.bottom);this.bodyEl.setHeight(_21);return _21;},onResize:function(){if(this.monitorResize){this.autoSizeTabs();}},beginUpdate:function(){this.updating=true;},endUpdate:function(){this.updating=false;this.autoSizeTabs();},autoSizeTabs:function(){var _22=this.items.length;var _23=_22-this.hiddenCount;if(!this.resizeTabs||_22<1||_23<1||this.updating){return;}var w=Math.max(this.el.getWidth()-this.cpad,10);var _25=Math.floor(w/_23);var b=this.stripBody;if(b.getWidth()>w){var _27=this.items;this.setTabWidth(Math.max(_25,this.minTabWidth)-2);if(_25<this.minTabWidth){}}else{if(this.currentTabWidth<this.preferredTabWidth){this.setTabWidth(Math.min(_25,this.preferredTabWidth)-2);}}},getCount:function(){return this.items.length;},setTabWidth:function(_28){this.currentTabWidth=_28;for(var i=0,len=this.items.length;i<len;i++){if(!this.items[i].isHidden()){this.items[i].setWidth(_28);}}},destroy:function(_2b){Ext.EventManager.removeResizeListener(this.onResize,this);for(var i=0,len=this.items.length;i<len;i++){this.items[i].purgeListeners();}if(_2b===true){this.el.update("");this.el.remove();}}});Ext.TabPanelItem=function(_2e,id,_30,_31){this.tabPanel=_2e;this.id=id;this.disabled=false;this.text=_30;this.loaded=false;this.closable=_31;this.bodyEl=Ext.get(_2e.createItemBody(_2e.bodyEl.dom,id));this.bodyEl.setVisibilityMode(Ext.Element.VISIBILITY);this.bodyEl.setStyle("display","block");this.bodyEl.setStyle("zoom","1");this.hideAction();var els=_2e.createStripElements(_2e.stripEl.dom,_30,_31);this.el=Ext.get(els.el,true);this.inner=Ext.get(els.inner,true);this.textEl=Ext.get(this.el.dom.firstChild.firstChild.firstChild,true);this.pnode=Ext.get(els.el.parentNode,true);this.el.on("mousedown",this.onTabMouseDown,this);this.el.on("click",this.onTabClick,this);if(_31){var c=Ext.get(els.close,true);c.dom.title=this.closeText;c.addClassOnOver("close-over");c.on("click",this.closeClick,this);}this.addEvents({"activate":true,"beforeclose":true,"close":true,"deactivate":true});this.hidden=false;Ext.TabPanelItem.superclass.constructor.call(this);};Ext.extend(Ext.TabPanelItem,Ext.util.Observable,{purgeListeners:function(){Ext.util.Observable.prototype.purgeListeners.call(this);this.el.removeAllListeners();},show:function(){this.pnode.addClass("on");this.showAction();if(Ext.isOpera){this.tabPanel.stripWrap.repaint();}this.fireEvent("activate",this.tabPanel,this);},isActive:function(){return this.tabPanel.getActiveTab()==this;},hide:function(){this.pnode.removeClass("on");this.hideAction();this.fireEvent("deactivate",this.tabPanel,this);},hideAction:function(){this.bodyEl.hide();this.bodyEl.setStyle("position","absolute");this.bodyEl.setLeft("-20000px");this.bodyEl.setTop("-20000px");},showAction:function(){this.bodyEl.setStyle("position","relative");this.bodyEl.setTop("");this.bodyEl.setLeft("");this.bodyEl.show();},setTooltip:function(_34){if(Ext.QuickTips&&Ext.QuickTips.isEnabled()){this.textEl.dom.qtip=_34;this.textEl.dom.removeAttribute("title");}else{this.textEl.dom.title=_34;}},onTabClick:function(e){e.preventDefault();this.tabPanel.activate(this.id);},onTabMouseDown:function(e){e.preventDefault();this.tabPanel.activate(this.id);},getWidth:function(){return this.inner.getWidth();},setWidth:function(_37){var _38=_37-this.pnode.getPadding("lr");this.inner.setWidth(_38);this.textEl.setWidth(_38-this.inner.getPadding("lr"));this.pnode.setWidth(_37);},setHidden:function(_39){this.hidden=_39;this.pnode.setStyle("display",_39?"none":"");},isHidden:function(){return this.hidden;},getText:function(){return this.text;},autoSize:function(){this.textEl.setWidth(1);this.setWidth(this.textEl.dom.scrollWidth+this.pnode.getPadding("lr")+this.inner.getPadding("lr"));},setText:function(_3a){this.text=_3a;this.textEl.update(_3a);this.setTooltip(_3a);if(!this.tabPanel.resizeTabs){this.autoSize();}},activate:function(){this.tabPanel.activate(this.id);},disable:function(){if(this.tabPanel.active!=this){this.disabled=true;this.pnode.addClass("disabled");}},enable:function(){this.disabled=false;this.pnode.removeClass("disabled");},setContent:function(_3b,_3c){this.bodyEl.update(_3b,_3c);},getUpdateManager:function(){return this.bodyEl.getUpdateManager();},setUrl:function(url,_3e,_3f){if(this.refreshDelegate){this.un("activate",this.refreshDelegate);}this.refreshDelegate=this._handleRefresh.createDelegate(this,[url,_3e,_3f]);this.on("activate",this.refreshDelegate);return this.bodyEl.getUpdateManager();},_handleRefresh:function(url,_41,_42){if(!_42||!this.loaded){var _43=this.bodyEl.getUpdateManager();_43.update(url,_41,this._setLoaded.createDelegate(this));}},refresh:function(){if(this.refreshDelegate){this.loaded=false;this.refreshDelegate();}},_setLoaded:function(){this.loaded=true;},closeClick:function(e){var o={};e.stopEvent();this.fireEvent("beforeclose",this,o);if(o.cancel!==true){this.tabPanel.removeTab(this.id);}},closeText:"Close this tab"});Ext.TabPanel.prototype.createStrip=function(_46){var _47=document.createElement("div");_47.className="x-tabs-wrap";_46.appendChild(_47);return _47;};Ext.TabPanel.prototype.createStripList=function(_48){_48.innerHTML="<div class=\"x-tabs-strip-wrap\"><table class=\"x-tabs-strip\" cellspacing=\"0\" cellpadding=\"0\" border=\"0\"><tbody><tr></tr></tbody></table></div>";return _48.firstChild.firstChild.firstChild.firstChild;};Ext.TabPanel.prototype.createBody=function(_49){var _4a=document.createElement("div");Ext.id(_4a,"tab-body");Ext.fly(_4a).addClass("x-tabs-body");_49.appendChild(_4a);return _4a;};Ext.TabPanel.prototype.createItemBody=function(_4b,id){var _4d=Ext.getDom(id);if(!_4d){_4d=document.createElement("div");_4d.id=id;}Ext.fly(_4d).addClass("x-tabs-item-body");_4b.insertBefore(_4d,_4b.firstChild);return _4d;};Ext.TabPanel.prototype.createStripElements=function(_4e,_4f,_50){var td=document.createElement("td");_4e.appendChild(td);if(_50){td.className="x-tabs-closable";if(!this.closeTpl){this.closeTpl=new Ext.Template("<a href=\"#\" class=\"x-tabs-right\"><span class=\"x-tabs-left\"><em class=\"x-tabs-inner\">"+"<span unselectable=\"on\""+(this.disableTooltips?"":" title=\"{text}\"")+" class=\"x-tabs-text\">{text}</span>"+"<div unselectable=\"on\" class=\"close-icon\">&#160;</div></em></span></a>");}var el=this.closeTpl.overwrite(td,{"text":_4f});var _53=el.getElementsByTagName("div")[0];var _54=el.getElementsByTagName("em")[0];return {"el":el,"close":_53,"inner":_54};}else{if(!this.tabTpl){this.tabTpl=new Ext.Template("<a href=\"#\" class=\"x-tabs-right\"><span class=\"x-tabs-left\"><em class=\"x-tabs-inner\">"+"<span unselectable=\"on\""+(this.disableTooltips?"":" title=\"{text}\"")+" class=\"x-tabs-text\">{text}</span></em></span></a>");}var el=this.tabTpl.overwrite(td,{"text":_4f});var _54=el.getElementsByTagName("em")[0];return {"el":el,"inner":_54};}};


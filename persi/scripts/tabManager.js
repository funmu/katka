/*
 *  tabManager.js
 *     Module to manage Tabs for website
 *
 *  ToDo: 
 *     Use responsive UI framework to style tabs
 * 
 */

 (function() {

 	'use strict';

 	/*
 	 *	Set up the TabManager Object
 	 *
 	 *  @param{Array} tabsList - array of tabs for display
 	 *  @param{bool} verbose - verbosity level to show values
 	 */
 	var tabManager = function( tabsList, verbose)
 	{
 		this.self = this;
 		this.fVerbose = verbose;
 		this.tabsList = tabsList;

 		if (this.fVerbose) {
 			console.log( "Created a new tab Manager with %d tabs", this.tabsList.length);
 			console.log( this.tabsList);
 		}
 	}

 	/*
 	 *	Set up tabNum tab as the active tab
 	 *
 	 *  @param{int} tabNum - index for the tab to be activated (1..N)
 	 *
 	 *  @return none
 	 */
 	tabManager.prototype.setActiveTab = function( tabNum)
 	{
 		if ((tabNum < 1) || (tabNum > this.tabsList.length)) {

 			throw new { Error: "Invalid Tab Number",
 						Message: "Supplied tab number is not in the right range"
 					};
 		}

 		if (this.fVerbose) { 
 			console.log( " Activating tab: %d. Category=%s", 
 				tabNum, this.tabsList[tabNum-1].category);
 		}

 		var $tabSelector = ".tabs a:nth-child(" + tabNum + ") span";

 		// remove all active class items
 		$(".tabs span").removeClass("active");
 		$($tabSelector).addClass("active");
 		$("main .content").hide();

 		var $contentToShow = "main " + this.tabsList[tabNum-1].contentClass;
 		$($contentToShow).fadeIn();

 		return false;
 	}


 	/*
 	 *	Set up tabs to start with
 	 *
 	 *  @param{string} tabsParent - parent selector node where tabs are attached to
 	 *
 	 *  @return none
 	 */
	tabManager.prototype.setupTabs = function( tabsParent) 
	{
		var $tabs = $(tabsParent);
		
		this.tabsList.forEach( function( item, i) {

			if (this.fVerbose) {
				console.log( "creating new tab [%d]. name=%s",
					i, item.category);
			}

			var $thistab = $("<a href=''>");
			var $tabname = $("<span>");
			$tabname.text( item.category);
			$tabname.addClass( item.contentClass);
			$tabname.on( "click", this.setActiveTab.bind( this, i+1));
			$thistab.append( $tabname);
			$tabs.append( $thistab);
		}, this);
	}

 	if ( (typeof module === 'undefined')) {
 		window.tabManager = tabManager;
 	}

 })();

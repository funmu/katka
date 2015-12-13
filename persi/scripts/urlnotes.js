/*
 *  urlnotes.js
 *     Module to keep track of Notes for URLs
 *
 * 
 */

 (function() {

 	'use strict';

 	var urlnotes = function( verbose)
 	{
 		this.fVerbose = verbose;
 	}

 	var tabContent = [
 		{ tabNum : 1, category: "News", contentClass: ".NewsSites" },
 		{ tabNum : 2, category: "People", contentClass: ".People" },
 		{ tabNum : 3, category: "Add Item", contentClass: ".AddUrl" }
 	];

 	var urlItems = [
	 	{ "label": "CNN", "url": "http://www.cnn.com"},
		{ "label": "NY Times", "url": "http://www.nytimes.com"},
		{ "label": "Seattle Times", "url": "http://www.seattletimes.com"},
		{ "label": "Univ. of Washington News", "url": "http://www.washington.edu/news"}
	];

 	var $activeClass = "";

 	function setActiveTab( tabNum)
 	{
 		var $tabSelector = ".tabs a:nth-child(" + tabNum + ") span";

 		// remove all active class items
 		$(".tabs span").removeClass("active");
 		$($tabSelector).addClass("active");
 		$("main .content").hide();

 		var $contentToShow = "main " + tabContent[tabNum-1].contentClass;
 		$activeClass = $contentToShow;
 		$($contentToShow).fadeIn();

 		return false;
 	}

	function setupActiveTabFunctions() 
	{
		$(".tabs a span").toArray().forEach( function( item, i) {
			// add tab activation handler

	 		$(item).on( "click", setActiveTab.bind(null, i+1));
		});
	}

	setupActiveTabFunctions();
	setActiveTab(2);


 	function handleUrlInput( event) 
 	{
 		var $url = $('#urlInput').val();
 		var $urlNote = $('#urlNoteInput').val();

 		if ( ($url !== "") && ($urlNote !== "")) {

 			var newUrlItem = { label: $urlNote, url: $url};
 			urlItems.push( newUrlItem);

 			var $urlContent = $('.urlNotes ul');
 			$urlContent.empty();
 	 		$urlContent.hide();
 			urlItems.forEach( function( urlItem, i) {
	 			var $alink = "<a href='" + urlItem.url + "' target='_blank'>" + urlItem.label + "</a>";
 				$urlContent.append( $("<li>").append($alink));
 			});

 	 		$urlContent.fadeIn();

	 		$('#urlInput').val("");
	 		$('#urlNoteInput').val("");
	 	}
 	}

 	$(".urlNotes-input button").on('click', handleUrlInput);

 	$(".urlNotes-input button").on('click', handleUrlInput);


 	if ( (typeof module === 'undefined')) {
 		window.urlNotes = urlnotes;
 	}

 })();

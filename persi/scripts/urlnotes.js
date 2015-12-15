/*
 *  urlnotes.js
 *     Module to keep track of Notes for URLs
 *
 *  ToDo: 
 *     Clean up Interactive UI Parts
 *     Separate Data out and enable data binding
 * 
 */

 (function() {

 	'use strict';

 	var urlnotes = function( verbose)
 	{
 		this.fVerbose = verbose;
 	}

 	var urlItems = [
	 	{ "label": "CNN", "url": "http://www.cnn.com"},
		{ "label": "NY Times", "url": "http://www.nytimes.com"},
		{ "label": "Seattle Times", "url": "http://www.seattletimes.com"},
		{ "label": "Univ. of Washington News", "url": "http://www.washington.edu/news"}
	];


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

/*
 *  flicrPhotos.js
 *     Module to get and display Flickr Photos
 * 
 */

 (function() {

 	'use strict';

 	var flickrPhotosLocForTag = "http://api.flickr.com/services/feeds/photos_public.gne?format=json&jsoncallback=?&tags=";

 	var flickrPhotos = function( verbose)
 	{
 		this.fVerbose = verbose;
 	}


 	flickrPhotos.prototype.showPhotos = function( docSelector, photoInputSelector)
 	{
		var photoTag = $(photoInputSelector).val();

		if (photoTag == null) {
			photoTag = "cat";
		}

 		if (this.fVerbose) {
 			console.log( "Fetching photos from [tag=%s] to render in [%s]", 
 				photoTag, docSelector)
 		}

	 	var photosLoc = flickrPhotosLocForTag + photoTag;

 		var $docItem = $(docSelector);
 		$docItem.empty();

 		$.getJSON( photosLoc, function( flickrAnswers) {

 			var $picsList = $("<div>");
 			var items = flickrAnswers.items;

 			items.forEach( function( item, i) {

 				var $img = $("<img>");
 				$img.attr( "src", item.media.m);
 				$img.attr( "alt", item.title);
 				$picsList.append( $img);
 			});

 			$docItem.append( $picsList);
 			$docItem.fadeIn();
 			console.log( flickrAnswers);
 		}, this);
 	}
 	
 	if ( (typeof module === 'undefined')) {
 		window.flickrPhotos = flickrPhotos;
 	}

 })();

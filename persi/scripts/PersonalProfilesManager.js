/*
 *  PersonalProfilesManager.js
 *     Module to get and display Personal Profiles for users
 * 
 */

 (function() {

 	'use strict';

 	var g_twitterBase = "http://www.twitter.com";
 	var g_linkedinBase = "http://www.linkedin.com/in/";

 	var PersonalProfilesManager = function( urlloc, verbose)
 	{
 		this.fVerbose = verbose;
 		this.urlloc = urlloc;
 		this.basepath = getBasePath( urlloc);
 	}

 	function getBasePath( urlloc) 
 	{
		var fullpath = urlloc.pathname;
		var pathparts = fullpath.split(/\/+/g);
		if (pathparts.length > 1) {
			// pop the last part
			pathparts.pop();
		}
		
		if (pathparts.length > 0) {
			// pop one more part if it exists
			pathparts.pop();
		}

		return pathparts.join('/');
 	}

 	/*
 	 *   constructs the location for the configuration per site
 	 *
 	 * Ex:  given the app at http://localhost/ppm/index.html, it produces
 	 *		http://localhost/config.localhost.json
 	 */
 	PersonalProfilesManager.prototype.ConfigUrl = function()
 	{
		var configUrl = this.urlloc.protocol + "//" + this.urlloc.host 
						+ this.basepath + "/config." + this.urlloc.hostname + ".json";

		return configUrl;
	}

	PersonalProfilesManager.prototype.PerserUrl = function( perserName)
 	{
		var perserUrl = this.urlloc.protocol + "//" + this.urlloc.host 
						+ this.basepath +  "/persers/" + perserName + ".json";

		return perserUrl;
	}

 	PersonalProfilesManager.prototype.loadConfig = function( callback) 
 	{
 		var configUrl = this.ConfigUrl();
 		if (this.fVerbose) {
 			console.log( " Loading configuration from %s", configUrl);
 		}

 		$.getJSON( configUrl, function( config) {

 			callback( null, config);
 		});
 	}

	function CreateProfileSection( persi) {

		console.log( persi);

		var $profile = $("<div>");
		var $info;

		$info = $("<h1>").text( persi.name.fullname);
		$profile.append($info);
	
		$info = $("<h3>").text(persi.description.meme);
		$info.attr("class", "meme");
		$profile.append($info);
		
		$info = $("<h3>").text("Experience");
		$profile.append($info);

		$info = $("<p>").text(persi.description.experience);
		$profile.append($info);

		var tech = persi.tech;
		$info = $("<h3>").text("Technologies");
		var $techlist = $("<ul>");
		tech.forEach( function( item, i) {
			var $a = $("<a>");
			$a.attr("href", item.href);
			$a.attr("target", "_blank");
			$a.text( item.name);
			var $li = $("<li>").append($a);
			$techlist.append($li);
		});
		$info.append($techlist);
		$profile.append( $info);

		return $profile;
	}

 	PersonalProfilesManager.prototype.showProfile = 
 		function( docSelector, profileLocation)
 	{
 		if (this.fVerbose) {
 			console.log( "Fetch profile from (%s) and render to Element at %s",
 				profileLocation, docSelector)
 		}

 		var $docItem = $(docSelector);
 		// ToDo: put a laoding indicator here ...
 		$docItem.empty();

 		// ToDo: consider using d3 data binding mapping
 		$.getJSON( profileLocation, function( persi) {

 			var $profile = CreateProfileSection( persi);

 			$docItem.append( $profile);
 			$docItem.fadeIn();
 		}, this)
 		.fail(function( jqxhr, textStatus, error ) {
		    var err = textStatus + ", " + error;
		    console.log( "Request Failed: " + err );

		    var $profile = $("<div>").text(" Could not find personal information. Create fresh one!");
		    $docItem.append($profile);
		    $docItem.fadeIn();
		});
 	}

// -------------------------------------------------------------------------
// export the constructor for local and remote usage

 	if ( (typeof module === 'undefined')) {
 		window.PersonalProfilesManager = PersonalProfilesManager;
 	}

 })();

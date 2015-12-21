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

	PersonalProfilesManager.prototype.PerserSiteUrl = function( perserName)
 	{
		var perserUrl = this.urlloc.protocol + "//" + this.urlloc.host 
						+ this.basepath +  "/persers/sites." + perserName + ".json";

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

 	PersonalProfilesManager.prototype.linkToAllUsers = function( selector, config)
 	{
 		// Construct the navigation links for all users
 		var d3selector = d3.select( selector);
 		var basepath = this.basepath;

 		var itemsList = d3selector.selectAll("a")
 						.data(config.persers)
 						.enter();
 		
 		var itemLink = itemsList.append("a")
			.attr( "href", function(d) { 
				return basepath + "/pe/index.html?user=" + d;})
			.attr( "id", function(d) { return d; })
			.attr( "target", "_blank");

 		itemLink.append("span")
			.style("padding-left", "0.5em")
			.text(function(d) { return d; });

		return itemsList;
	}

	PersonalProfilesManager.prototype.linkToAllUsers2 = function( selector, config)
 	{
 		// Construct the navigation links for all users
 		var d3selector = d3.select( selector);
 		var basepath = this.basepath;

		var headerList = d3selector
					.append("div").attr("class", "col-sm-2")
					.append("div")
						.attr("id", "groupsList")
						.attr("class", "dropdown");

		headerList.append("button")
			.attr("class", "btn-sm btn-primary dropdown-toggle")
			.attr("type", "button")
			.attr("aria-hidden", "false")
			.attr("data-toggle", "dropdown")
				.text( function(d) { return "Select Users ..."; })
				.append("span").attr("class", "caret");

		var groupsList = headerList.append("ul")
				.attr("class", "dropdown-menu");

		// for each gorup create the top-level anchor link in the menu
		groupsList.selectAll("li")
				.data( config.persers)
				.enter()
				.append( "li")
				.append("a")
					.attr( "href", function(d) { 
						return basepath + "/pe/index.html?user=" + d;})
					.attr( "id", function(d) { return d; })
					.attr( "target", "_blank");

		// remove unwanted nodes
		groupsList.selectAll("li")
			.data(config.persers)
			.exit()
			.remove();

		return headerList;
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
 		var $docItem = $(docSelector);
 		// ToDo: put a laoding indicator here ...
 		$docItem.empty();

 		// ToDo: consider using d3 data binding mapping
 		$.getJSON( profileLocation, function( persi) {

 			var $profile = CreateProfileSection( persi);

 			$docItem.append( $profile);
 		}, this)
 		.fail(function( jqxhr, textStatus, error ) {
		    var err = textStatus + ", " + error;
		    console.log( "Request Failed: " + err );

		    var $profile = $("<div>").text(" Could not find personal information. Create fresh one!");
		    $docItem.append($profile);
		});
 	}


 	PersonalProfilesManager.prototype.loadProfile = function( selector, perserName) 
 	{
  		if (this.fVerbose) {
 			console.log( " loadProfile() for (%s) and render to Element at %s",
 				perserName, selector)
 		}

		// Personalize as per input user name
		// ToDo: localize configuration management inside PersonalProfilesManager
		var pathToProfile = ppm.PerserUrl( perserName);
		this.showProfile( selector, pathToProfile);
 	}


	/*
		renderGroupItems()
		- create all the group items per group


	 @param{object} d3selector - root selector to which attach the nodes generated
	 @param{groupsJson} groupItem - array with the items for the group

	Ouptut:
		<div style="margin-top: 15px;">
			<a href="http://www.dinamani.com" target="_blank" style="margin-left: 10px;">
				<img width="40px" height="40px" src="http://www.dinamani.com/favicon.ico">
				<span style="padding-left: 20px;">தினமணி
				</span>
			</a>
		</div>

	*/
	function renderGroupItems( group, groupItems) 
	{
		var itemList = group.selectAll("div.groupItem")
						.data( groupItems)
						.enter()
						.append("div")
							.attr("class", "groupItem");

		var itemLink = itemList.append("a")
			.attr( "href", function(d) { return d.url})
			.attr( "id", function(d) { return d.inputId; })
			.attr( "target", "_blank");

		itemLink.append("img")
			.attr("class", "groupItemImage")
			.attr("src", function(d) { return d.url + "/favicon.ico";});

		itemLink.append("span")
			.style("padding-left", "0.5em")
			.text(function(d) { 
					return (d.nativelabel != null)? 
							d.nativelabel: d.label;
				});

		return itemList;
	} 	

	/*
		renderGroups()
		- Dynamically load up the selector with details received

	 @param{object} d3selector - root selector to which attach the nodes generated
	 @param{groupsJson} groupsJson - list of groups with pages in it

		Output:
		  for each item we will get the output as:
		  <div class="groupHeader" id="usmagazines">
		  	USMagazines
		  	... group items .. 
		  </div>
	*/
	function renderGroups( d3selector, pagesJson) {

		// layout in a grid if there are more than 3 columns in the output
		// create the group headers first
		var groups = d3selector
					.selectAll("div.groupHeaders")
					.data( pagesJson.groups)
					.enter()
					.append("div")
						.attr("class", "groupHeader col-sm-4")
						.style("background-color", function(d) {
							return d.bgcolor;})
						.attr("id", function(d) { return d.groupId;});

		groups.append("span").text( function(d) { return d.group;});

		// iterate throgh each item and create per-group list
		groups.each( function(d, i) {
			// first create the containing div for the group items
			var groupItemsContainer = d3.select(this).append("div")
						.attr("id", function(d) { return d.group + d.items.length;});
			renderGroupItems( groupItemsContainer, d.items);
		});

		// remove unwanted nodes
		d3selector.selectAll("div.groupHeaders")
			.data(pagesJson.groups)
			.exit()
			.remove();

		return groups;
	}


 	PersonalProfilesManager.prototype.ProcessSiteInfo = function( docSelector, perserName)
 	{
 		var perserSiteUrl = this.PerserSiteUrl( perserName);

   		if (this.fVerbose) {
 			console.log( " ProcessSiteInfo() for Perser(%s) from [%s] and render to Element at %s",
 				perserName, perserSiteUrl, docSelector);
 		}

 		$.getJSON( perserSiteUrl, function( siteInfo) {

	 		var d3DocSelector = d3.select( docSelector);

	    	// input is an array of objects { header, groups} ... render them
	 		siteInfo.forEach( function( group, i) {
	 			renderGroups( d3DocSelector, group);
	 		});
		 })
 		.fail( function (err) {
	 		console.log( "ERROR: Unable to load site info. Error:%s", err);
 		});

 		return;
	}


// -------------------------------------------------------------------------
// export the constructor for local and remote usage

 	if ( (typeof module === 'undefined')) {
 		window.PersonalProfilesManager = PersonalProfilesManager;
 	}

 })();

/*
 *  linksManager.js
 *     Module to manage links of interest
 *
 */

 (function() {

 	'use strict';

 	/*
 	 *	Set up the LinksManager Object
 	 *
 	 *  @param{Array} formInputList - array of items for form
 	 *  @param{bool} verbose - verbosity level to show values
 	 */
 	var LinksManager = function(verbose)
 	{
 		this.self = this;
 		this.fVerbose = verbose;
 		this.allLinks = [];

 		if (this.fVerbose) {
 			console.log( "Created a new Links Manager with %d form items", 
 				this.allLinks.length);
 		}
 	}

 	LinksManager.prototype.links = function()
 	{
 		return this.allLinks;
 	}

 	LinksManager.prototype.print = function()
 	{
 		console.log( " Number of Links: %d", this.allLinks.length);
 		this.allLinks.forEach( function( link, i) {
			console.log( "[%d at %s] Label: %s; URL: %s; Group:Subgroup: [%s:%s].",
				i, Date(link.createdAt), link.label, link.url, 
				link.group, link.subgroup
				);
 		});

 		console.log("---------------------");
 		console.log(this.allLinks);
 	}

 	LinksManager.prototype.add = function( newLink)
 	{
 		// ToDo: check and add to avoid duplicates
 		this.allLinks.push( newLink);

 		// ToDo: save it to the backing store
 	}

 	LinksManager.prototype.organizeByGroups = function() 
 	{
 		// first group the all links by the group and subgroup
 		var groups = [];
 		var groupStructure = [];
 		this.allLinks.forEach( function(link) { 

 			var groupParent = null;
 			var groupIndex = groups.indexOf( link.group);

 			if ( groupIndex === -1) {
 				groups.push( link.group);
	 			groupParent = { header: link.group, groups: []};
	 			groupStructure.push( groupParent);
 			} else {
 				groupParent = groupStructure[groupIndex];
 			}

 			// ToDo: handle subgroups; for now use just a single sub-group
 			var subGroupItem = null;
 			for( var i = 0; i < groupParent.groups.length; i++) {
 				if (groupParent.groups[i].group == link.subgroup) {
 					subGroupItem = groupParent.groups[i];
 					break;
 				}
 			}

 			if (null == subGroupItem) {
 				// add a new subgroup Item
 				subGroupItem = { group: link.subgroup, groupId: Date.now()*10+groupParent.groups.length, items:[]};
 				groupParent.groups.push( subGroupItem);
 			}

 			// Now add the link to the specific subGroup Item
 			subGroupItem.items.push( link);
 		});

 		return groupStructure;
 	}


 	if ( (typeof module === 'undefined')) {
 		window.LinksManager = LinksManager;
 	}

 })();

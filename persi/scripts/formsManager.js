/*
 *  formsManagaer.js
 *     Module to manage Forms for website
 *
 */

 (function() {

 	'use strict';

 	/*
 	 *	Set up the FormsManager Object
 	 *
 	 *  @param{Array} formInputList - array of items for form
 	 *  @param{bool} verbose - verbosity level to show values
 	 */
 	var FormsManager = function( formInputList, processForm, verbose)
 	{
 		this.self = this;
 		this.fVerbose = verbose;
 		this.formInputList = formInputList;
 		this.processForm = processForm;

 		if (this.fVerbose) {
 			console.log( "Created a new forms Manager with %d form items", 
 				this.formInputList.length);
 		}
 	}

 	/*
 	 *	Set up form input fields
 	 *
 	 *  @param{string} formParent - parent selector name where the form is attached to
 	 *
 	 * For each input element repeat this structure.
 	 * Input: { label, id, size, type}
 	 * Ouput:
			<div class='form-label col-sm-1 col-lg-1'> URL:</div> 
			<input type='text' size='120' class='textInput'
				name='urlInput' id='urlInput'></input>
			<br/>

	 And at the end add a button
		<button class="button">Add</button>

 	 *  @return none
 	 */
	FormsManager.prototype.setupForm = function( formParentSelector) 
	{		
 		// Construct the navigation links for all users
 		var d3formRoot = d3.select( formParentSelector);

		// for each input item, we create a distinct row 		
		var inputsList = d3formRoot.selectAll( "div.row")
					.data( this.formInputList)
					.enter()
					.append("div")
					.attr("class", "row form-input-item")
					.attr("id", 
						function( d, i) { 
							console.log( " Creating form input for [%d] %s",
								i, d.label);
							return "form-input-" + i;
						});

		// within each item, create label and input box
		inputsList.append("div")
			.attr("class", "form-label col-sm-1 col-lg-1")
			.text( function(d, i) { return d.label;})

		inputsList.append("input")
			.attr("class", "form-input col-sm-3 col-lg-3")
			.attr("id", function(d, i) { return d.id;})
			.attr("type", function(d, i) { return d.type;})
			.attr("size", function(d, i) { return d.size;});

		//create line separator between input elements
		// ToDo: do simple line separator between elements
		inputsList.append("br")

		var formsMgr = this;

		// add the submit button at the end
		// ToDo: only add this if the button is missing
		d3formRoot.append("button")
			.attr("class", "form-button")
			.text("Add")
			.on( "click", 
				function() {
					formsMgr.processForm();
				});


		// ToDo: remove unwanted nodes
		return;
	}

 	if ( (typeof module === 'undefined')) {
 		window.FormsManager = FormsManager;
 	}

 })();

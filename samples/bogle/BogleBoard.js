/*
 *  BogleBoard.js
 *    Represent and solve Bogle Board Gome 
 *
 *
 *  Created: muralirk@gmail.com - Dec 8, 2015
 */

 (function() {

	'use strict';
	
	// Dependencies


	/*
		Bogle Board Representation

		2D board is laid out as 1D array for simplicity

		(x, y) => i ... location where the element is present
			i = (x*4) + y;


		for a given (x,y) - the neighbors are at offsets
			-5,  -4, -3
			-1, cur, +1
			+3,  +4, +5 

		we also have to check if these are bound within the 4x4
			if not we will drop those neighbors.
		for ex: (x, y) at (0, 0) will only have 3 neighbors at 
			offsets of +1, +4, +5
	 */
	 var offsetForNeighbors = [-5, -4, -3, -1, +1, +3, +4, +5];

 	/* 
 	 * BogleBoard - Object that represents Bogle Board
 	 *
 	 * @param{bool} verbose - should we show verboselog
	 * 
	 * @return{Object} BogleBoard
 	 */
 	var BogleBoard = function( verbose)
 	{
 		this.fVerbose = verbose;

 		// we will represent the board data as a 4x4 table
 		// the table itself can be maintained as a linear array

 		this.neighborMap = this.buildupNeighbors();
 	}

 	function XY2Index( x, y)
 	{
 		// ToDo: Validate the x and y values. 
 		// For now assume they are within the range (0,3)

 		return ( x*4 + y);
 	}

 	BogleBoard.prototype.Index2XY = function( i)
 	{
 		// ToDo: Validate the index i
 		// For now assume they are within the range (0,15)

 		return { x: Math.floor(i / 4), y: i %4 }
 	}


 	/* 
 	 * getNeighbors - list of indices for valid neighbors
 	 *
 	 * @param{int} cur - flattened 'cur' position 
 	 * @param{int} x - x coordinate 
 	 * @param{int} x - x coordinate 
	 * 
	 * @return{array} array of integer indices that are neighbors
 	 */
 	BogleBoard.prototype.getNeighbors = function( cur, x, y)
 	{
 		var neighbors = [];
 		var cur = XY2Index(x, y)

 		// ToDo: optimize the generation of neighbors

 		if (x > 0) {

 			if (y > 0) { neighbors.push( cur-5); }
 			if (y < 3) { neighbors.push( cur-3); }
 			neighbors.push( cur-4);
 		}

 		if (x < 3) {

 			if (y > 0) { neighbors.push( cur+3); }
 			if (y < 3) { neighbors.push( cur+5); }
 			neighbors.push( cur+4); 			
 		}

 		if (y > 0) { neighbors.push( cur-1);}
 		if (y < 3) { neighbors.push( cur+1);}

 		return neighbors;
 	}

 	var _bogleNeighborMap = null; // will be an array of size 16 for all neighbors

 	/* 
 	 * buildupNeighbors - build the neighbor list for all parts of the board
 	 *   THIS IS AN onetime operation ever
 	 *   Use JavaScript singleston model to optimize the build out.
 	 *   ToDo: thread safety
	 * 
	 * @return{array} array of array of neighbor mapping
 	 */
 	BogleBoard.prototype.buildupNeighbors = function()
 	{
 		if (null == _bogleNeighborMap) {

 			// iterate and build up all neighbors and save it away
 			var allNeighbors = [];

 			for( var x = 0; x < 4; x++ ) {
 				for( var y = 0; y < 4; y++) {
 					var cur = XY2Index( x, y);
 					var ngh = this.getNeighbors( cur, x, y);
 					allNeighbors.push( ngh);
 				}
 			}

 			_bogleNeighborMap = allNeighbors;
 		}

 		return _bogleNeighborMap;
 	}

 	/* 
 	 * printMatchingBoard - prints a text based tables showing the match list word
	 * 
 	 * @param{String} content - content for entire bogle board
 	 * @param{array} matchList - list of indices to turn on in the board
	 *
	 * @return{array} array of array of neighbor mapping
 	 */
 	BogleBoard.prototype.printMatchingBoard = function( content, matchList) 
	{
		// initialize an empty board
		var board = [];
		for(var x = 0; x < 4; x++) {
			var boardX = [ '-', '-', '-', '-'];
			board[x] = boardX;
		}

		// set the matching letters in the form n:char
		matchList.forEach( function( matchIndex, i) {
			var xy = bb.Index2XY( matchIndex);
			board[xy.x][xy.y] = (i+1).toString() + ': ' + content[matchIndex];
		});

		// print the full board out
		for(var x = 0; x < 4; x++) {
			console.log( board[x].join('\t'));
		}
	}

  	/* 
 	 * IsIndexInPrefix - check to see if this specified index is already in the prefix array
	 *
	 * @return{bool} true if it is present; else false
 	 */
	function IsIndexInPrefix( prefixList, index)
 	{
 		// ToDo: Optimize for faster scans in the future
 		for(var i = 0; i < prefixList.length; i++) {
 			if (prefixList[i] == index) { return true;}
 		}

 		return false;
 	}


  	/* 
 	 * IsWordPresentAtIndex - check to see if the word is present from the index
 	 *    - recursive function that does bulk of the work of matching
	 *
 	 * @param{String} bogleContent - content for entire bogle board
	 * @param{int} index - current index from which to explore further (use depth first search)
  	 * @param{array} prefixList - list of indices so far where match was found
  	 * @param{String} word - remaining part of the word to be found
	 *
	 * @return{array} matched list if there was full match. Else return null.
 	 */
 	BogleBoard.prototype.IsWordPresentAtIndex = function( bogleContent, index, prefixList, word)
 	{
 		if ( 0 == word.length) {

 			if (this.fVerbose) { console.log( "\tFull word is exhausted. That means we found a match.");}
 			return prefixList; // this is the full path for the word!
 		}

 		// let us find all neighbors and start checking for where the first char is present
 		var neighbors = this.neighborMap[index];
 		for( var i = 0; i < neighbors.length; i++) {

 			// do not reuse a tile if already used
 			if (IsIndexInPrefix( prefixList, neighbors[i])) {
	 			if (this.fVerbose) { console.log( "\tTile at [%d] already used. Skip and check others.", neighbors[i]);}
	 			continue;
 			}

 			// if the first character of remaining word matches, start deeper exploration.
 			if ( bogleContent[neighbors[i]] == word[0]) {
 				prefixList.push( neighbors[i]); // add this position
 				var matchFound = this.IsWordPresentAtIndex( bogleContent, neighbors[i], prefixList, word.slice(1));
	 			if (null != matchFound) {
	 				return matchFound;
	 			}
				prefixList.pop( neighbors[i]); // pop this item for handling other neighbors 				
 			}
 		}

		if (this.fVerbose) { console.log( "\tPartial match found till %d positions.", prefixList.length);}
 		return null;
 	}


  	/* 
 	 * FindStartingIndices - find all indices where the character is found
	 *
 	 * @param{String} bogleContent - content for entire bogle board
	 * @param{char} char1 - first character to be matched for
	 *
	 * @return{array} matched list of indices where the character is found. Else return null.
 	 */
 	BogleBoard.prototype.FindStartingIndices = function( bogleContent, char1) 
 	{
 		var startIndices = [];

 		for( var i = 0; i < bogleContent.length; i++)
 		{
 			if (char1 == bogleContent[i]) {
 				startIndices.push(i);
 			}
 		}

 		return (startIndices.length > 0) ? startIndices : null;
 	}


  	/* 
 	 * IsWordPresent - check to see if the word is present in bogle content
	 *
 	 * @param{String} bogleContent - content for entire bogle board
  	 * @param{String} word - remaining part of the word to be found
	 *
	 * @return{array} matched list if there was full match. Else return null.
 	 */
 	BogleBoard.prototype.IsWordPresent = function( bogleContent, word)
 	{
 		if ( (null == word) || (16 < word.length)) {
 			if (this.fVerbose) { console.log( "\tERROR: Invalid Length. No Match found.");}
 			return null;
 		}

 		var startIndices = this.FindStartingIndices( bogleContent, word[0]);

 		if ( null == startIndices) {
  			if (this.fVerbose) { console.log( "\tNo match found for starting character. No Match found.");}
  			return null;
 		}

 		for( var i = 0; i < startIndices.length; i++ ) {

  			if (this.fVerbose) { console.log( "\tChecking from position [%d]", startIndices[i]); }
 			var matchList = [ startIndices[i]];
 			var matchFound = this.IsWordPresentAtIndex( bogleContent, startIndices[i], matchList, word.slice(1));

 			if (null != matchFound) {
 				return matchFound;
 			}
 		}

		if (this.fVerbose) { console.log( "\tNo full word match found. No Match found.");}
 		return null;
 	}

	// ----------------------------------------------------------------
	// Module Interface for external use
    if ((typeof module) === 'undefined') {
        window.BogleBoard =  BogleBoard;
    } else if ((typeof module === 'object') && module.exports) {
		module.exports = BogleBoard;
	}
})();


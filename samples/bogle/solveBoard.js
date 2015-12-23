/*
 *	solveBoard.js - Get bogle board
 *
 *  Created: muralirk@gmail.com - Dec 8, 2015
 */

// First load up the BogleBoard object
var BogleBoard = require('./BogleBoard');


var bb = new BogleBoard( false);

console.log("\n\n ------------------------------------");
console.log(" [TRACE DEBUG] See neighbor list for each position of the board");
var allN = bb.buildupNeighbors();
allN.forEach( function( n, i) {
	console.log( "Neighbors[%d] = [%s]", i, n);
});


// --- HELPER FUNCTIONS
function printMatchingBogleBoard( content, matchList) 
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


function checkForWord( content, word, matchable) 
{
	console.log( "\n-------------------------------------------------------------");
	console.log( " Check for word: '%s' in {{%s}}", word, content);
	var matchList = bb.IsWordPresent( content, word);
	if (matchList) {
		console.log("  ++++ WORD FOUND. Indices: [%s]", matchList);
		printMatchingBogleBoard( content, matchList)
	} else {
		console.log("  ------ NO MATCH FOUND");
	}

	if ( matchable ^ (matchList != null)) {
		console.log( "  ****** MISMATCH in expecation vs. result")
	}

}

// --- RUN THE FULL TESTS

var content1 = "abcdefghijklmnop";

console.log("\n\n ###########################################################################");
checkForWord( content1, null, false);
checkForWord( content1, 'a', true);
checkForWord( content1, 'f', true);
checkForWord( content1, 'p', true);
checkForWord( content1, 'abcdefghijklmnopqrstuvwxyz', false);
checkForWord( content1, 'abc', true);
checkForWord( content1, 'abf', true);
checkForWord( content1, 'abp', false);
checkForWord( content1, 'aba', false);


var content2 = "RILESMSXAYAZRTQE";
console.log("\n\n ###########################################################################");
checkForWord( content2, null, false);
checkForWord( content2, 'SMILE', true);
checkForWord( content2, 'MILES', true);
checkForWord( content2, 'MAZE', true);
checkForWord( content2, 'TARR', false);
checkForWord( content2, 'RAMA', true);

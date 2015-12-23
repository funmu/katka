/*
 *	solvePoker.js - solve for poker hand
 *
 *  Created: muralirk@gmail.com - Dec 22, 2015
 */

// First load up the BogleBoard object
var PokerChecker = require('./pokerChecks');


var pc = new PokerChecker( false);

var cardSet1 = [
	{ rank: '2', suit: 'C'},
	{ rank: '2', suit: 'D'},
	{ rank: '3', suit: 'C'},
	{ rank: '4', suit: 'C'},
	{ rank: '5', suit: 'C'}
];

var cardSet2 = [
	{ rank: '3', suit: 'C'},
	{ rank: '3', suit: 'D'},
	{ rank: '2', suit: 'S'},
	{ rank: '2', suit: 'C'},
	{ rank: '5', suit: 'C'}
];

var cardSet3 = [
	{ rank: '3', suit: 'C'},
	{ rank: '3', suit: 'D'},
	{ rank: '3', suit: 'S'},
	{ rank: '2', suit: 'D'},
	{ rank: '1', suit: 'H'}
];

var cardSet4 = [
	{ rank: '3', suit: 'C'},
	{ rank: '3', suit: 'D'},
	{ rank: '3', suit: 'S'},
	{ rank: '3', suit: 'H'},
	{ rank: '2', suit: 'H'}
];

var cardSet5 = [
	{ rank: '3', suit: 'C'},
	{ rank: '4', suit: 'D'},
	{ rank: '5', suit: 'S'},
	{ rank: '6', suit: 'H'},
	{ rank: '7', suit: 'H'}
];

var cardSet6 = [
	{ rank: '10', suit: 'C'},
	{ rank: 'J', suit: 'D'},
	{ rank: 'Q', suit: 'S'},
	{ rank: 'K', suit: 'H'},
	{ rank: 'A', suit: 'H'}
];

var cardSet7 = [
	{ rank: '3', suit: 'C'},
	{ rank: '7', suit: 'C'},
	{ rank: '9', suit: 'C'},
	{ rank: 'K', suit: 'C'},
	{ rank: 'A', suit: 'C'}
];

var cardSet8 = [
	{ rank: '3', suit: 'C'},
	{ rank: '3', suit: 'D'},
	{ rank: '8', suit: 'S'},
	{ rank: '8', suit: 'H'},
	{ rank: '8', suit: 'D'}
];

var cardSet9 = [
	{ rank: '3', suit: 'D'},
	{ rank: '4', suit: 'D'},
	{ rank: '5', suit: 'D'},
	{ rank: '6', suit: 'D'},
	{ rank: '7', suit: 'D'}
];

var cardSet10 = [
	{ rank: '10', suit: 'C'},
	{ rank: 'J', suit: 'C'},
	{ rank: 'Q', suit: 'C'},
	{ rank: 'K', suit: 'C'},
	{ rank: 'A', suit: 'C'}
];

var cardSets = [
	{ expectedType: "Pair", set: cardSet1},
	{ expectedType: "TwoPair", set: cardSet2},
	{ expectedType: "ThreeOfAKind", set: cardSet3},
	{ expectedType: "FourOfAKind", set: cardSet4},
	{ expectedType: "Straight", set: cardSet5},
	{ expectedType: "Straight", set: cardSet6},
	{ expectedType: "Flush", set: cardSet7},
	{ expectedType: "FullHouse", set: cardSet8},
	{ expectedType: "StraightFlush", set: cardSet9},
	{ expectedType: "RoyalFlush", set: cardSet10},
	];

cardSets.forEach( function( cardset, i) {

	console.log("\n\n ----- SET %d -------- Expect: %s", 
		i+1, cardset.expectedType);

	var matchesFound = pc.CheckHands( cardset.set);
	console.log("      %d MATCHES FOUND.", 
		matchesFound.length);
	matchesFound.forEach( function( m, i) {

		console.log( " Match[%d]: Type=%s, Score=%d, Suit=%s, Rank=%s, Count=%d",
				i, m.matchType, m.matchScore, m.matchSuit, m.matchRank, m.matchCount);

	});
});

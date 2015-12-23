/*
 *  pokerChecks.js
 *     Module to check hands for poker results
 *
 */

 (function() {

 	'use strict';


 	/*
 	 *	Set up the PokerChecker Object
 	 *
 	 *  @param{bool} verbose - verbosity level to show values
 	 */
 	var PokerChecker = function(verbose)
 	{
 		this.self = this;
 		this.fVerbose = verbose;
 	
 		if (this.fVerbose) {
 			console.log( "Created a new Poker Checker");
 		}
 	}

	var PokerHand = function( cards)
	{
		this.cards = cards;

		// model 'A' as both 1 and 14
		// array ranges from 0..14
		// rankVal of 0 at index 0 is invalid
		this.rankCounts=[];
		var b=15; while(b--) { this.rankCounts[b]=0 };

		// map suits to an associative array
		this.suitCounts = [
			{ suit: 'C', count: 0},
			{ suit: 'D', count: 0},
			{ suit: 'H', count: 0},
			{ suit: 'S', count: 0}
		];
	}

 	PokerChecker.prototype.printHand = function(cards) 
 	{	
 		console.log( " -----------------\n Cards in Hand. #: %d", 
 			cards.length);

 		cards.forEach( function( d, i) {

 			console.log( "  [%d] suite: %s; rank: %s",
 				i, d.suit, d.rank);
 		});
 	}


 	PokerHand.prototype.print = function()
 	{	
		console.log("\n-------- RANK COUNTS ----------");
		this.rankCounts.forEach( function( rc, i) {
			console.log( " [%d] count = %d", i, rc);
		});

		console.log("\n-------- SUIT COUNTS ----------");
		this.suitCounts.forEach( function( sc, i) {
			console.log( " [%d] suit=%s; count = %d", i, sc.suit, sc.count);
		});
	}

	PokerHand.prototype.Prepare = function() 
	{	
		// ToDo: Check if the cards are valid 

		// get the rank of the cards
		var ranks = this.cards.map( function(c) { 
				var r = c.rank;
				var rankVal = 0;
				switch (r) {
					case 'A': rankVal = 1; break;
					case 'J': rankVal = 11; break;
					case 'Q': rankVal = 12; break;
					case 'K': rankVal = 13; break;
					default:
						var rnum = parseInt( r);
						if ((rnum >= 2) && (rnum <= 10)) {
							rankVal = rnum;
						}
						break;
				}

				return rankVal;
			});

		// count # cards per rank

		// for each rank ... find how many time it occurs
		var self = this;
		ranks.forEach( function(r) {

			self.rankCounts[r]++; 			
			if (r == 1) {
				// set an additional entry for 'A' at r=14
				self.rankCounts[14]++;
			}
		});

		// update the per suite count
		self.cards.forEach( function (c, i) {

			for( var i = 0; i < self.suitCounts.length; i++) {
				if (self.suitCounts[i].suit == c.suit) {
					self.suitCounts[i].count++;
					break;
				}
			}
		});

		return;
	}

	function RankForIndex(i) 
	{
		var indexToRank = [
			'0', 'A', '2', '3', '4', '5', 
			'6', '7', '8', '9', '10', 
			'J', 'Q', 'K', 'A'
			];

		if ( (i >= 0) && (i <= 14)) {
			return indexToRank[i];
		}

		return 'unknown';
	}


	// each of the function here has the signature of type
	//		function( priorMatches, pokerHand) 
	//		- priorMatches allows us to compute optimized answers for select matches
	//
	var possibleMatchTypes = [

			{ name: "Pair", score: 1, fn: FindPairMatches },
			{ name: "TwoPair", score: 2, fn: FindTwoPairMatches },
			{ name: "ThreeOfAKind", score: 3, fn: FindThreeOfAKindMatches },						
			{ name: "FourOfAKind", score: 7, fn: FindFourOfAKindMatches },
			{ name: "Straight", score: 4, fn: FindStraightMatches },
			{ name: "Flush", score: 5, fn: FindFlushMatches },
			{ name: "FullHouse", score: 6, fn: FindFullHouseMatches },
			{ name: "StraightFlush", score: 8, fn: FindStraightFlushMatches },
			{ name: "RoyalFlush", score: 9, fn: FindRoyalFlushMatches }
		];

	function FindPerKindMatches( cards, rankCounts, numToMatch)
	{
		var matches = [];

		for( var i = 1; i < 14; i++) {

			if (rankCounts[i] == numToMatch) {

				var match = { 
					matchRank: RankForIndex(i), 
					matchCount: rankCounts[i]
				};
				matches.push(match);
			}
		}

		return matches;
	}

	function FindPairMatches( priorMatches, pokerHand) 
	{
		return FindPerKindMatches( pokerHand.cards, pokerHand.rankCounts, 2);
	}

	function FindTwoPairMatches( priorMatches, pokerHand)
	{
		// ToDo: optimize to reuse the matches found in Pair Matches
		var matches = FindPerKindMatches( pokerHand.cards, pokerHand.rankCounts, 2);
		return (matches.length >= 2) ? matches : null;
	}

	function FindThreeOfAKindMatches( priorMatches, pokerHand)
	{
		return FindPerKindMatches( pokerHand.cards, pokerHand.rankCounts, 3);
	}

	function cloneMatches( matches) 
	{
		var clonedMatches = [];

		if (matches!= null) {
			matches.forEach( function(m, i) {
				var newMatch = {
					matchSuit: m.matchSuit,
					matchRank: m.matchRank,
					matchCount: m.matchCount
				};

				clonedMatches.push( newMatch);
			});
		}

		return clonedMatches;
	}

	function FindFullHouseMatches( priorMatches, pokerHand)
	{
		if (priorMatches.length < 2) {
			return null;
		}

		var match2 = null;
		var match3 = null;

		for( var i = 0; i < priorMatches.length; i++ ) {

			switch (priorMatches[i].matchType) {
				case "ThreeOfAKind":
					match3 = priorMatches[i];
					break;

				case "Pair":
					match2 = priorMatches[i];
					break;
			}
		}

		if ( (null != match2) && (null != match3)) {
			// there will only be 1 of each .. since there are only 5 cards
			var matches = [match2, match3];
			return cloneMatches( matches); // clone so we have fresh copy
		} 

		return null;
	}

	function FindFourOfAKindMatches( priorMatches, pokerHand)
	{
		return FindPerKindMatches( pokerHand.cards, pokerHand.rankCounts, 4);
	}

	function FindStraightMatches( priorMatches, pokerHand)
	{
		// there can only be a single match possible for straight
		var matches = [];

		for( var i = 1; i <= 10; i++) {

			if (pokerHand.rankCounts[i] == 1) {

				// this is the first index where we found a single card
				// all subsequent cards should be present for a Straight

				// special case for 'A' at start
				if ( pokerHand.rankCounts[i+1] != 1) continue;
				
				var isSequential = true;
				for( var j = i+1; isSequential && (j <= i+4); j++) {
					isSequential = (pokerHand.rankCounts[j] == 1);
				}

				if (isSequential) {
					var match = { 
						matchRank: RankForIndex(i), // starting rank
						matchCount: pokerHand.rankCounts[i]
					};
					matches.push(match);
					break;
				} else {
					// there is a break somewhere .. no straight possible
					break;
				}
			}
		}

		return matches;
	}

	function FindFlushMatches( priorMatches, pokerHand)
	{
		var matches = [];

		// iterate through suit counts and see if any suit has 5 cards in it
		pokerHand.suitCounts.forEach( function( sc, i) {
			if (sc.count == 5) {

				var match = {
					matchSuit: sc.suit,
					matchCount: sc.count
				}
				matches.push(match);
			}
			// ToDo: optimize to stop scanning once we found a match
		});

		return matches;
	}

	function FindStraightFlushMatches( priorMatches, pokerHand)
	{
		// has precisely just Straight and Flush match in it

		if (priorMatches.length != 2) {
			return null;
		}

		var matchStraight = null;
		var matchFlush = null;


		for( var i = 0; i < priorMatches.length; i++ ) {

			switch (priorMatches[i].matchType) {
				case "Straight":
					matchStraight = priorMatches[i];
					break;

				case "Flush":
					matchFlush = priorMatches[i];
					break;
			}
		}

		if ( (matchFlush != null) && (matchStraight != null)) {

			var matches = cloneMatches( [matchStraight]);
			matches[0].matchSuit = matchFlush.matchSuit;

			return matches;
		} 

		return null;
	}


	function FindRoyalFlushMatches( priorMatches, pokerHand)
	{
		// has precisely three items: Straight, flush, and StraightFlush
		//	if not ignore and return

		if (priorMatches.length != 3) {
			return null;
		}

		var matchSF = null;

		for( var i = 0; i < priorMatches.length; i++ ) {

			switch (priorMatches[i].matchType) {
				case "StraightFlush":
					matchSF = priorMatches[i];
					break;
			}
		}

		if ( matchSF != null)  {

			var matches = cloneMatches( [matchSF]);
			return matches;
		} 

		return null;
	}

 	/*
	 *  Check the hand of cards and return all possible pokerhands
	 *
 	 *  @param{Array} cards - cards in hand

		Poker hand consists if an arry of cards
		card has {suit, rank} attribute
		suit comes from [ 'C', 'D', 'H', 'S'] for various suites
		rank comes from [2..10, J, Q, K, A]

	 *  @return{Array} pokerHands - all possible poker hand matches
 	 */
 	PokerChecker.prototype.CheckHands = function( cards)
 	{
 		var pokerMatches = [];
 		var maxScore = -1;

 		var pokerHand = new PokerHand( cards);
 		pokerHand.Prepare();

 		possibleMatchTypes.forEach( function( pmt, i) {

 			if (this.fVerbose) { 
 				console.log( " [%d] Trying out possible match of type: %s",
 					i, pmt.name);
 			}

 			var matchedHands = pmt.fn( pokerMatches, pokerHand);

 			if (this.fVerbose) { 
 				console.log( " ... found %d matches for type: %s",
 					(matchedHands != null) ? matchedHands.length : 0, pmt.name);
 			}

 			if ( (matchedHands != null) && matchedHands.length > 0) {

 				if (pmt.score > maxScore) {
 					maxScore = pmt.score;
	 				matchedHands.forEach( function(m) {
	 					m.matchScore = pmt.score;
	 					m.matchType = pmt.name;
	 				})
	 				pokerMatches = pokerMatches.concat(matchedHands);
	 			}
 			}
 		}, this);

 		// filter out to only send back the matches with max score
 		var finalMatches = pokerMatches.filter( function( pm, i) { 
 			return ( pm.matchScore == maxScore) ? pm : null; 
 		});
 		return finalMatches;
 	}


 	if ( (typeof module === 'undefined')) {
 		window.PokerChecker = PokerChecker;
 	} else if ((typeof module === 'object') && module.exports) {
		module.exports = PokerChecker;
	}

 })();

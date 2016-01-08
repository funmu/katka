/*
 *	checkBucketFiller.js - Checks the bucket filler based on interactive input
 *
 *  Created: muralirk@gmail.com - Jan 8, 2015
 */

// First load up the BucketFilller
var BucketFiller = require('./BucketFiller');
var bf = new BucketFiller( false);

process.stdin.resume();
process.stdin.setEncoding('utf8');
var util = require('util');
printUsage();

process.stdin.on('data', function (text) {
	switch (text) {

		case "?":
		case "?\n":
		case "help\n":
			printUsage();
			break;

		case "quit":
		case "quit\n":
			done();
			break;

		case "test":
		case "test\n":
			testAll();
			break;

		default:
			// load up the array and test
			var bucketStrings = text.split(',');
			var buckets = bucketStrings.map( function(d) { return parseInt(d);});
			var capacity = bf.findCapacity( buckets);
			console.log( " Capacity for given input is: %d", capacity);
			break;

	}
	console.log("---------------");
});

function printUsage()
{
	console.log( "?|help - help message");
	console.log( "test   - run inbuilt set of tests");
	console.log( "quit   - quit this program");
	console.log( "comma separated numbers - finds capacity for that sequence");
	console.log("---------------");
}

function done() {
	console.log('Thanks for checking out the BucketFiller. See you later.');
	process.exit();
}

function checkHoldingCapacity( buckets, expectedCapacity)
{

	console.log( "\nBucket: %s has %d elements", buckets, buckets.length);
	var capacity = bf.findCapacity( buckets);
	if (capacity == expectedCapacity) {
		console.log(" HURRAY! We found that bucket holds %d units as expected",
			expectedCapacity);
	} else {
		console.log("---ALAS! Expected %d units; Filler says %d units.",
			expectedCapacity, capacity);
	}

}

// --- RUN THE FULL TESTS

// testAll();

function testNullGroup() 
{

	console.log("\n\n #####  NULL GROUP");
	checkHoldingCapacity( [], 0);
	checkHoldingCapacity( [1, 1, 1], 0);
	checkHoldingCapacity( [1, 2, 3], 0);
	checkHoldingCapacity( [3, 2, 1], 0);
}

function testSimpleGroup()
{
	console.log("\n\n #####  Simple GROUP");
	checkHoldingCapacity( [ 2, 1, 2], 1);
	checkHoldingCapacity( [ 3, 2, 2, 3], 2);
	checkHoldingCapacity( [ 3, 1, 1, 3], 4);
	checkHoldingCapacity( [ 3, 1, 2, 3], 3);
	checkHoldingCapacity( [ 3, 2, 1, 3], 3);
}

function testComplexGroup1()
{
	console.log("\n\n #####  Complex GROUP 1");
	checkHoldingCapacity( [ 2, 1, 2, 1, 2, 1, 2], 3);
	checkHoldingCapacity( [ 5, 2, 1, 2, 3, 6], 12);
	checkHoldingCapacity( [ 5, 2, 1, 2, 3, 6, 3, 4, 2, 5], 18);
}

function testComplexGroup2()
{
	console.log("\n\n #####  Complex GROUP 2");
	checkHoldingCapacity( [ 5, 3, 4, 2, 3, 1, 2], 3);
	checkHoldingCapacity( [ 5, 2, 1, 2, 3, 3], 4);
	checkHoldingCapacity( [ 5, 2, 1, 2, 3, 3, 6], 14);

}

function testAll()
{
	testNullGroup();
	testSimpleGroup();
	testComplexGroup1();
	testComplexGroup2();
}



 
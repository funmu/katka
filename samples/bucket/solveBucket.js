/*
 *	solveBucket.js - Solve for units of storage in buckets
 *
 *  Created: muralirk@gmail.com - Jan 8, 2015
 */

// First load up the BucketFilller
var BucketFiller = require('./BucketFiller');


var bf = new BucketFiller( false);

console.log("\n\n ------------------------------------");

function checkHoldingCapacity( buckets, expectedCapacity)
{

	console.log( "\nBucket: %s", buckets);
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

testAll();

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



 
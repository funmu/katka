/*
 *  BucketFiller.js
 *    Handle variable length array of buckets and estimate capacity 
 *
 *
 *  Created: muralirk@gmail.com - Jan 8, 2015
 */

 (function() {

	'use strict';
	
	// Dependencies


 	/* 
 	 * BucketFiller - Object that represents Filler Capcacity Estimations
 	 *
 	 * @param{bool} verbose - should we show verbose log
	 * 
	 * @return{Object} BucketFiller
 	 */
 	var BucketFiller = function( verbose)
 	{
 		this.fVerbose = verbose;

 	}


 	/* 
 	 *  findCapacity - estimate the capacity of units in the bucket
	 * 
	 * @param{array} array of integers representing height of bars for bucket
	 *
	 * @return{int} number of units of capacity
 	 */
 	BucketFiller.prototype.findCapacity = function( buckets)
 	{
 		if ( null == buckets) {
 			return 0;
 		}

 		return this.findCapacityInRange( buckets, 0, buckets.length);
 	}


 	BucketFiller.prototype.calcCapacity = function( buckets, adjustedStart, adjustedEnd, maxCapacityHeight)
 	{
 		var capacity = 0;

		for( var k = adjustedStart+1; k < adjustedEnd; k++) {
			if ( buckets[k] > maxCapacityHeight) {
				console.log( "\toops! ERROR = there should NOT be another local maxima in this range [%d] has value %d higher than maxCapacityHeight of %d",
						k, buckets[k], maxCapacityHeight);
			} else {
				capacity += ( maxCapacityHeight - buckets[k]);
			}
		}

 		if (this.fVerbose) {
 			console.log( "\t Calculate capacity in range [%d, %d] => capacity of %d units",
 				adjustedStart, adjustedEnd, capacity);
 		}

 		return capacity;
 	};


 	BucketFiller.prototype.findCapacityInRange = function( buckets, start, end)
 	{
 		if (this.fVerbose) {
 			console.log( "\tFinding capacity in range [%d, %d]", start, end);
 		}

 		if ( end <= start) {
 			// no water can be held in this situation
 			return 0;
 		}

 		// 1a. Normalize - trim ascending only sequence of bar heights
 		var adjustedStart = start;
 		while ( (adjustedStart < end-1) && 
 				(buckets[adjustedStart] <= buckets[adjustedStart+1]))
 		{
 			adjustedStart++;
 		}

 		// 1a. Normalize - trim descending only sequence of bar heights
 		var adjustedEnd = --end;
 		while ( (adjustedEnd > adjustedStart) && 
 				(buckets[adjustedEnd] <= buckets[adjustedEnd-1]))
 		{
 			adjustedEnd--;
 		}

 		if ( adjustedEnd <= adjustedStart) {

 			// no water can be held since there are no bucekt left
 			return 0;
 		}

 		if ( this.fVerbose) {
 			console.log( "\tAdjusted Range: [%d, %d]",
 				adjustedStart, adjustedEnd);
 		}

 		// 2. Check for any local maxima within range
		var maxCapacityHeight = (buckets[adjustedStart] < buckets[adjustedEnd]) 
								? buckets[adjustedStart] : buckets[adjustedEnd];


		// scan to find if there are other local maxima within this reange
		var localMaxima = maxCapacityHeight;
		var localMaximaIndex = -1;
		for( var k = adjustedStart+1; k < adjustedEnd-1; k++) {
			if ( buckets[k] > localMaxima) {
				localMaxima = buckets[k];
				localMaximaIndex = k;
			}
		}

 		if ( this.fVerbose) {
 			console.log( "\t Local Maxima is %d at [%d]",
 				localMaxima, localMaximaIndex);
 		}

 		// 3. Do the capacity estimation
		var capacity = 0;
		if ( localMaximaIndex == -1) {
			// we did not find any local maxima => calc capacity locally
			capacity = this.calcCapacity( buckets, adjustedStart, adjustedEnd, maxCapacityHeight);
		} else {
			// divide and conquer the range
			// Note: use +1 for the ending indices since that is waht findCapacityInRange expects
			capacity  =
					this.findCapacityInRange( buckets, adjustedStart, localMaximaIndex+1) +
					this.findCapacityInRange( buckets, localMaximaIndex, adjustedEnd+1);
		}

		return capacity;
 	}

	// ----------------------------------------------------------------
	// Module Interface for external use
    if ((typeof module) === 'undefined') {
        window.BogleBoard =  BucketFiller;
    } else if ((typeof module === 'object') && module.exports) {
		module.exports = BucketFiller;
	}
})();


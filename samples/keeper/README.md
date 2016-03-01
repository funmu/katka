# Solve Bucket Capacity

Imagine we are given a sequence of positive integers representing the height of bars. Imagine that water is dumped from the top. Determine the number of units fo water held inside the bars.



##Solution Approach##
Take the input sequence as an array of numbers bounded by index (i, j) 
 1. Normalize the array to find the area to process deeply. 
   1a. Remove leading sequence of ascending numbers (water drains off)
   1b. Remove trailing sequence of descending numbers (water drainsoff)
 2. Check for local maxima within this adjusted range after trimming
   Assume element at "m" is the local maxima. Scan to find element at "k" which is the next local maxima (after which values are equal are smaller). Worst case I may have to scan the entire array at O(N) and sometimes we may do repeat scans of there are sequence of local maximas.
 3. Calculate holding capacity within the adjusted range.
  If no local maxima, do a simple capacity calculation. If there is a local maxima, divide and conquer around the local maxima.

##Code##
 * [Bucket Filler Module](BucketFiller.js)
 * [Check Bucket Filler](checkBucketFiller.js)

The code has some in-line documentation.


## Examples
 * All examples below will result in no water is held
 >  []
 >
 >  [ 1, 1, 1]
 >
 >  [ 1, 2, 3]
 > 
 >  [ 3, 2, 1]
 >

* For the below sequence limited water is held
 >  [ 2, 1, 2]  => 1 unit of water held
 >
 >  [ 3, 2, 2, 3] => 2 units of water held
 >
 >  [ 3, 1, 1, 3] => 4 units of water held
 > 
 >  [ 3, 1, 2, 3] => 3 units of water held
 >
 >  [ 3, 2, 1, 3] => 3 units of water held
 >

* For the below sequence are complex holding variable amounts of water
 >  [ 2, 1, 2, 1, 2, 1, 2]  => 3 unit of water held
 >
 >  [ 5, 2, 1, 2, 3, 6] => 12 units of water held
 >
 >  [ 5, 2, 1, 2, 3, 6, 3, 4, 2, 5] => 18 units of water held
 >
 >  [ 5, 3, 4, 2, 3, 1, 2] => 3 units of water held
 >
 >  [ 5, 2, 1, 2, 3, 3] => 4 units of water held
 >
 >  [ 5, 2, 1, 2, 3, 3, 6] => 14 units of water held
 >
  
###Testing Code###
 Use *node.js* to run these JavaScript modules, after having the two files in the same directory.

> *node checkBucketFiller.js* 

The above command will run thru the simple set of tests used for checking out the *Bucket Filler*. For matching words, the board is printed out with sequential indices to show the flow of the word in the board.

###Wish List###
 * Optimizations 
  * Reduce scanning time in step #3

##Contributors##
Murali Krishnan


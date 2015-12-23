# Solve Bogle Board

*Bogle board* is a square of size 4 tiles by 4 tiles in rows and columns. Each tile contains a letter from the alphabet. The same letter may be repeated multiple times. Given a Bogle board, we are interested in finding if any particular word is found. To find word match, one can start from the first character and look for matches in each of the eight sides from that tile. Wraps are not supported around the edges of the square.

##Solution Approach##
Bogle board is of a fixed size. The easiest representation is to use an array of size 16 (= 4x4) to represent the board indices. The content of the bogle board itself can be maintained as an array of characters (aka _string_). This makes it easy to generate the matches for a given word as an array of indices that match for the word.

To ease the generation of the matches, we need to do quick neighbor lookup. The good news is that we can compute the neighbors for each of the tile independent of the content. This one-time computation is cheaper and well amortized for repeat searches. So there will be an array of size 16 (again = 4 x 4) that contains the list of valid neighbors (without the tiles from the wrapping).

One wrinkle in this search is that each tile can only be used once. And that is handled by doing a check each time to see if the tile is already used. If it is used we will discard it.

##Code##
 * [Bogle Board Module](BogleBoard.js)
 * [Solve Board Test Code](solveBoard.js)

The code has more in-line documentation.

###Testing Code###
 Use *node.js* to run these JavaScript modules, after having the two files in the same directory.

> *node solveBoard.js* 

The above command will run thru the simple set of tests used for checking out the *Bogle Board*. For matching words, the board is printed out with sequential indices to show the flow of the word in the board.

###Wish List###
 * Optimizations 
  * Use 16-bit number for storing prefixList so we can avoid linear search
  * Use iteartion with a queue instead of recursion (if processor cycles are important)
  * Use letter scan early on to check if all letters exist independent of position
 * Experience
  * Enable a graphical mode to show the matches
  * An app to illustrate the use of the Bogle Board matches
  * Generalize BogleBoar for nxn sized grids (instead of just 4x4)
  * Genaralize to support other langauges

##Contributors##
Murali Krishnan


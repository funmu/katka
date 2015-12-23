# Solve Poker Hand

*Poker* is a card game that deals with the occurence pattern of cards. The sample module here attempts to decipher the highest possible poker hand match possible.

##Solution Approach##
The module quickly parses the cards provided to count number of cards by rank and suit. It uses the same to run thru the different possible matches using dedicated functions. It reuses prior matches to reduce checks if possible. Finally it prunes the matches to find hte highest possible match for a given card set.

##Code##
 * [PokerChecks Module](pokerChecks.js)
 * [Solve Poker Hand Test Code](solvePoker.js)

The code has more in-line documentation.

###Testing Code###
 Use *node.js* to run these JavaScript modules, after having the two files in the same directory.

> *node solvePoker.js* 

The above command will run thru the simple set of tests used for checking out the *Poker Card Sets*. 

###Wish List###
 * Optimizations 
  * Measure and optimize memory footprint
 * Experience
  * Better documentation 
  * Enable a graphical mode to show the matches

##Contributors##
Murali Krishnan


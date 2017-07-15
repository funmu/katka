#!/usr/bin/python

"""

 PuzzleGenerator.py
    Class for generating word puzzles with
       Word Search &
       Crosswords

    Created Date: Apr 23, 2017

    Dependencies
    -  DropBox SDK installed using
        pip install dropbox
"""
__author__ = 'Murali Krishnan'
__version__ = "v1.0.0"


# coding: utf-8


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Import Section

import csv;
import json;
import random;
from PyDictionary import PyDictionary;
from crossword import Crossword;

dictionary = PyDictionary();

from stemming.porter2 import stem;

def stemall( words):
    return set([ stem(word) for word in words]);

# ------------------------------------------------------------------------
class _WordHelpers(object):
    """
        Class used for processing and fetching meaning for words
    """

    fVerbose = 0;

    def __init__(self, fVerbose=0):
        self.fVerbose = fVerbose;

    def GetInfoOnWord( self, wd):
        if (self.fVerbose):
            print "\nprocesing word .... ", wd;
        mng = dictionary.meaning(wd);
        syn = dictionary.synonym(wd);
        ant = dictionary.antonym(wd);
        wordInfo = { "word" : wd, "partOfSpeech": "Unknown", "meaning": ""};
        if (mng != None):
            mngList = mng.items();
            if (mngList != None):
                (k, v) = mng.items()[0];
                wordInfo["partOfSpeech"] = k;
                wordInfo["meaning"] = v;
        wordInfo["synonym"] = syn;
        wordInfo["antonym"] = ant;
        return wordInfo;

    def Test_GetInfoOnWord( self):
        word = 'interconnection';
        print self.GetInfoOnWord(word);
        word2 = "dance";
        print GetInfoOnWord(word2);

# ------------------------------------------------------------------------
class WordWithMeanings(object):
    """
        Class used for keeping track of words with meanings
    """

    fVerbose = 0;
    wordHelpers = None;

    def __init__(self, fVerbose=0):
        self.fVerbose = fVerbose;
        self.wordHelpers = _WordHelpers( fVerbose);

    def LoadInputWords( self, fileName, fVerbose = 0):
        """
            Load input words from a given file
            and returns the words back
        """
        lines = None;
        with open( fileName, "r") as text_file:
            lines = text_file.readlines();
            text_file.close();

        # read in the input words
        if ( self.fVerbose):
            print("\n\n -- Read words from file: [{}].", fileName);
            print lines;
            
        inputWords = [ wd.strip() for wd in lines ];
        return inputWords;

    def GenernateMeaningsForWords( self, wordInfoList, fileName = None):
        """
            Generates the list of meanings for input word supplied.
            The generated meanings are stored in output file.

            Nothing returned.
        """
        
        if (self.fVerbose):
            print wordInfoList;
            
        outputFile = None;
        if (fileName != None):
            outputFile = open( fileName, "w");
        
        # iterate through each word info and produce an output
        for wdi in wordInfoList:
#        outText = "{:15s}\t{:10s}\t{:s}\t {:s}\t{:s}\n".format(
#            wdi["word"], wdi["partOfSpeech"], wdi["meaning"], wdi["synonym"], wdi["antonym"]);
            outText = "{:15s}\t{:10s}\t".format( wdi["word"], wdi["partOfSpeech"]);

            for j in wdi["meaning"]:
                outText += j + "\t";
            outText += "\n";

            if (outputFile != None):
                outputFile.write( outText);
            else:
                print outText;
        
        if (fileName != None):
            outputFile.close();

        return;

    def GenMeaningForWordsFromFile( self, inputFile1, outputFile1):
        inputWords = self.LoadInputWords( inputFile1);
        wordInfoList = [ self.wordHelpers.GetInfoOnWord(wd.strip(), 1) 
                            for wd in inputWords ];
        GenernateMeaningsForWords( wordInfoList);
        GenernateMeaningsForWords( wordInfoList, outputFile1);
        return wordInfoList;
    

    def Test_GetMeaningOfWords( self):
        return GenMeaningForWordsFromFile('tests/test1.txt', "tests/test.meanings.txt");

    def Test_LoadWords( self):
        # Read the Input Words List
        inputFile2 = 'jsb1000.txt';
        inputWords = self.LoadInputWords( inputFile2);
        print len(inputWords)
    
    # Process the words list and generate output with meanings for words
    def Test_GetMeaningForJSBWords( self):
        return GenMeaningForWordsFromFile( 'inputs/jsb1000.txt', "inputs/full.jsb1000.txt");
        
    def LoadWordMeanings( self, wordMeaningsFile):
        mwList = [];
        with open( wordMeaningsFile, 'rb') as csvfile:
            mwRead = csv.DictReader(csvfile);
            for mw in mwRead:
                mwList.append( mw);
        print "Loaded {} words from File [{}]".format(
            len(mwList), wordMeaningsFile);
        return mwList;

    def Test_Stemming( self):
        test1 = [ "water", "waterjug", "dilute", "dilution", "waterhshed", "quarter", "quartermaster", "quarterback"];
        print test1;
        print "\n......... Stemming .... ";
        # print stem( "indigestion");
        # print stemall( [ 'indigestion']);
        stem1 = stemall( test1);
        print len(test1);
        print len(stem1);

    def Test_StemmingOnJSBWords(self):
        stemInputs = stemall(inputWords);
        print len(stemInputs);
        setForInputs = set(inputWords);
        print len(setForInputs);
        diff1 = setForInputs.difference( stemInputs);
        diff2 = stemInputs.difference(setForInputs);
        print len(diff1);
        print len(diff2);

# ------------------------------------------------------------------------
class PuzzleGenerator(object):
    """
        Class to generating Puzzles for given set of words.
    """

    fVerbose = 0;

    def __init__(self, fVerbose=0):
        self.fVerbose = fVerbose;

    def GeneratePuzzle( self, i, inputWords):
        """
            Generates a puzzle for the supplied words
        """
        a = Crossword( 16, 16, '-', 3000, inputWords);
        a.compute_crossword(2);


        generatedPuzzle = {
            "problemNumber": i,
            "totalWords" : len(inputWords),
            "totalWordsGenerated" : len(a.current_word_list),
            "wordsList": inputWords,
            "generatedWords": [ str(word) for word in a.current_word_list],
            
            "wordsBank" : a.word_bank().split('\n'),
            "wordsFinder": a.word_find(),
            "wordsFinderSolution": a.solution(),
            
            "wordsCrossword": a.display(),
            "legend": a.legend().split('\n')
        };

        if (generatedPuzzle["totalWordsGenerated"] < generatedPuzzle["totalWords"]):
            print "WARNING: Only {} words out of {} was generated".format(
                generatedPuzzle["totalWordsGenerated"], 
                generatedPuzzle["totalWords"]);
        print "Input: ", [ w for (w, m) in inputWords];
        print "Generated: ", generatedPuzzle["generatedWords"];

        if (self.fVerbose):
            print generatedPuzzle;

        return generatedPuzzle;

    def GeneratePuzzleForIndexList( self, pnum, mwList, indexList):
        words10 = [ mwList[i] for i in indexList];
        pf10 = [ [ word['Word'], word['Meaning1']] for word in words10];
        return self.GeneratePuzzle( pnum, pf10);

    def WritePuzzleToFile( self, puzzleJSON, fileName):

        output1 = json.dumps( puzzleJSON, indent=4);

        with open( fileName, 'w') as fp:
            print >>  fp, output1

        print "\n Puzzle is written to output File [{}].".format( fileName);    
        return;

    def GeneratePuzzleForWordsInFile( self, inputFile, numPuzzles = 1):
        """
            Read in the meanings from input file and generate N puzzles
            by default only one puzzle file is generated.
        """
        wmManager = WordWithMeanings( self.fVerbose);
        mwList = wmManager.LoadWordMeanings( inputFile);
        numWords = len(mwList);
        puzzleList = [];

        # Create a random collection of indices to create random word sets
        indexList = range( numWords);
        random.shuffle( indexList); # in-place random collection is created

        if ( (numPuzzles < 1) or (numPuzzles *10 >= numWords)):
            numPuzzles = numWords / 10; # set to maximum number of puzzles

        if (numPuzzles == 1):
            puzzle = self.GeneratePuzzleForIndexList( 1, mwList, indexList[1:10]);
            puzzleList.append( puzzle);
            self.WritePuzzleToFile( puzzle, "outputs/test.json");
        else:
            # iterate through each collection of 10 words and generate puzzles
            for i in range( numPuzzles):
                # index is: (i-1)*10 to i*10
                print "\n\n [{}] Generating puzzle with {} words for indices[{}:{}]".format(
                    i, 10, i*10, (i+1)*10);
                puzzle = self.GeneratePuzzleForIndexList( 
                    i+1, mwList, indexList[ i*10:(i+1)*10]);
                puzzleList.append( puzzle);
                self.WritePuzzleToFile( puzzle, 
                    "outputs/puzzle_" + str(i+1) + ".json");

        return puzzleList;


# ------------------------------------------------------------------------
def main():
    puzzleGenerator = PuzzleGenerator( 0);
    puzzle1 = puzzleGenerator.GeneratePuzzleForWordsInFile( 
        'inputs/meanings.jsb1000.csv', 
        0);
    print "\n Successfully completed."

if __name__ == "__main__":
    main();


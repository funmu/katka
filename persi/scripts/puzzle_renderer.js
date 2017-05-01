/*
 *  puzzle_renderer.js
 *     Module to render word puzzles
 *
 *  ToDo: 
 *     Use responsive UI framework to style the deliverable
 * 
 */

 (function() {

 	'use strict';

	const puzzle_files_prefix = "puzzles/puzzle_";
	const puzzle_files_suffix = ".json";

	function GenHrefLink( pnum, hrefData) 
	{
		
		hrefData = hrefData + "&pn=" + pnum;
		return hrefData;
	}

	function GenHrefLinkForStartEnd( startNum, endNum, hrefData) 
	{
		
		hrefData = hrefData 
			+ "&start=" + startNum
			+ "&end=" + endNum;

		return hrefData;
	}

	function RenderAsIs( d3selector)
	{
		d3selector.append("td")
			.text( function(d) { return d; }
			);
	}		

 	/*
 	 *	Set up the PuzzleRender Object
 	 *
 	 *  @param{bool} verbose - verbosity level to show values
 	 */
 	var PuzzleRenderer = function( verbose)
 	{
 		this.self = this;
 		this.fVerbose = verbose;

 		if (this.fVerbose) {
 			console.log( "Created a new Puzzle Renderer");
 		}
 	}

 	/*
 	 *	Render a lit of items
 	 *
 	 *  @param{object} d3selector - d3 selector to attach objects to
 	 *
 	 *  @return{object} rowsGenerated - a list of rows generated for the the list
 	 */
 	PuzzleRenderer.prototype.RenderList = function( d3selector, listTitle, listClass, listOfItems, itemClass = "clue_item", fnRenderPuzzlet = RenderAsIs)
	{
		var dt = d3selector.append( "h2")
			.text( listTitle)
			.append("table")
			.attr("class", listClass)

		var rowsGenerated = dt.selectAll( "tr")
			.data( listOfItems)
			.enter()
			.append("tr")
			.attr( "class", itemClass)
			;

		fnRenderPuzzlet( rowsGenerated);

		return rowsGenerated;
	}

	PuzzleRenderer.prototype.GetPuzzleFilePath = function( pnum)
	{
		return puzzle_files_prefix + pnum + puzzle_files_suffix;
	}


	PuzzleRenderer.prototype.RenderPuzzleLink = function( hrefBase, d3selector)
	{
		d3selector.append("td")
			.attr( "class", "puzzlet")
			.append("a")
			.attr( "class", "puzzlet_link")
			.attr( "href", 
				function (d) {
					var hrefData = GenHrefLink( d, hrefBase);
					return hrefData;
				})
			.text( function (d) {
					return "Puzzle : " + d }
				);
	}

	PuzzleRenderer.prototype.RenderPuzzleGroupLink = function( hrefBase, d3selector)
	{
		d3selector.append("td")
			.attr( "class", "puzzlet")
			.append("a")
			.attr( "class", "puzzlet_link")
			.attr( "href", 
				function (d) {
					var hrefData = GenHrefLinkForStartEnd( d.startNum, d.endNum, hrefBase);
					return hrefData;
				})
			.text( function (d) {
					return "Puzzle For Group: " + d.startNum + " - " + d.endNum;
				});
	}

	PuzzleRenderer.prototype.RenderSectionOfPuzzle = function( 
		d3selector, puzzleRenderInfo, problemNumber, puzzleText, cluesList)
	{	
		d3selector.append("h2")
			.attr("class", "page_break")
			.text( puzzleRenderInfo.puzzleType + " " + problemNumber);

		var dt = d3selector.append("table")
			.attr( "width", "1000")
			.append("trow");

		dt.append("td")
			.attr( "width", puzzleRenderInfo.widthForPuzzle)
			.append( "pre")
			.attr("class", puzzleRenderInfo.classForPuzzle)
			.text( puzzleText);

		var dtf = dt.append("td")
			.attr( "width", puzzleRenderInfo.widthForClues)
			.attr("class", puzzleRenderInfo.classForClues);

		this.RenderList( dtf, 
			puzzleRenderInfo.cluesTitle,
			puzzleRenderInfo.cluesClass,
			cluesList);

		return d3selector;
	}

	var wordSearchRenderInfo = {
		puzzleType : "Word Search",
		widthForPuzzle : "70%",
		widthForClues : "30%",

		classForPuzzle : "words_finder",
		classForClues :  "words_finder_bank",

		cluesTitle : "Find Words",
		cluesClass : ""
	};

	var crosswordRenderInfo = {
		puzzleType : "Crossword",
		widthForPuzzle : "50%",
		widthForClues : "50%",

		classForPuzzle : "crosswords",
		classForClues :  "words_finder_bank",

		cluesTitle : "Word Clues", 
		cluesClass : "crosswords_clues"
	};

	PuzzleRenderer.prototype.RenderWordPuzzle = function ( anchor, puzzleInputs) 
	{
 		var d3selector = d3.select( anchor);

		if ( showWordSearch) {

			this.RenderSectionOfPuzzle( 
				d3selector, 
				wordSearchRenderInfo,
				puzzleInputs.problemNumber,
				puzzleInputs.wordsFinder,
				puzzleInputs.wordsBank);

		}
		
		if (showCrossword) {

			this.RenderSectionOfPuzzle( 
				d3selector, 
				crosswordRenderInfo,
				puzzleInputs.problemNumber,
				puzzleInputs.wordsCrossword,
				puzzleInputs.legend);

		}
	}


 	if ( (typeof module === 'undefined')) {
 		window.PuzzleRenderer = PuzzleRenderer;
 	}

 })();

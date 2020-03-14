/*
 *	xformSparksip.js - Generate Sparksip Projects List
 *
 *  Created: muralirk@gmail.com - March 12, 2017
 */

var fVerbose = false;
var fs = require('fs');
var fileToProcess = './inputs/1sponsor.json'; // sample file for testing purposes
var templateForHTML = "templates/templateForProjects.html";
var outputDirectoryRoot = "output/";
var outputIndexStart = 201900; // some random number. use a uniquefier in the future


const input_output_key_aliases = {

	"Timestamp" : "Timestamp",
	"ProjectId" : "ProjectId",

	"Email Address" : "ContactEmail",
	"ContactTitle" : "ContactTitle",
	"Name of your Organization" : "Organization",
	"OrganizationWebsite" : "OrganizationWebsite",
	"Who is the best contact  (name + email) if not you?": "ContactName",
	
	"Length of Internship (in number of weeks)" : "Length",
	"Number of hours per week": "HoursPerWeek",
	"Can you pay an optional stipend of (max of $500 per intern)?": "Stipend",
	
	"Project Title (6-8 words)" : "ProjectTitle",
	"Describe the project (3-5 sentences)": "Description",
	"Qualifications you are looking for (3-5 sentences)": "Qualifications",

	"Is there a Scientific or Business Research component?": "HasResearch",
	"Describe the Research Component (3-5 sentences)": "ResearchDescription"
};

// --=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Process Command line to get parameters for processing

if (process.argv.length > 2) {

	// 2nd argument is the year for which we are processing this input
	outputDirectory = outputDirectoryRoot + process.argv[2] + "/";
	outputIndexStart = parseInt(process.argv[2])*100;
} else {
	outputDirectory = outputDirectoryRoot + "Unknown" + "/"
}

if (process.argv.length > 3) {

	// 3rd argument is the input data file
	fileToProcess = process.argv[3];
}


if (process.argv.length > 4) {

	// 4th argument is the template HTML data file
	templateForHTML = process.argv[4];
}

// --=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
/*
 * Prints the JSON details
 * 
 *
 * @param{string} p - project information in JSON
 * @param{number} i - index of the project in the array
 * 
 * @return{object} model information object after applying the parameters.
 */
function printProjectsJSON( p, i) {

	console.log("\n ------------------------------------\n");
	console.log( "[%d] %s", i, p.ProjectTitle);
	console.log( "Description: %s", p.Description);

	console.log( "HasResearch: %s", p.HasResearch);
	console.log( "ResearchDescription: %s", p.ResearchDescription);

	console.log( "Email: %s", p.ContactEmail);
	console.log( "Contact: %s", p.ContactName);
	console.log( "Title: %s", p.ContactTitle);
	console.log( "Organization: %s", p.Organization);
	console.log( "Website: %s", p.OrganizationWebsite);

	console.log( "Qualifications: %s", p.Qualifications);

	console.log( "Stipend: %s", p.Stipend);
	console.log( "Length: %s", p.Length);
	console.log( "HoursPerWeek: %s", p.HoursPerWeek);
}

/*
 * Maps the alias long name keys to short structured key names
 * 
 *
 * @param{object} p - input object with long name keys from survey results
 * @param{i} integer - integer index for the object
 *		for processing data
 * 
 * @return{object} structured object with short key names
 */
function deAliasKeyNames( p, i) 
{
	const keysInput = Object.keys(p);
	var outputObject = {};
	keysInput.forEach( (k, i) => {
		outputObject[ input_output_key_aliases[k]] = p[k];
	});

	return outputObject;
}

/*
 * Formats the HTML information by applying the parameters 
 * 
 *
 * @param{string} htmlTemplateFile - reference to the template file
 * @param{parameters} array of objects - collection of parameters used 
 *		for processing data
 * 
 * @return{object} formatted HTML as a textual string
 */
function FormatModelInfo( htmlTemplateFile, parameters)
{

	var rawModelInfo = fs.readFileSync( htmlTemplateFile).toString();
	console.log( "\tLoaded model reference file: %s", htmlTemplateFile);

	for (var p in parameters) {

		var replacePart = new RegExp( "{" + p + "}", 'g');
		var replaceWith = JSON.stringify(parameters[p]);
		if (replaceWith[0] == "\"") {
			replaceWith = replaceWith.slice( 1, replaceWith.length - 1);
		}
		if (fVerbose) {
			console.log( "\tReplacing [%s] with %s", replacePart, replaceWith);
		}
		rawModelInfo = rawModelInfo.replace( replacePart, replaceWith);
	}

	return rawModelInfo;
}

/*
 * Process the incoming JSON files and format to HTML using a template.
 * Write the output to unique file per project supplied.
 *
 * @param{string} p - project information in JSON
 * @param{number} i - index of the project in the array
 * 
 * @return None
 */
function formatJSON2Html( p, i) {

	console.log("\n --- FORMATTING JSON PROJECT definition to HTML ---");
	console.log( "[%d] %s\n", i, p.ProjectTitle);
	p["ProjectId"] = outputIndexStart + i;
	var formattedHtml = FormatModelInfo( templateForHTML, p);

	// console.log( formattedHtml);
	var fileNameToOutput = outputDirectory + p["ProjectId"] + ".html";
	console.log("\tSaving HTML for [%d] into file [%s]", i, fileNameToOutput);
	fs.writeFileSync( fileNameToOutput, formattedHtml);
}


// --=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// Load up the input data file
var inputProjectsJSON = require( fileToProcess);

if (fVerbose) {
	console.log("\n\n ------------------------------------");
	console.log( inputProjectsJSON);
}

// Iterate through each project and output the JSON in pretty form
// projectsJSON.forEach( printProjectsJSON);

var projectsJSON = inputProjectsJSON.map( deAliasKeyNames);
console.log( projectsJSON);

// Iterate through each project, format the HTML and spit it out
projectsJSON.forEach( formatJSON2Html);
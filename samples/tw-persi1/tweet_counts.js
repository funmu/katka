// 
//  Count Number of Tweets
//

var Twitter = require('twitter');
var creds = require('./config1.json');
var twitter;

console.log( creds);
// set up the twitter object
twitter = new Twitter(creds);

// make a sample post using 
// apiPost(twitter);

// check the latest tweets
checkTwitter(twitter);

// set up twitter streams with parameters
function fetchAndPrintStream( twitter) {
	var ntweets = 0;
	twitter.stream(
			"statuses/filter", // string parameter for query sub-path
			{ "track": [ "awesome", "rad", "cool"]}, // object with tracking strings
			function( stream) {
				console.log( "---- SETTING up twitter.stream");

				stream.on( "data", function(tweet) {
					console.log( "hello tweet");
					console.log( " Tweet %d", ++ntweets);
					console.log( tweet.text);
				});

				stream.on( "error", function(tweet, statusCode) {
					console.log( "**** we got an error with %s Status Code", statusCode);
					console.log( tweet);
				});
			}
		);
}

function checkTwitter( twitter) 
{
	var params = {screen_name: 'nodejs'};
	console.log( "Let us get the user timeline stuff");

	twitter.get('statuses/user_timeline.json', params, 
		function(error, tweets, response){
			if (error) {
				console.log( "Error!!");
				console.log(error);
				throw error;
			}
			console.log( "Number of Tweets: %d", tweets.length);
		    // console.log(tweets);
		});
}

function apiPost( twitter)
{
	twitter.post('statuses/update', {status: 'Twitter API at https://dev.twitter.com/rest/public are well documented.'},  
	function(error, tweet, response){

		if(error) throw error;
		
		console.log(tweet);  // Tweet body. 
		console.log(response);  // Raw response object. 
	});
}
/*  TwitterHelper.js
 *
 */

 (function() {

 	// Module level dependencies
	var Twitter = require('twitter');
	// var creds = require('./config1.json');


	var TwitterHelper = function( credentials, verbose) 
	{
		this.fVerbose = true;
		this.creds = credentials;
		this.twitterClient = new Twitter( this.creds);
		this.tweetCounts = {};
	}

	TwitterHelper.prototype.getCounts = function()
	{
		return this.tweetCounts;
	}


	TwitterHelper.prototype.setupTweetCounter = function( username) 
	{
		if (this.fVerbose) { console.log( "Counting Tweets for %s", username);}		
		var params = {screen_name: username};
		var self = this;
		var lookFor = ["awesome", "cool", "elections"];
		lookFor.forEach( function(lf) {
			self.tweetCounts[lf] = 0;
		})

		// get data from the user_timeline stream
		this.twitterClient.stream('statuses/sample', 

			null, // { "track" : lookFor},

			function( stream) {

				console.log( "Stream is set up");
				stream.on('data', function(tweet) {
					console.log( tweet);
					console.log("inside stream:", tweet);
					if ( tweet.indexOf( "awesome")) {
						self.tweetCounts.awesome++;
					}
				});

				stream.on('error', function(error) {
				  console.log(error);
				});

			    // console.log(tweets);
			});
	}


// -------------------------------------------------------------------------
// export the constructor for local and remote usage

	if ((typeof module) === 'undefined') {
	    window.TwitterHelper =  TwitterHelper;
	} else {
	    module.exports =  TwitterHelper;
	}

 })();

// test-tw.js
var TH = require('./TwitterHelper');
var creds = require('./config.tw-persi1.json');

var thelper = new TH( creds, true);
thelper.setupTweetCounter( "muralirk");


// do periodic count prints
setInterval( function() {
	console.log( " Awesome reached : %d", thelper.tweetCounts.awesome);
}, 1000);

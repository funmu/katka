/*
 *  server.js
 *     Main server module for Application: {TEMPLATE_APP_NAME_GOES_HERE}
 * 
 */

 (function() {

 	'use strict';

 	/*
 	 *	Set up the TabManager Object
 	 *
 	 *  @param{Array} tabsList - array of tabs for display
 	 *  @param{bool} verbose - verbosity level to show values
 	 */

	// set up ======================================================================
	// get all the tools we need
	var port     = process.env.PORT || 8080;

	var express  = require('express');
	var app      = express();
	var passport = require('passport');
	var flash    = require('connect-flash');

	var morgan       = require('morgan');
	var cookieParser = require('cookie-parser');
	var bodyParser   = require('body-parser');
	var session      = require('express-session');

	// set up our express application
	app.use(morgan('dev')); // log every request to the console
	app.use(cookieParser()); // read cookies (needed for auth)
	app.use(bodyParser()); // get information from html forms

	app.set('view engine', 'ejs'); // set up ejs for templating

	var mongoose = require('mongoose');

	// configuration ===============================================================
	var configDB = require('./config/database.js');
	mongoose.connect(configDB.url); // connect to our database

	// require('./config/passport')(passport); // pass passport for configuration

	// required for passport
	app.use(session({ secret: 'trial_and_error_in_2017_from_1994' })); // session secret
	app.use(passport.initialize());
	app.use(passport.session()); // persistent login sessions
	app.use(flash()); // use connect-flash for flash messages stored in session


	// routes ======================================================================
	require('./app/routes.js')(app, passport); // load our routes and pass in our app and fully configured passport

	// launch ======================================================================
	app.listen(port);
	console.log('Get started at the service on port ' + port);

}) ();





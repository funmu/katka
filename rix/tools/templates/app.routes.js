/*
 *  app/routes.js
 *     Setup all routes for handling the various actions
 * 
 */

 (function() {

 	'use strict';

	// route middleware to make sure a user is logged in
	function isLoggedIn(req, res, next) {

	    // if user is authenticated in the session, carry on 
	    if (req.isAuthenticated())
	        return next();

	    // if they aren't redirect them to the home page
	    res.redirect('/');
	}

	function getHomePage(req, res) {
        res.render('index.ejs', {
        	user: req.user
        }); // load the index.ejs file
    }

	function getLoginPage(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('login.ejs', { message: req.flash('loginMessage') }); 
    }

	function getLoginLocalPage(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('login_local.ejs', { message: req.flash('loginMessage') }); 
    }

	function getSignupPage(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('signup.ejs', { message: req.flash('signupMessage') });
    }

	function getProfilePage(req, res) {
        res.render('profile.ejs', {
            user : req.user // get the user out of session and pass to template
        });
    }

	function handleLogout(req, res) {
        req.logout();
        res.redirect('/');
    }

    // -------------------------------
    // QUOTEs related code
    // -------------------------------
    var ourModels = require('../app/models/modelloader');
    var QuotesModel = ourModels.quoteModel;

	function getQuotesPage(req, res) {

		// Use the user Id to ask for quotes for this specific user
        QuotesModel.find( { userid : req.user.id}, 
        	function( err, quotes) {
        	console.log( " Got %d quotes ", quotes.length);
        	console.log( quotes);
        	res.render( 'quotes.ejs', {
        		user : req.user,
        		quotes: quotes
        	});
        });
    }

    // -------------------------------
    // Applications related code
    // -------------------------------
    var ApplicationsModel = ourModels.applicationModel;

	function getApplicationsPage(req, res) {

		// Use the user Id to ask for quotes for this specific user
        ApplicationsModel.find( { userid : req.user.id}, 
        	function( err, applications) {
        	console.log( " Got %d quotes ", applications.length);
        	console.log( applications);
        	res.render( 'appslist.ejs', {
        		user : req.user,
        		applications: applications
        	});
        });
    }    

    // -------------------------------
    // Configuration of Routing Table
    // -------------------------------

    var _routingTable = {
    	getMethods : [
    		{ path: "/", handler: getHomePage, loginRequired: false },
    		{ path: "/login", handler: getLoginPage, loginRequired: false },
    		{ path: "/login_local", handler: getLoginLocalPage, loginRequired: false },
    		{ path: "/profile", handler: getProfilePage, loginRequired: true },
    		{ path: "/appslist", handler: getApplicationsPage, loginRequired: true },
    		{ path: "/quotes", handler: getQuotesPage, loginRequired: true },
    		{ path: "/logout", handler: handleLogout, loginRequired: true }
    	],
    	postMethodsForAuthentication: [
    		{ path: "/login", handler: function( passport) {
    			return passport.authenticate('local-login', {
			        successRedirect : '/', // redirect to the secure profile section
			        failureRedirect : '/login', // redirect back to the login page if there is an error
			        failureFlash : true // allow flash messages
			    }) 
    		}},
    		{ path: "/signup", handler: function( passport) {
    			return passport.authenticate('local-signup', {
			        successRedirect : '/', // redirect to the secure profile section
			        failureRedirect : '/signup', // redirect back to the signup page if there is an error
			        failureFlash : true // allow flash messages
			    }) 
    		}}
    	],
    	getMethodsForAuthentication: [
    		{ path: "/auth/google", handler: function( passport) {
    			return passport.authenticate('google', { scope : ['profile', 'email'] });
    		}},
    		{ path: "/auth/google/callback", handler: function( passport) {
    			return passport.authenticate('google', {
                    successRedirect : '/', 	// redirect to the secure profile section
                    failureRedirect : '/'			// redirect back to home page for errors
	            })
    		}}
    	]  	
    };

	function RouteManager(app, passport) {

		// Use the routing table to set up the routes
		_routingTable.getMethods.forEach( function( handlerInfo, i) {

			console.log( "  Route [%d]: Get handler set up for path: %s", 
				i, handlerInfo.path);
			if ( handlerInfo.loginRequired) {
				app.get( handlerInfo.path, isLoggedIn, handlerInfo.handler);
			} else {
				app.get( handlerInfo.path, handlerInfo.handler);
			}
		});

		_routingTable.postMethodsForAuthentication.forEach( function( handlerInfo, i) {

			console.log( "  Route [%d]: Post handler for Authentication set up for path: %s", 
				i, handlerInfo.path);
			app.post( handlerInfo.path, handlerInfo.handler( passport));
		});

		_routingTable.getMethodsForAuthentication.forEach( function( handlerInfo, i) {

			console.log( "  Route [%d]: Get handler for Authentication set up for path: %s", 
				i, handlerInfo.path);
			app.get( handlerInfo.path, handlerInfo.handler( passport));
		});

/*
	// Pre-routing table code

	    // =====================================
	    // HOME PAGE (with login links) ========
	    // =====================================
	    app.get('/', getHomePage);

	    // =====================================
	    // LOGIN ===============================
	    // =====================================
	    // show the login form
	    app.get('/login', getLoginPage);

	    // process the login form
	    app.post('/login', passport.authenticate('local-login', {
	        successRedirect : '/profile', // redirect to the secure profile section
	        failureRedirect : '/login', // redirect back to the login page if there is an error
	        failureFlash : true // allow flash messages
	    }));

	    // =====================================
	    // SIGNUP ==============================
	    // =====================================
	    // show the signup form
	    app.get('/signup', getSignupPage);

	    // process the signup form
		app.post('/signup', passport.authenticate('local-signup', {
	        successRedirect : '/profile', // redirect to the secure profile section
	        failureRedirect : '/signup', // redirect back to the signup page if there is an error
	        failureFlash : true // allow flash messages
	    }));

	    // =====================================
	    // PROFILE SECTION =====================
	    // =====================================
	    // we will want this protected so you have to be logged in to visit
	    // we will use route middleware to verify this (the isLoggedIn function)
	    app.get('/profile', isLoggedIn, getProfilePage);

	    // =====================================
	    // GOOGLE ROUTES =======================
	    // =====================================
	    // send to google to do the authentication
	    // profile gets us their basic information including their name
	    // email gets their emails
	    app.get('/auth/google', 
	    	passport.authenticate('google', { scope : ['profile', 'email'] }));

	    // the callback after google has authenticated the user
	    app.get('/auth/google/callback',
	            passport.authenticate('google', {
	                    successRedirect : '/profile',
	                    failureRedirect : '/'
	            }));

	    // =====================================
	    // LOGOUT ==============================
	    // =====================================
	    app.get('/logout', handleLogout);

*/	    
	};

	module.exports = RouteManager;
}) ();





/*
 *  config/passport.js
 *     We handle everything related to using passport for signup and logins
 * 
 */

 (function() {

    'use strict';

    // load all the things we need
    var LocalStrategy   = require('passport-local').Strategy;
    var GoogleStrategy = require('passport-google-oauth').OAuth2Strategy;

    // load up the user model
    var ourModels = require('../app/models/modelloader');
    var UserModel = ourModels.userModel;

    // load the auth variables
    var configAuth = require('./auth');

    // expose this function to our app using module.exports
    function PassportManager(passport) {

        // =========================================================================
        // passport session setup ==================================================
        // =========================================================================
        // required for persistent login sessions
        // passport needs ability to serialize and unserialize users out of session

        // used to serialize the user for the session
        passport.serializeUser(function(user, done) {
            done(null, user.id);
        });

        // used to deserialize the user
        passport.deserializeUser(function(id, done) {
            UserModel.findById(id, function(err, user) {
                done(err, user);
            });
        });

        // =========================================================================
        // LOCAL SIGNUP ============================================================
        // =========================================================================
        // we are using named strategies since we have one for login and one for signup
        // by default, if there was no name, it would just be called 'local'

        passport.use('local-signup', new LocalStrategy({
                // by default, local strategy uses username and password, we will override with email
                usernameField : 'email',
                passwordField : 'password',
                passReqToCallback : true // allows us to pass back the entire request to the callback
            },
            function(req, email, password, done) {

                // asynchronous
                // UserModel.findOne wont fire unless data is sent back
                process.nextTick(function() {

                    // find a user whose email is the same as the forms email
                    // we are checking to see if the user trying to login already exists
                    UserModel.findOne({ 'local.email' :  email }, function(err, user) {
                        // if there are any errors, return the error
                        if (err)
                            return done(err);

                        // check to see if there's already a user with that email
                        if (user) {
                            return done(null, false, 
                                req.flash('signupMessage', 'That email is already taken.'));
                        } else {

                            // if there is no user with that email
                            // create the user
                            var newUser            = new UserModel();

                            console.log( "Getting name from Req Body as: ", req.body.name);
                            // set the user's local credentials
                            newUser.local.email    = email;
                            newUser.local.name     = req.body.name;
                            newUser.local.password = newUser.generateHash(password);

                            // save the user
                            newUser.save(function(err) {
                                if (err)
                                    throw err;
                                return done(null, newUser);
                            });
                        }

                    });    

                });
        }));

        // =========================================================================
        // LOCAL LOGIN =============================================================
        // =========================================================================
        // we are using named strategies since we have one for login and one for signup
        // by default, if there was no name, it would just be called 'local'

        passport.use('local-login', new LocalStrategy({
            // by default, local strategy uses username and password, we will override with email
            usernameField : 'email',
            passwordField : 'password',
            passReqToCallback : true // allows us to pass back the entire request to the callback
        },
        function(req, email, password, done) { // callback with email and password from our form

            // find a user whose email is the same as the forms email
            // we are checking to see if the user trying to login already exists
            UserModel.findOne({ 'local.email' :  email }, function(err, user) {
                // if there are any errors, return the error before anything else
                if (err)
                    return done(err);

                // if no user is found, return the message
                if (!user)
                    return done(null, false, req.flash('loginMessage', 'No user found.')); // req.flash is the way to set flashdata using connect-flash

                // if the user is found but the password is wrong
                if (!user.validPassword(password))
                    return done(null, false, req.flash('loginMessage', 'Password is not valid; Please try again.')); // create the loginMessage and save it to session as flashdata

                // all is well, return successful user
                return done(null, user);
            });

        }));

        // =========================================================================
        // GOOGLE ==================================================================
        // =========================================================================
        passport.use(new GoogleStrategy({

            clientID        : configAuth.googleAuth.clientID,
            clientSecret    : configAuth.googleAuth.clientSecret,
            callbackURL     : configAuth.googleAuth.callbackURL,

        },
        function(token, refreshToken, profile, done) {

            // make the code asynchronous
            // User.findOne won't fire until we have all our data back from Google
            process.nextTick(function() {

                // try to find the user based on their google id
                UserModel.findOne({ 'google.id' : profile.id }, function(err, user) {
                    if (err)
                        return done(err);

                    if (user) {

                        // if a user is found, log them in
                        return done(null, user);
                    } else {
                        // if the user isnt in our database, create a new user
                        var newUser          = new UserModel();

                        // set all of the relevant information
                        newUser.google.id    = profile.id;
                        newUser.google.token = token;
                        newUser.google.name  = profile.displayName;
                        newUser.google.email = profile.emails[0].value; // pull the first email

                        // save the user
                        newUser.save(function(err) {
                            if (err)
                                throw err;
                            return done(null, newUser);
                        });
                    }
                });
            });

        }));
    }

    module.exports = PassportManager;
})();

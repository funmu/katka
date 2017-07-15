/*
 *  app/models/user.js
 *     Defines and loads the User Model
 * 
 */

 (function() {

    'use strict';

    // 
    // load the things we need
    var mongoose = require('mongoose');
    var bcrypt   = require('bcrypt-nodejs');
    var user_model = require('./user.json');

    // define the schema for our user model
    var userSchema = mongoose.Schema( user_model);

    // methods ======================
    // generating a hash
    userSchema.methods.generateHash = function(password) {
        return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
    };

    // checking if password is valid
    userSchema.methods.validPassword = function(password) {
        return bcrypt.compareSync(password, this.local.password);
    };

    // create the model for users and expose it to our app
    module.exports = {
        userModel: mongoose.model('User', userSchema)
    };
})();
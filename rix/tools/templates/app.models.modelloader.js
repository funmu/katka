/*
 *  app/models/user.js
 *     Defines and loads the User Model
 * 
 */

 (function() {

    function _buildModelMap() 
    {
        // 
        // load the things we need
        var mongoose = require('mongoose');
        var bcrypt   = require('bcrypt-nodejs');
        var user_model = require('./user.json');
        var quote_model = require('./quote.json');

        // define the schema for our user model
        var userSchema = mongoose.Schema( user_model);
        var quoteSchema = mongoose.Schema( quote_model);

        // var application_model = require('./application.json');
        // var applicationSchema = mongoose.Schema( application_model);

        // methods ======================
        // generating a hash
        userSchema.methods.generateHash = function(password) {
            return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
        };

        // checking if password is valid
        userSchema.methods.validPassword = function(password) {
            return bcrypt.compareSync(password, this.local.password);
        };

        var modelMap = {
            userModel: mongoose.model('User', userSchema),
            quoteModel: mongoose.model('Quote', quoteSchema)
            // , applicationModel: mongoose.model('Application', applicationSchema)
        };

        return modelMap;
    }

    // Use a singleton modelMap if possible.
    _modelMap = _buildModelMap();

    // create the model for users and expose it to our app
    module.exports = _modelMap;

})();
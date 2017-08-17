/*
 *  app/models/user.js
 *     Defines and loads the User Model
 * 
 */

 (function() {

    ///
    /// getSchemaFromModel - generates the schema file required for database loader
    ///
    /// @param{Object} modelInfo - model from which to extract MongoDB file
    ///
    /// @return{Object} - schema model for use with MongoDB initialization
    ///
    function getSchemaFromModel( modelInfo) 
    {
        // get the modelInfo.properties and flatten with type of each object
        var propertyNames = Object.keys( modelInfo.properties);
        var schemaBag = {};
        propertyNames.forEach( function ( propName, i) {
            schemaBag[ propName] = modelInfo.properties[propName].type;
        });

        return schemaBag;
    }

    function _buildModelMap() 
    {
        // 
        // load the things we need
        var mongoose = require('mongoose');

        // ============== User Model Related code ==============
        var user_model = require('./user.json');
        var bcrypt   = require('bcrypt-nodejs');
        var userSchema = mongoose.Schema( user_model);
        // generating a hash
        userSchema.methods.generateHash = function(password) {
            return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
        };

        // checking if password is valid
        userSchema.methods.validPassword = function(password) {
            return bcrypt.compareSync(password, this.local.password);
        };

        // ============== Application Related code ==============
        var application_model = require('./application.json');
        var applicationSchema = mongoose.Schema( application_model);

        // ============== Quotes Related code ==============

        var quote2Model = require('./common.quote.json');
        var quote_properties = getSchemaFromModel( quote2Model);
        var quoteSchema = mongoose.Schema( quote_properties);

        // old way of doing it. 
        // var quote_model = require('./quote.json');
        // var quoteSchema = mongoose.Schema( quote_model);

        // ============== OKR1 Related code ==============

        var OKR1Model = require('./common.OKR1.json');
        var okr1_properties = getSchemaFromModel( OKR1Model);
        var okr1Schema = mongoose.Schema( okr1_properties);


        // ============== Construct final Model Map ==============
        var modelMap = {
            userModel: mongoose.model('User', userSchema)
            , quoteModel: mongoose.model('Quote', quoteSchema)
            , OKR1Model: mongoose.model('OKR1', okr1Schema)
            , applicationModel: mongoose.model('Application', applicationSchema)
        };

        return modelMap;
    }

    // Use a singleton modelMap if possible.
    _modelMap = _buildModelMap();

    // create the model for users and expose it to our app
    module.exports = _modelMap;

})();
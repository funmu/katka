# RIX - Rapid Information Exchange
 RIX is an attempt to create framework for authenticated experience for personal information management.

## Folders
 - [tools](tools/) scripts to build out the application using templates
 - [Template Files](tools/templates/) Template files used to generate parts of application
 - [test1](test1/) sample test app - test1

## Adding new Model
 Following steps help you to add a new model - say for maintaining a list of *'qoutes'*

### draft1 (July 20, 2017)
 - Add a new model file *app.models.quote.json*
 - Include model file in the Model Loader at *app.modelloader.js*
 - include a way to show the list of model outputs in index.js (and later move it to separate file of its own)

### draft2 (July 30, 2017)
 - Add a new model file *common.models.quote.json*
 - Add function *getSchemaFromModel()* to app.models.modelloader.js to extract schema
 - ToDo: add a central directory of all model/schema files and update it with the new model file entry.



## References
  
### Node JS
  - [Node JS](http://npmjs.org) and upgrade using [NodeJS download](https://nodejs.org/en/download/).
     Node.js was installed at */usr/local/bin/node*
     npm was installed at */usr/local/bin/npm*
  - [Node Upgrade](https://www.solarianprogrammer.com/2016/04/29/how-to-upgrade-nodejs-mac-os-x/)

### Tools for CSS and HTML5
 - [Font Awesome Icons](http://fontawesome.io/icons/) - great collection of icons to use
 
### Authentication
- [Easy Authentication with NodeJS](https://scotch.io/tutorials/easy-node-authentication-setup-and-local)


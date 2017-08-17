#!/bin/bash
# Copyright (C) 2016 Murali Krishnan "All Rights Reserved"
#   Last Revised 07/03/2017
#

## Usage: create_node_server.sh [options] app_name
##
## Options:
##  -h, --help      Display this message.
##  -n, --dryrun    Dry-run; Shows only what will be done.
##  -v, --verbose   Verbose logging of outputs.
##  -f, --force     Force creation of all files without checking for time stamp
##  -c, --configFrom    Location to fetch config settings from
##  -m, --macosx    On MAC OSX
##  -d, --directory Prepare the directories for copying files into.
##  -p, --package   Prepare the packages for nodejs app
##  -t, --toolsdir  Root directory for Tools (default: ./tools)
##
## Description:
##  Prepares the folders and files for an application given the app name
##

# ------------------------------------------------------------------------------------
# Process Command Line Arguments
#
COMMAND_NAME=$0;

usage() {
    [ "$*" ] && echo "$0: $*"; echo
    sed -n '/^##/,/^$/s/^## \{0,1\}//p' "$0"
    exit 2
} 2>/dev/null

error_exit() {
    echo "${COMMAND_NAME}: Exiting with error" 1>&2;
    exit 1;
}

SetMacMode() {

    ON_MAC=1;
    SED_CMD="sed -i -e";

}

echo

TOOLS_DIRECTORY_ROOT=./tools
FULL_LOGGING=0
CONFIG_FROM="./config.auth.js"
FORCE_CREATION=0
SED_CMD="sed -i"
while [ $# -gt 0 ]; do
    case $1 in
        (-n) DRY_RUN=1; shift;;
        (-h|-\?|--help) usage ; shift;;
        (-v|--verbose) FULL_LOGGING=1; shift;;
        (-f|--force) FORCE_CREATION=1; shift;;
        (-d|--directory) PREP_DIRECTORY=1; shift;;
        (-m|--macosx) SetMacMode; shift;;
        (-p|--package) PREP_PACKAGE=1; shift;;
        (-c|--config)  CONFIG_FROM=$2; shift 2;;
        (-*) usage "$1: unknown option";;
        (*) APP_NAME_FOR_CREATION=$1; shift;;
    esac
done

if [ -z $APP_NAME_FOR_CREATION ]; then
    echo No app name is specified.
    usage;
fi

# ------------------------------------------------------------------------------------
# Functional routines ... 

CreateFoldersForServer() {

    FOLDERS_TO_CREATE=( $* );
    FOLDER_ROOT=${FOLDERS_TO_CREATE[0]};

    for ((i = 1; i < ${#FOLDERS_TO_CREATE[@]}; i+= 1)); do
        echo Creating folder: $FOLDER_ROOT/${FOLDERS_TO_CREATE[$i]}
        CMD_TO_EXECUTE="mkdir -p  $FOLDER_ROOT/${FOLDERS_TO_CREATE[$i]}"
        if [ $DRY_RUN ]; then
            echo $CMD_TO_EXECUTE
        else
            $CMD_TO_EXECUTE
        fi
        echo
    done
};


CreatePackageJSON() {

    PACKAGES_TO_ADD=( $* );
    TMP_PACKAGE_JSON="/tmp/package_$APP_NAME_FOR_CREATION.json"

    echo "{" > $TMP_PACKAGE_JSON;
    echo "   \"name\": \"$APP_NAME_FOR_CREATION\"," >> $TMP_PACKAGE_JSON
    echo "   \"version\": \"1.0.0\"," >> $TMP_PACKAGE_JSON
    echo "   \"description\": \"starting version of $APP_NAME_FOR_CREATION \"," >> $TMP_PACKAGE_JSON
    echo "   \"main\": \"server.js\"," >> $TMP_PACKAGE_JSON
    echo "   \"scripts\": {" >> $TMP_PACKAGE_JSON
    echo "      \"start\": \"nodemon server.js\"," >> $TMP_PACKAGE_JSON
    echo "      \"test\": \"echo \\\"Error: No Test specified\\\" && exit 1\"" >> $TMP_PACKAGE_JSON
    echo "   }," >> $TMP_PACKAGE_JSON
    echo "   \"author\": \"Murali\"," >> $TMP_PACKAGE_JSON
    echo "   \"repository\": \"\"," >> $TMP_PACKAGE_JSON
    echo "   \"license\": \"ISC\"," >> $TMP_PACKAGE_JSON

    # let us now ensure dependencies are created
    echo "   \"dependencies\": {" >> $TMP_PACKAGE_JSON
    LAST_PACKAGE_INDEX=$((${#PACKAGES_TO_ADD[@]}-1));
    for ((i = 0; i < $LAST_PACKAGE_INDEX; i+= 1)); do
        echo Adding package: ${PACKAGES_TO_ADD[$i]}
        echo "       \"${PACKAGES_TO_ADD[$i]}\": \"latest\"," >> $TMP_PACKAGE_JSON
    done

    # no trailing commas for the last item
    if [ $LAST_PACKAGE_INDEX -ge 0 ]; then
        echo Adding package: ${PACKAGES_TO_ADD[$LAST_PACKAGE_INDEX]}
        echo "       \"${PACKAGES_TO_ADD[$LAST_PACKAGE_INDEX]}\": \"latest\"" >> $TMP_PACKAGE_JSON
    fi
    echo "   }" >> $TMP_PACKAGE_JSON    
    echo "}" >> $TMP_PACKAGE_JSON
    echo

    CMD_TO_EXECUTE="cp $TMP_PACKAGE_JSON $APP_NAME_FOR_CREATION/package.json"
    if [ $DRY_RUN ]; then
        echo $CMD_TO_EXECUTE
    else
        $CMD_TO_EXECUTE
    fi
    echo
}

CopyFromSourceToDest() {

    SOURCE_FILE=$1      # do not escape the first file
    DEST_FILE=$APP_NAME_FOR_CREATION/$2

    DO_COPY=;  # nothing to start with
    if [ ! -z $FORCE_CREATION ]; then
        DO_COPY=YES;
    else
        echo Optimizing the copy of files
        if ( [ -e $SOURCE_FILE ] && [ -e $DEST_FILE ] ); then

            TS1=`stat -r $SOURCE_FILE | cut -d ' ' -f 10`
            TS2=`stat -r $DEST_FILE | cut -d ' ' -f 10`
            if [ "1$TS1" -gt "1$TS2" ]; then DO_COPY=YES; fi
        elif ( [ -e $SOURCE_FILE ] ); then
            DO_COPY=YES;
        fi
    fi

    if [ $DO_COPY ]; then
        echo Copy updated file: $SOURCE_FILE to $DEST_FILE.
        TEMPLATE_TO_REPLACE={TEMPLATE_APP_NAME_GOES_HERE}
        REPLACE_SED_COMMAND="s/$TEMPLATE_TO_REPLACE/$APP_NAME_FOR_CREATION/g"    
        CMD_TO_EXECUTE1="cp $SOURCE_FILE $DEST_FILE"
        CMD_TO_EXECUTE2="$SED_CMD $REPLACE_SED_COMMAND $DEST_FILE"     
        if [ $DRY_RUN ]; then
            echo $CMD_TO_EXECUTE1
            echo $CMD_TO_EXECUTE2
        else
            echo $CMD_TO_EXECUTE1
            $CMD_TO_EXECUTE1
            $CMD_TO_EXECUTE2
        fi
        echo
    else
        if [ $FULL_LOGGING -gt 0 ]; then
            echo Skipping older file: $SOURCE_FILE
        fi
    fi
}

CopyFromTemplate() {

    SOURCE_FILE=$TOOLS_DIRECTORY_ROOT/templates/$1
    CopyFromSourceToDest $SOURCE_FILE $2
}

CreateFilesFromTemplate() 
{

    CopyFromTemplate "app.server.js" "server.js";
    CopyFromTemplate "app.routes.js" "app/routes.js";
    CopyFromTemplate "assets.styles-1.css" "public/assets/styles-1.css";

    CopyFromTemplate "config.database.js" "config/database.js";
    CopyFromTemplate "config.passport.js" "config/passport.js";

    CopyFromTemplate "views.index.ejs" "views/index.ejs";

    CopyFromTemplate "views.header.ejs" "views/header.ejs";
    CopyFromTemplate "views.footer.ejs" "views/footer.ejs";

    CopyFromTemplate "views.loginform.inc" "views/loginform.ejs";

    CopyFromTemplate "views.profile.ejs" "views/profile.ejs";
    CopyFromTemplate "views.login.ejs" "views/login.ejs";
    CopyFromTemplate "views.login_local.ejs" "views/login_local.ejs";
    CopyFromTemplate "views.signup.ejs" "views/signup.ejs";
    CopyFromTemplate "views.appslist.ejs" "views/appslist.ejs";

    CopyFromTemplate "views.quotes.ejs" "views/quotes.ejs";
    CopyFromTemplate "views.quoteAdd.inc" "views/quoteAdd.ejs";
    CopyFromTemplate "views.quote_add.ejs" "views/quote_add.ejs";

    CopyFromTemplate "views.okr1.ejs" "views/okr1.ejs";

    # Get Special files from special locations
    echo .... copying the special file from $CONFIG_FROM
    CopyFromSourceToDest $CONFIG_FROM "config/auth.js";
    echo    
}

CreateModelsFromTemplate() 
{

    CopyFromTemplate "app.models.modelloader.js" "app/models/modelloader.js";

    CopyFromTemplate "app.models.user.json" "app/models/user.json";
    CopyFromTemplate "app.models.application.json" "app/models/application.json";

    # CopyFromTemplate "app.models.quote.json" "app/models/quote.json";

    CopyFromTemplate "common.models.application.json" "app/models/common.application.json";
    CopyFromTemplate "common.models.quote.json" "app/models/common.quote.json";
    CopyFromTemplate "common.models.okr1.json" "app/models/common.okr1.json";

    echo

}


PostCreationSteps() {

    echo
    echo " Connect to mongo database and set up a database";
    echo "   Database Name: $APP_NAME_FOR_CREATION_db";
    echo "   Collection: users";


    echo
    echo Install the Node Packages using the following command at [$APP_NAME_FOR_CREATION]
    echo "   \"npm install\""
}


echo
echo ----------------------------------------------------------


FOLDERS_FOR_NODE_WITH_AUTHENTICATION=( 
    "app"
    "app/models"
    "assets"    
    "config"
    "public"
    "public/assets"
    "views"    
    )

FILES_FOR_NODE_WITH_AUTHENTICATION=(
    "app/models/user.js"        # user model file
    "app/routes.js"             # all the routes for our application
    "config/auth.js"            # will hold all our client secret keys (facebook, twitter, google)
    "config/database.js"        # will hold our database connection settings
    "config/passport.js"        # configuring the strategies for passport
    "views/index.ejs"           # show our home page with login links
    "views/login.ejs"           # show our login form
    "views/signup.ejs"          # show our signup form
    "views/profile.ejs"         # show profile after user logs in
    "package.json"              # handle our npm packages
    "server.js"                 # setup our application
    )

NODE_PACKAGES_FOR_APP=(
    "express"           # web server framework 
    "ejs"               # templating engine
    "mongoose"          # object modeling for our MongoDB database
    "passport"          # framework for authenticating with different methods
    "connect-flash"     # allows us passing session flashdata messages.
    "bcrypt-nodejs"     # gives us the ability to hash the password.
    "passport-local"    # passport strategy for local database    
#    "passport-facebook" # passport strategy for facebook
    "passport-twitter"  # passport strategy for twitter
    "passport-google-oauth" # passport strategy for google OAuth
    "morgan"            # log module for requests
    "body-parser"       # Express 4.0 module for parsing HTTP POST body
    "cookie-parser"     # Handle HTTP cookies
    "method-override"   # simulates DELETE and PUT
    "express-session"   # Express 4.x session management
    )

if [ ! -z $PREP_DIRECTORY ]; then

    echo  Set up Node Server with Authentication for: $APP_NAME_FOR_CREATION
    echo ----------------------------------------------------------
    CreateFoldersForServer $APP_NAME_FOR_CREATION ${FOLDERS_FOR_NODE_WITH_AUTHENTICATION[@]};
fi

if [ ! -z $PREP_PACKAGE ]; then

    echo  Create package.json for: $APP_NAME_FOR_CREATION
    echo ----------------------------------------------------------
    CreatePackageJSON ${NODE_PACKAGES_FOR_APP[@]};
fi

echo  Create basic set of files from template
echo ----------------------------------------------------------
CreateModelsFromTemplate;
CreateFilesFromTemplate;

echo ----------------------------------------------------------
echo  Follow up Actions after creation ...
echo ----------------------------------------------------------
PostCreationSteps;
echo;

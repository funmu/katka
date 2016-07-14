# My OneDrive

*My OneDrive* is a simple utility to list and download files from OneDrive storage.

##Problem##
OneDrive provides a convenient way to store files. To manage storage and ensure we have a local copy of the files, a utility is required to list and download files. 

##Solution Approach##
The scripts here use [OneDrive SDK](https://github.com/OneDrive/onedrive-sdk-python) in Python to access the OneDrive storage. A simple class is provided for listing, getting, and downloading the files.

A separate configuration file is required to specify account details. For security reasons, the exact configuration file is not stored here. 

###Configuration###
 Set up an app for accessing One Drive using [Apps for Accesss](
 https://apps.dev.microsoft.com/). 

 Then copy over the [Config Template](configTemplate.ini) to create your own local config file named **myConfig.ini** to use with the python script.

##Code##
 * [myOneDrive](myOneDrive.py) - main script for downloading files
 * [class AccessOneDrive](AccessOneDrive.py) - helper class for handling OneDrive usage as per my needs
 * [List Config](listConfig.py) - simple script to list config file details (used for testing and viewing configuration)
 * [Config Template](configTemplate.ini) - sample configuration file


###Wish List###
 * Logging - write out log to a separate file for analysis
 * Copy over folders into appropriate folder structure in the destination. (Right now there is only one level based on last part of the path name)
 * Use conditional input file to perform deletion to remove unwanted files at OneDrive

##Contributors##
Murali Krishnan


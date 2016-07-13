# Get My OneDrive

*Get My OneDrive* is a simple utility to list and download files from OneDrive storage.

##Problem##
OneDrive provides a convenient way to store files. To manage storage and ensure we have a local copy of the files, a utility is required to list and download files. 

##Solution Approach##
The scripts here use [OneDrive SDK](https://github.com/OneDrive/onedrive-sdk-python) in Python to access the OneDrive storage. A simple class is provided for listing, getting, and downloading the files.

A separate configuration file is required to specify account details. For security reasons, the exact configuration file is not stored here. 

##Code##
 * [getMyOneDrive](getMyOneDrive.py) - main script for downloading files
 * [List Config](listConfig.py) - simple script to list config file details
 * [Config Template](configTemplate.ini) - sample configuration file


###Wish List###
 * Logging - write out log to a separate file for analysis
 * Copy over folders into appropriate folder structure in the destination. (Right now there is only one level based on last part of the path name)
 * Use conditional input file to perform deletion to remove unwanted files at OneDrive

##Contributors##
Murali Krishnan


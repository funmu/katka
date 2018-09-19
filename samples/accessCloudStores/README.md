# Access Cloud Stores

Collection of Python utility programs to access Cloud Stores to retrieve relevant content to list and download files.

##Problem##
Cloud File Stores provide a convenient way to store files. However managing files and having local copies are harder. Especially harder when users are charged for accessing the content over time. Further cleaning up content (thousands of pictures from cell phone uploads) are not easy. So we need a way to manage the files and download them.

OneDrive provides a convenient way to store files. To manage storage and ensure we have a local copy of the files, a utility is required to list and download files. 

Similarly DropBox also provides API access to fetch and manage files.

##Solution Approach##
The scripts here use SDK from appropriate cloud storage providers.

 * [OneDrive SDK](https://github.com/OneDrive/onedrive-sdk-python) in Python to access the OneDrive storage. And there are several samples to build from at [OneDrive github](https://github.com/OneDrive/). Set up an app for OneDrive access using[Apps for Accesss](https://apps.dev.microsoft.com/). 
 * [Dropbox SDK](https://www.dropbox.com/developers) provides access to DropBox storage.

A separate configuration file is required to specify account details. For security reasons, the exact configuration file is not stored here. 

A simple class is provided for listing, getting, and downloading the files. 

###Configuration###
 
 Then copy over the [Config Template](configTemplate.ini) to create your own local config file named **myConfig.ini** to use with the python script.

##Code##
 * [myCloudStorage](myOneDrive.py) - scripts for accessing cloud storage files
 * [class AccessOneDrive](AccessOneDrive.py) - helper class for handling OneDrive usage as per my needs
 * [class AccessDropBox](AccessDropBox.py) - helper class for handling OneDrive usage as per my needs
 * [class StorageHelper](StorageHelper.py) - helper class for storage related access
 * [List Config](listConfig.py) - simple script to list config file details (used for testing and viewing configuration)
 * [Config Template](configTemplate.ini) - sample configuration file
  
##Usage##
	python myCloudStorage.py -c $CONFIGFILE -s Dropbox
	python myCloudStorage.py -c $CONFIGFILE -s OneDrive


###Wish List###
 * Logging - write out log to a separate file for analysis.
 * Use conditional input file to perform deletion to remove unwanted files.

##Contributors##
Murali Krishnan


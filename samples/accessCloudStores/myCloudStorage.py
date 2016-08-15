#!/usr/bin/python

#
#  myCloudStorage.py 
#  -- script to help access files on Cloud Storage
#
#  Dependencies
#   - DropBox SDK
#	- OneDrive SDK
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = 'Murali Krishnan'
__version__ = "v1.0.0"

from optparse import OptionParser;


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up global configuration
_CLOUD_STORE_TO_ACCESS='OneDrive';

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Load Command Line Arguments

usage = "Usage: %prog [options]";
optParser = OptionParser(usage = usage, 
				version="%prog 1.0",
				description="Access files on cloud storage.");
optParser.add_option("-c", "--config", dest="configFile",
					default = "myConfig.ini",
                 	help="Read configuration from FILE [default = %default]", 
                 	metavar="FILE");
optParser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout [default]");
optParser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout");
optParser.add_option("-s", "--useStorage",
					default = _CLOUD_STORE_TO_ACCESS,
                  	dest="storageService",
                  	help="access storage from service [default = %default]");

(options, args) = optParser.parse_args()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
from AccessDropBox import AccessDropBox;
from AccessOneDrive import AccessOneDrive;
import ConfigParser;
import StorageHelper as SH;

# ------------ MAIN Section starts here -----------------------

def main():
	if (options.verbose):
		print("\t Reading Config File %s" % options.configFile);

	storageHelper = SH.AccessStorageHelper( options.verbose);

	print("\n1. Creating the Object to access Dropbox");
	if ( options.storageService == "Dropbox"):
		accountType = "DropboxAccount";
		aod = AccessDropBox( options.verbose);
	elif (options.storageService == "OneDrive"):
		accountType = "HotmailAccount";
		aod = AccessOneDrive( options.verbose);
	else:
		optParser.error("ERROR: Unknown cloud storage service specified.");
		exit();

	if (options.verbose):
		print(" Using Storage Service: {}".format(accountType));

	print("\n2. Parse in the configuration file to fetch access details.");
	Config = ConfigParser.ConfigParser()
	Config.read( options.configFile);

	if (len(Config.sections()) == 0):
		optParser.error("ERROR: Invalid Config File or no config sections found");
		exit();

	foldersToDownload = [];
	if ( Config.has_option( accountType	, "FoldersToDownload")):
		folders = Config.get( accountType	, "FoldersToDownload");
		foldersToDownload = folders.split('\n');

	foldersToList = [];
	if ( Config.has_option( accountType	, "FoldersToList")):
		folders = Config.get( accountType	, "FoldersToList");
		foldersToList = folders.split('\n');

	foldersToDelete = [];
	if ( Config.has_option( accountType	, "FoldersToDelete")):
		folders = Config.get( accountType	, "FoldersToDelete");
		foldersToDelete = folders.split('\n');

	print( "\n3. Get connected to Storage Service using my access token");
	if ( options.storageService == "Dropbox"):
		client_token = Config.get( accountType	, "AccessToken");
		redirect_uri = Config.get( accountType	, "WebRedirectUri");
		aod.Connect( client_token);
	elif (options.storageService == "OneDrive"):
		client_id = Config.get( accountType, "AppId");
		client_secret =  Config.get( accountType, "AppSecret");
		redirect_uri = Config.get( accountType, "WebRedirectUri");
		aod.Connect( client_id, redirect_uri, client_secret);
	else:
		optParser.error("ERROR: Unknown cloud storage service specified.");
		exit();

	if ( len(foldersToList) > 0): 
		print( "\n4. Enumerate items in given paths");
		items = storageHelper.Apply( foldersToList, aod.GetAndShowItems);
		storageHelper.PrintItems( items);

	if ( len(foldersToDownload) > 0): 
		if ( Config.has_option( accountType	, "DownloadPath")):
			downloadPath = Config.get( accountType	, "DownloadPath");
		else:
			downloadPath = u".";

		print( "\n5. Download Items");
		storageHelper.DownloadItems( foldersToDownload, 
			aod.GetAndShowItems,
			aod.DownloadItem, 
			downloadPath);
	
	if ( len(foldersToDelete) > 0):
		print( "\n6. Delete Items");
#		storageHelper.Apply( foldersToDelete, aod.DeleteItems);
		storageHelper.DeleteItems( foldersToDelete,
			aod.GetAndShowItems,
			aod.DeleteItem,
			downloadPath);

if __name__ == "__main__":
    main()


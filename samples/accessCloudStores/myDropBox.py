#!/usr/bin/python

#
#  nyDropbox.py 
#  -- script to help access files on Dropbox
#
#  Dependencies
#   -  DropBox SDK
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = 'Murali Krishnan'

from optparse import OptionParser;
import ConfigParser;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Load Command Line Arguments

usage = "Usage: %prog [options]";
optParser = OptionParser(usage = usage, 
				version="%prog 1.0",
				description="List Configuration Information for One Drive Access.");
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

(options, args) = optParser.parse_args()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
from AccessDropBox import AccessDropBox;

# ------------ MAIN Section starts here -----------------------
import ConfigParser

def main():
	if (options.verbose):
		print("\t Reading Config File %s" % options.configFile);
	Config = ConfigParser.ConfigParser()
	Config.read( options.configFile);

	if (len(Config.sections()) == 0):
		optParser.error("Invalid Config File or no config sections found");
		exit();

	accountType = "DropboxAccount";
	foldersToDownload = [];
	if ( Config.has_option( accountType	, "FoldersToDownload")):
		folders = Config.get( accountType	, "FoldersToDownload");
		foldersToDownload = folders.split('\n');

	foldersToList = [];
	if ( Config.has_option( accountType	, "FoldersToList")):
		folders = Config.get( accountType	, "FoldersToList");
		foldersToList = folders.split('\n');

	client_token = Config.get( accountType	, "AccessToken");
	redirect_uri = Config.get( accountType	, "WebRedirectUri");

	print("\n1. Creating the Object to access Dropbox");
	aod = AccessDropBox( 0);

	print( "\n2. Getting connected to Dropbox using my access token");
	aod.Connect( client_token);


	if ( len(foldersToList) > 0): 
		print( "\n3. Enumerate items in a given path");
		items = aod.Apply( foldersToList, aod.GetAndShowItems);
		aod.ListItems( items);

	if ( len(foldersToDownload) > 0): 
		print( "\n4. Download Items");
		# items = aod.Apply( foldersToDownload, aod.GetAndShowItems);
		# aod.DownloadItem( items[0]);
		# aod.Apply( items, aod.DownloadItem);
		aod.DownloadItems( foldersToDownload);

if __name__ == "__main__":
    main()


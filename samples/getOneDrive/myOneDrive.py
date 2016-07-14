#!/usr/bin/python

#
#  myOneDrive.py 
#  -- script to help access files on One Drive
#
#  Dependencies
#   -  OneDriveSDK
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = 'Murali Krishnan'
from AccessOneDrive import AccessOneDrive;

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

	foldersToDownload = [];
	if ( Config.has_option("HotmailAccount", "FoldersToDownload")):
		folders = Config.get("HotmailAccount", "FoldersToDownload");
		foldersToDownload = folders.split('\n');

	foldersToList = [];
	if ( Config.has_option("HotmailAccount", "FoldersToList")):
		folders = Config.get("HotmailAccount", "FoldersToList");
		foldersToList = folders.split('\n');

	client_id = Config.get("HotmailAccount", "AppId");
	client_secret =  Config.get("HotmailAccount", "AppSecret");
	redirect_uri = Config.get("HotmailAccount", "WebRedirectUri");

	print("\n1. Creating the Object to access One Drive");
	aod = AccessOneDrive( 0);

	print( "\n2. Getting connected to One Drive using my ID and secret");
	aod.Connect( client_id, redirect_uri, client_secret);


	if ( len(foldersToList) > 0): 
		print( "\n3. Enumerate items in a given path");
		aod.Apply( foldersToList, aod.GetAndShowItems);

	if ( len(foldersToDownload) > 0): 
		print( "\n4. Download Items");
		aod.Apply( foldersToDownload, aod.DownloadItems);

if __name__ == "__main__":
    main()


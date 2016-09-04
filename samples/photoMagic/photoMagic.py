#!/usr/bin/python

#
#  photoMagic.py 
#  -- script to help manage Photo Files
#
#  Credits
#
#	Python Library for UI with sample for Photo Viewer 
#    - http://www.blog.pythonlibrary.org/2010/03/26/creating-a-simple-photo-viewer-with-wxpython/


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = 'Murali Krishnan'
__version__ = "v1.0.0"

from optparse import OptionParser;
import StorageHelper as SH;
from AccessLocalDrive import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up global configuration

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Load Command Line Arguments
_CLOUD_STORE_TO_ACCESS = "LocalDrive";

usage = "Usage: %prog [options]";
optParser = OptionParser(usage = usage, 
				version="%prog 1.0",
				description="Display and Manage Photos.");

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

def printSeparator():
	print( "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
import ConfigParser;

# ------------ MAIN Section starts here -----------------------

def main():
	if (options.verbose):
		print("\t Reading Config File %s" % options.configFile);

	print("\n1. Parse in the configuration file to fetch access details.");
	Config = ConfigParser.ConfigParser()
	Config.read( options.configFile);
	if (len(Config.sections()) == 0):
		optParser.error("ERROR: Invalid Config File or no config sections found");
		exit();

	storageHelper = SH.AccessStorageHelper( options.verbose);

	print("\n2. Creating the Object to access Dropbox");
	if ( options.storageService == "LocalDrive"):
		accountType = "LocalDrive";
		aod = AccessLocalDrive( options.verbose);
	else:
		optParser.error("ERROR: Unknown cloud storage service specified.");
		exit();

	foldersToList = [];
	if ( Config.has_option( accountType	, "FoldersToList")):
		folders = Config.get( accountType	, "FoldersToList");
		foldersToList = folders.split('\n');

	if ( len(foldersToList) > 0): 
		printSeparator();
		print("3. Enumerate items in given paths");
		items = storageHelper.Apply( foldersToList, aod.GetAndShowItems);
		storageHelper.PrintItems( items);




if __name__ == "__main__":
    main()


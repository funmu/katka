#!/usr/bin/python
# configParser Example

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
#  Helper Functions

def GetAndPrintList( config, listName):
	print("\n   List %s" % listName);
	folderList = [];
	if ( config.has_option("HotmailAccount", listName)):
		folders = config.get("HotmailAccount", listName);
		folderList = folders.split('\n');
		for item in folderList:
			print "\t %s" % item;
	else:
		print("\t No List is found for: %s" % listName);

def GetAndPrintOption( config, section, option):
	print( "\t {:15}: {:40}".format( section, config.get( section, option)));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Load Configuration File and print out configuration options

def main():
	if (options.verbose):
		print("\t Reading Config File %s" % options.configFile);
	Config = ConfigParser.ConfigParser()
	Config.read( options.configFile);

	if (len(Config.sections()) == 0):
		optParser.error("Invalid Config File or no config sections found");
		exit();

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	#  Print out configuration details
	print("\n Configuration from the input File: %s" % options.configFile);
	GetAndPrintOption( Config, "HotmailAccount", "Description");
	GetAndPrintOption( Config, "HotmailAccount", "Name");
	GetAndPrintOption( Config, "HotmailAccount", "AppSecret");
	GetAndPrintOption( Config, "HotmailAccount", "AppId");
	GetAndPrintOption( Config, "HotmailAccount", "WebRedirectUri");
	GetAndPrintOption( Config, "HotmailAccount", "MobileRedirectUri");

	GetAndPrintList( Config, "FoldersToDownload");
	GetAndPrintList( Config, "FoldersToList");

if ( __name__ == "__main__"):
	main();

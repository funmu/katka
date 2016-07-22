#!/usr/bin/python

#
#  getMyOneDrive.py 
#  -- script to help access files on One Drive
#
#  Dependencies
#   -  OneDriveSDK
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
import onedrivesdk;
from onedrivesdk.helpers import GetAuthCodeServer;

from PIL import Image; # for image processing
import os; # for file access

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	AccessOneDrive - Class to access and use OneDrive
class AccessOneDrive:

	fVerbpse = 0;
	client = None;	
	idPathDirectory = {};

	def __init__(self, verbose):
		self.fVerbose = verbose;

	def Connect( self, clientId, redirectUri, clientSecret):

		print( "\t  a.Creating a client object");
		self.client = onedrivesdk.get_default_client(client_id=clientId,
		                                        scopes=[
		                                        # 'wl.signin',
		                                         #       'wl.offline_access',
#		                                                "offline_access",
		                                                'onedrive.readwrite'])

		print( "\t  b.Getting an authorization URL");
		auth_url = self.client.auth_provider.get_auth_url(redirectUri);
		# print( auth_url);

		#this will block until we have the code

		print( "\t  c.Getting the Auth code");
		code = GetAuthCodeServer.get_auth_code(auth_url, redirectUri);
		# print(code);

		print( "\t  d.Complete the authentication process");
		self.client.auth_provider.authenticate(code, redirectUri, clientSecret);
		# print("\t authentication complete ...");
		return;

	def GetCollection( self, topNLevels):
		#get the top three elements of root, leaving the next page for more elements
		collection = self.client.item(drive="me", id="root").children.request(top = topNLevels).get();
		return collection;

	def _printItem( self, index, item):
		if (item is None):
			print(" No item was found");
		else:
			itemFullName = item.name if item.folder is None else "/"+item.name;
			print("{} {} \"{:30}\" {:,d}".format( '' if index == 0 else index, item.id, itemFullName, item.size));

	def printItemWithPath( self, index, item, itemPath = None):
		if (item is None):
			print(" No item was found");
		else:
			if (itemPath is None):
				itemFullName = item.name if item.folder is None else "/"+item.name;
			else:
				itemFullName = itemPath;

			print("{} {} \"{}\"".format( '' if index == 0 else index, item.id, itemFullName));

	def ListItems( self, items, printItem = 1):
		itemList = [];
		basecount = 0;
		while (not items is None):
			count = 1;
			for count, item in enumerate( items):
				if (printItem):
					self._printItem( basecount+count, item);
				itemList.append( item);

			basecount = basecount + len(items);

			#get the next page of three elements, if none exist, returns None
			items = None if items.next_page_request is None else items.next_page_request.get();
			print( "\t .... fetched {} items".format( basecount));
		return itemList;

	def GetItemsForId( self, itemId):
		if (self.fVerbose):
			print( "\n Accessing items for itemID = {0}".format( itemId));
		return self.client.item( id=itemId).children.request(top=200).get();

	def GetItemForPath( self, itemPath):

		if (self.fVerbose): 
			print( "\n Accessing items using the path supplied = {0}".format( itemPath));

		if ( not self.idPathDirectory.has_key( itemPath)):
			#  split the path into smaller parts to find the specific ID
			parentPathEndsAt = itemPath.rfind( '/');
			parentPath = itemPath[0:parentPathEndsAt];
	
			if (parentPathEndsAt == 0):
				itemsInParent = self.GetItemsForId( "root");
			else:
				parentItem = self.GetItemForPath( parentPath);
				itemsInParent = self.GetItemsForId( parentItem.id);

			count = 0
			for count, item in enumerate( itemsInParent):
				# add the to item to directory
				subItemPath = parentPath + "/" + item.name;
				self.idPathDirectory[subItemPath] = item;
				if (self.fVerbose):
					print( "Adding new item {0} to local Directory at path = {1}".format( item.id, subItemPath));

		itemForPath = self.idPathDirectory[ itemPath];

		return itemForPath;

	def GetAndShowItems( self, path):
		print("\n--------------------------------------------------------")
		print(" Enumerating items in folder \"{}\"".format( path));
		print("--------------------------------------------------------")
		item = self.GetItemForPath( path);
		if (self.fVerbose):
			self.printItemWithPath( 0, item, path);

		subItemsStart = self.GetItemsForId( item.id);
		allItems = self.ListItems( subItemsStart);
		return allItems;

	def DownloadItems( self, path):
		print("\n--------------------------------------------------------")
		print(" Downloading files for folder \"{}\"".format( path));
		print("--------------------------------------------------------")
		item = self.GetItemForPath( path);
		if (self.fVerbose):
			self.printItemWithPath( 0, item, path);

		subItemsStart = self.GetItemsForId( item.id);
		allItems = self.ListItems( subItemsStart, 0);

		parentPathEndsAt = path.rfind( '/');
		downloadPath = path[parentPathEndsAt+1:] + "/";
		if (not os.path.exists( downloadPath)):
			print("\t Creating the directory {}".format(downloadPath));
			createdDir = os.makedirs( downloadPath);

		numFilesDownloaded = 0;
		numBytesDownloaded = 0;
		numFolders = 0;

		# Now let us really download each item and save it away
		for item in allItems:
			if (item.folder):
				print( "\tskipping folder: \{}\"".format(item.name));
				numFolders += 1;
			else:
				print( " get \"{:30}\" Id: {} size: {:,d}".format( item.name, item.id, item.size));
				fileName = downloadPath + item.name;
				if ( os.path.isfile( fileName) and (os.path.getsize( fileName) == item.size)):
					print("\tskipping same sized file");
				else:
					self.client.item( id = item.id).content.request().download( fileName);
					numFilesDownloaded += 1;
					numBytesDownloaded += item.size;				

		print("\n Total of {:,d} files. Downloaded {:,d} files of size {:,d} bytes".format( len(allItems), numFilesDownloaded, numBytesDownloaded));
		print("\t Skipped {:,d} files".format( len(allItems) - numFilesDownloaded));
		print("\t Skipped {:,d} folders".format( numFolders));

		return allItems;

	def Apply( self, list, applyFunction):
		for item in list:
			applyFunction( item);

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

	# mobile Redirect URI does not work ... troubleshoot later.
	# redirect_uri = mobile_redirect_uri;


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


#!/usr/bin/python

#
#  AcessOneDrive.py 
#  -- Class for handling OneDrive related access
#
#  Dependencies
#   -  OneDriveSDK
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = 'Murali Krishnan'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
import onedrivesdk;
from onedrivesdk.helpers import GetAuthCodeServer;
import StorageHelper as SH;

from PIL import Image; # for image processing

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	AccessOneDrive - Class to access and use OneDrive
class AccessOneDrive:

	fVerbpse = 0;
	client = None;	
	idPathDirectory = {};
	storageHelper = None;

	def __init__(self, verbose):
		self.fVerbose = verbose;
		self.storageHelper = SH.AccessStorageHelper( verbose);

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
			print( "\t .... fetched {} items\n".format( basecount));
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
				# add the item to directory
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

	def DownloadItems( self, path, downloadRoot = u"."):
		print("\n--------------------------------------------------------")
		print(" Downloading files for folder \"{}\"".format( path));
		print("--------------------------------------------------------")
		item = self.GetItemForPath( path);
		if (self.fVerbose):
			self.printItemWithPath( 0, item, path);

		subItemsStart = self.GetItemsForId( item.id);
		allItems = self.ListItems( subItemsStart, 0);

		downloadPath = downloadRoot+ path + "/";
		self.storageHelper.CreateDirectory( downloadPath);

		numFilesDownloaded = 0;
		numBytesDownloaded = 0;
		numFolders = 0;

		# Now let us really download each item and save it away
		for item in allItems:
			if (item.folder):
				print( "\tskipping folder: \{}\"".format(item.name));
				numFolders += 1;
			else:
				fileName = downloadPath + item.name;
				toDownload = self.storageHelper.IsDownloadRequired( item.name, item.size, fileName);

				if ( toDownload):
					print( u"Downloading {:15s} {:15s} {:,d} "
						.format( item.name, item.id, item.size));
					self.client.item( id = item.id).content.request().download( fileName);
					numFilesDownloaded += 1;
					numBytesDownloaded += item.size;				

		print("\n Total of {:,d} files. Downloaded {:,d} files of size {:,d} bytes"
			.format( len(allItems), numFilesDownloaded, numBytesDownloaded));
		print("\t Skipped {:,d} files".format( len(allItems) - numFilesDownloaded));
		print("\t Skipped {:,d} folders".format( numFolders));

		return allItems;

	def PrintItems( self, items):
		count = 1;
		for count, item in enumerate( items):
			self._printItem( count, item);

	def Apply( self, list, applyFunction):
		allItems = [];
		for item in list:
			foundItems = applyFunction( item);
			allItems.extend( foundItems);
		return allItems;

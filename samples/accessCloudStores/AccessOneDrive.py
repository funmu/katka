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
		self._setupRootNode();

	def _setupRootNode(self):
		newStorageItem = SH.AccessStorageItem(self.fVerbose);
		newStorageItem.name 	= "root"
		newStorageItem.id 		= "root";
		newStorageItem.path 	= "/";
		newStorageItem.num_bytes= 0;
		newStorageItem.is_dir	= True;
		newStorageItem.modified_date = "NoDate";
		newStorageItem.revision	= "NoRevision";
		self.idPathDirectory[ newStorageItem.path] = newStorageItem;

		if (self.fVerbose):
			print("------ ROOT ITEM ----------");
			newStorageItem.PrintItem(0);

	def Connect( self, clientId, redirectUri, clientSecret):

		print( "\t  a. Creating a client object");
		self.client = onedrivesdk.get_default_client(client_id=clientId,
		                                        scopes=[
		                                        #	'wl.signin',
		                                        #   'wl.offline_access',
												#	"offline_access",
												 'onedrive.readwrite'])

		print( "\t  b. Getting an authorization URL");
		auth_url = self.client.auth_provider.get_auth_url(redirectUri);
		# print( auth_url);

		#this will block until we have the code

		print( "\t  c. Getting the Auth code");
		code = GetAuthCodeServer.get_auth_code(auth_url, redirectUri);
		# print(code);

		print( "\t  d. Complete the authentication process");
		self.client.auth_provider.authenticate(code, redirectUri, clientSecret);
		# print("\t authentication complete ...");

		print( "\t  e. Load up the children for root node after connection");
		rootItem = self.idPathDirectory["/"];
		allItems = self.GetAllItemsForId( rootItem.id, "");
		rootItem.children = allItems;

		return;

	def GetCollection( self, topNLevels):
		#get the top three elements of root, leaving the next page for more elements
		collection = self.client.item(drive="me", id="root").children.request(top = topNLevels).get();
		return collection;

	def PrintItem( self, index, item):
		if (item is None):
			print(" No item was found");
		else:
			itemFullName = item.name if item.folder is None else "/"+item.name;
			print("{:3} {:10} {:10} \"{:30}\" {:10}"
				.format( '' if index == 0 else index, 
						item.id, item.folder,
						itemFullName, item.size));


	def ListItems( self, items, printItem = 1):
		itemList = [];
		basecount = 0;
		while (not items is None):
			count = 1;
			for count, item in enumerate( items):
				if (printItem):
					self.PrintItem( basecount+count, item);
				itemList.append( item);

			basecount = basecount + len(items);

			#get the next page of three elements, if none exist, returns None
			items = None if items.next_page_request is None else items.next_page_request.get();
			if (self.fVerbose):
				print( "\t .... fetched {} items\n".format( basecount));
		return itemList;

	def GetAllItemsForId( self, itemID, pathForItem):
		"""
			Give the itemID and path, let us find all the items.
			Convert these to standard representation and add the path for item as well.
		"""
		if (self.fVerbose):
			print( "\n\t\t Accessing items itemID = {0} at path = {1}"
				.format( itemID, pathForItem));

		# Let us construct the details for the specified path
		subItemsStart = self.client.item( id=itemID).children.request(top=200).get();
		allItems = self.ListItems( subItemsStart, 0);
		storageItems = [];
		count = 0
		for count, item in enumerate(allItems):
			newStorageItem = SH.AccessStorageItem(self.fVerbose);
			newStorageItem.name 	= item.name;
			newStorageItem.id 		= item.id;
			newStorageItem.path 	= pathForItem + "/" + item.name;
			newStorageItem.num_bytes= item.size;
			newStorageItem.is_dir	= item.folder;
			newStorageItem.modified_date = item.last_modified_date_time;
			newStorageItem.revision	= "NoRevision";
			storageItems.append( newStorageItem);
			# add the item to directory for faster lookup
			self.idPathDirectory[newStorageItem.path] = newStorageItem;
			if (self.fVerbose):
				print( "\n\t add new item {0} at path = {1}"
					.format( newStorageItem.id, newStorageItem.path));
				newStorageItem.PrintItem(count);

		return storageItems;

	def GetItemForPath( self, itemPath):

		if (self.fVerbose): 
			print("---------------------------------------------------------------");
			print( "\t Accessing items using the path supplied = {0}"
				.format( itemPath));

		if ( not self.idPathDirectory.has_key( itemPath)):
			#  split the path into smaller parts to find the specific ID
			parentPathEndsAt = itemPath.rfind( '/');
			parentPath = itemPath[0:parentPathEndsAt];
	
			if (parentPathEndsAt > 0):
				parentItem = self.GetItemForPath( parentPath);

		itemForPath = self.idPathDirectory[ itemPath];
		if ( itemForPath.isFolder() and itemForPath.children is None):
			allItems = self.GetAllItemsForId( itemForPath.id, itemPath);
			itemForPath.children = allItems;

		if (self.fVerbose):
			print("~~~~~~~ GOT ITEM for path {}".format(itemPath));
			itemForPath.PrintItem( 0);

		return itemForPath;

	def GetAndShowItems( self, path):
		print("---------------------------------------------------------------");
		print(" Enumerating items in folder \"{}\"".format( path));
		item = self.GetItemForPath( path);

		allItems = [item] if (item.children is None) else item.children;
		return allItems;

	def _downloadFile( self, item, outputFileName):
		# We need to make sure that any parent directories exist beforehand
		succeeded = 1;
		try:
			self.client.item( id = item.id).content.request().download( outputFileName);
		except:
			print( "\n~~~~~~ ERROR: unable to download item");
			item.PrintItem();
			succeeded = 0;
		return succeeded;

	def DownloadItem( self, item, destRoot = u"."):
		"""
			Download the items locally within the destination root path given

		"""
		downloadInfo = { "folder": 0, "file": 0, "bytes": 0, "skipped" : 0 }

		outputFileName = destRoot +  item.path;
		if ( item.isFolder()):
			self.storageHelper.CreateDirectory( outputFileName);
			self.storageHelper.DownloadItems( [item.path], 
				self.GetAndShowItems,
				self.DownloadItem, 
				destRoot);
			downloadInfo["folder"] += 1;								
		else:
			toDownload = self.storageHelper.IsDownloadRequired( item.path, item.num_bytes, outputFileName);

			if ( toDownload):
				print( u"Downloading {:15,d} {:40s} rev:{:15s} to {:40s}"
					.format( item.num_bytes, item.path, item.revision, 
						outputFileName
					));
				if (not self._downloadFile( item, outputFileName)):
					downloadInfo["skipped"]	= 1;
				downloadInfo["bytes"] = item.num_bytes;
				downloadInfo["file"] = 1;
			else:
				downloadInfo["skipped"]	= 1;

		return [downloadInfo];

	def DeleteItem( self, item, deleteConfirmed, destRoot = u"."):
		"""
			Check and Delete an item

		"""
		deleteInfo = { "folder": 0, "file": 0, "bytes": 0, "download": 0 }

		if (item.isFolder()):
			print( "\tskipping folder: \{}\"".format(item.name));
			deleteInfo["folder"] += 1;
		else:
			fileName = destRoot + item.path;
			toDownload = self.storageHelper.IsDownloadRequired( item.path, item.num_bytes, fileName);

			if ( toDownload):
				print( u" Download Required for: {:15s} {:15s} {:,d} "
					.format( item.name, item.id, item.num_bytes));
			else:
				print( u"******** Ready for deletion : {:15s} {:15s} {:,d} "
					.format( item.name, item.id, item.num_bytes));

				confirmForItem = deleteConfirmed;
				if (confirmForItem == 0):
					confirm = raw_input("Confirm delete? Y/N: ")
					if (confirm == "Y"):
						confirmForItem = 1;

				if (confirmForItem == 1):
					self.client.item( id = item.id).delete()
					print( u"\tDeleted file : {:s}".format( item.name));
					deleteInfo["file"] += 1;
					deleteInfo["download"] += 1;
					deleteInfo["bytes"] += item.num_bytes;

		return [deleteInfo];


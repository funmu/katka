#!/usr/bin/python

"""
	Class and helpers to handle Dropbox related content


	Dependencies
	-  DropBox SDK installed using
		pip install dropbox
"""
__author__ = 'Murali Krishnan'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
import dropbox;
import StorageHelper as SH;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AccessDropBox:
	"""
		Class to access Dropbox account to list and download files.
	"""

	fVerbose = 0;
	client = None;	
	idPathDirectory = {};
	storageHelper = None;

	def __init__(self, verbose):
		self.fVerbose = verbose;
		self.storageHelper = SH.AccessStorageHelper( verbose);

	def Connect( self, access_token):

		if (self.fVerbose):
			print( "\t  a.Creating a client object");
		self.client = dropbox.client.DropboxClient(access_token)
		if (self.fVerbose):
			print( "\t  d.Complete the authentication process");		
			print 'linked account: ', self.client.account_info()
		return;

	def GetCollection( self, folderPath):
		"""
			Get the files and folders at the 'folderPath'
		"""
		if (self.fVerbose):
			print( "\t  Getting metadata for folder: {}".format( folderPath));

		folder_metadata = self.client.metadata( folderPath);
		# print 'metadata: ', folder_metadata
		collection = folder_metadata["contents"];
		return collection;

	def isFolder(self, item):
		"""
			Check if the given item is a folder
		"""
		return (item["is_dir"]);

	def _printItem( self, index, item):
		if (item is None):
			print(" No item was found");
		else:
			# itemFullName = item.name if not self.isFolder(item) else "/"+item.name;
			print( u"{:4d}. {:15s} {:15s} {:40s} "
				.format( index, item["rev"], 
					"Folder" if self.isFolder(item) else item["size"],
					item["path"]
				));

	def ListItems( self, items, printItem = 1):
		"""
			List the items to cosole
		"""		
		itemList = [];

		# Dropbox provides a full list without pagination
		count = 1;
		for count, item in enumerate( items):
			if (printItem):
				self._printItem( count + 1, item);
			itemList.append( item);

		return itemList;

	def GetAndShowItems( self, path, goDeep = 1):
		"""
			Enumerate the items included below the path.
		"""

		if (self.fVerbose):
			print("\n--------------------------------------------------------")
			print(" Enumerating items in folder \"{}\"".format( path));
			print("--------------------------------------------------------")

		subItemsStart = self.GetCollection( path);
		allItems = subItemsStart;

		subFoldersList = [folder for folder in subItemsStart if self.isFolder(folder)];

		numItems = len(subItemsStart);
		numFolders = len(subFoldersList);
		numFiles = numItems - numFolders;

		if (self.fVerbose):
			print("\t ---- Folder {:30s} has {:,d} folders and {:,d} files"
				.format( path, numFolders, numItems));

		if ( goDeep ):
			for folder in subFoldersList:
				if (self.fVerbose):
					print("\n --- Enumerating Folder {:30s}".format(folder["path"]));
				subItems = self.GetCollection( folder["path"]);
				numInFolder = len(subItems);
				allItems.extend( subItems);

				numItems += numInFolder;
				foldersHere = [folder for folder in subItems if self.isFolder(folder)];
				numFoldersHere = len(foldersHere);
				numFilesHere = numInFolder - numFoldersHere;

				numFolders += numFoldersHere;
				numFiles += numFilesHere;
				if (self.fVerbose):
					print("\t ---- Folder {:30s} has {:,d} folders and {:,d} files"
						.format( folder["path"], numFoldersHere, numFilesHere)); 

		print( "\nTotal of {:10d} items: {:10d} folders and {:10d} items\n"
			.format(numItems, numFolders, numFiles));
		return allItems;

	def _downloadFile( self, path, outputFileName):
		f = self.client.get_file( path);
		print( u"Download file {:30s} to {:40s}"
			.format( path, outputFileName));
		out = open( outputFileName, 'wb');
		out.write(f.read());
		out.close();
		return;

	def DownloadItem( self, item, destRoot = u"."):
		"""
			Download the items locally within the destination root path given

		"""
		savedList = [];

		if (item is None):
			print(" No item was found");
		else:

			outputFileName = destRoot + item["path"];
			if ( self.isFolder( item)):
				self.storageHelper.CreateDirectory( outputFileName);
			else:
				toDownload = self.storageHelper.IsDownloadRequired( item["path"], item["bytes"], outputFileName);

				if ( toDownload):
					print( u"Downloading {:15s} {:15s} {:40s} "
						.format( item["rev"], item["size"], item["path"]
						));
					self._downloadFile( item["path"], outputFileName);

			savedList = [ outputFileName];

		return savedList;

	def DownloadItemsForPaths( self, foldersToDownload, downloadPath = u"."):
		print("\n--------------------------------------------------------")
		print(" Downloading files for folder \"{}\"".format( foldersToDownload));
		print("--------------------------------------------------------")
		items = self.Apply( foldersToDownload, self.GetAndShowItems);

		self.storageHelper.CreateDirectory( downloadPath);

		allItems = self.Apply( items, self.DownloadItem);
		return allItems;

	def DownloadItems( self, folderToDownload, downloadPath = u"."):
		print("\n--------------------------------------------------------")
		print(" Downloading files for folder \"{}\"".format( folderToDownload));
		print("--------------------------------------------------------")
		items = self.GetAndShowItems(folderToDownload);

		self.storageHelper.CreateDirectory( downloadPath);

		allItems = self.Apply( items, self.DownloadItem);
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
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
		items = [];
		for item in collection:
			newStorageItem = SH.AccessStorageItem(self.fVerbose);
			newStorageItem.name 	= item["path"];
			newStorageItem.path 	= item["path"];
			newStorageItem.num_bytes= item["bytes"];
			newStorageItem.is_dir	= item["is_dir"];
			newStorageItem.modified_date = item["modified"];
			newStorageItem.revision	= item["rev"];
			items.append( newStorageItem);

		return items;

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

		subFoldersList = [item for item in subItemsStart if item.isFolder()];

		numItems = len(subItemsStart);
		numFolders = len(subFoldersList);
		numFiles = numItems - numFolders;

		if (self.fVerbose):
			print("\t ---- Folder {:30s} has {:,d} folders and {:,d} files"
				.format( path, numFolders, numItems));

		if ( goDeep ):
			for folder in subFoldersList:
				if (self.fVerbose):
					print("\n --- Enumerating Folder {:30s}".format( folder.path));
				subItems = self.GetCollection( folder.path);
				numInFolder = len(subItems);
				allItems.extend( subItems);

				numItems += numInFolder;
				foldersHere = [folder for folder in subItems if  folder.path];
				numFoldersHere = len(foldersHere);
				numFilesHere = numInFolder - numFoldersHere;

				numFolders += numFoldersHere;
				numFiles += numFilesHere;
				if (self.fVerbose):
					print("\t ---- Folder {:30s} has {:,d} folders and {:,d} files"
						.format(  folder.path, numFoldersHere, numFilesHere)); 

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

			outputFileName = destRoot +  item.path;
			if ( item.isFolder()):
				self.storageHelper.CreateDirectory( outputFileName);
			else:
				toDownload = self.storageHelper.IsDownloadRequired( item.path, item.num_bytes, outputFileName);

				if ( toDownload):
					print( u"Downloading {:15s} {:15,d} {:40s} "
						.format( item.revision, item.num_bytes, item.path
						));
					self._downloadFile( item.path, outputFileName);

			savedList = [ outputFileName];

		return savedList;

	def DeleteItems( self, folderToDelete, deleteRoot = u"."):
		"""
			Delete items from Dropbox after confirming that 
				it is locally available
				and local copy is same as Cloud copy
		"""
		print("\n--------------------------------------------------------")
		print(" Deleting files for folder \"{}\"".format( folderToDelete));
		print("--------------------------------------------------------")
		allItems = self.GetAndShowItems(folderToDelete);

		confirmForAll = raw_input("Confirm delete for ALL Files? Y/N: ")
		allItemsConfirmed = 0;
		if (confirmForAll == 'Y'):
			print(" You confirmed delete for ALL files here. No more detailed confirmation.");
			allItemsConfirmed = 1;

		numFilesDeleted = 0;
		numBytesDeleted = 0;
		numFolders = 0;

		# Now let us check and delete each item and save it away
		for item in allItems:
				localFileName = deleteRoot + item.path;
				toDownload = self.storageHelper.IsDownloadRequired( item.path, item.num_bytes, localFileName);

				if ( toDownload):
					print( u"Download Required {:40s} {:15s} {:15,d}"
						.format( item.path, item.revision, item.num_bytes
						));
				else:
					print( u"******** Ready to delete : {:40s} {:15s} {:15,d}"
						.format( item.path, item.revision, item.num_bytes));

					confirmForItem = allItemsConfirmed;
					if (confirmForItem == 0):
						confirm = raw_input("Confirm delete? Y/N: ")
						if (confirm == "Y"):
							confirmForItem = 1;

					if (confirmForItem == 1):
						self.client.file_delete( item.path);
						print( u"\t{:5,d}. Deleted file : {:s}".format( numFilesDeleted, item.path));
						numFilesDeleted += 1;
						numBytesDeleted += item["bytes"];

		print("\n Total of {:,d} files. Deleted {:,d} files of size {:,d} bytes"
			.format( len(allItems), numFilesDeleted, numBytesDeleted));
		print("\t Skipped {:,d} files".format( len(allItems) - numFilesDeleted));
		print("\t Skipped {:,d} folders".format( numFolders));

		return allItems;

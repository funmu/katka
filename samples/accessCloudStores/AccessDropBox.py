#!/usr/bin/python

"""
	Class and helpers to handle Dropbox related content


	Dependencies
	-  DropBox SDK installed using
		pip install dropbox
	- Dropbox SDK updated from v1 API to v2 in July 2017. 
		https://blogs.dropbox.com/developers/2016/06/api-v1-deprecated/
	- accordingly I am updating the code in Sep 2018.
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
		self.client = dropbox.Dropbox(access_token)
		if (self.fVerbose):
			print( "\t  d.Complete the authentication process");
			print( self.client);		
			print('linked account: ', self.client.users_get_current_account());
		return;

	def GetCollection( self, folderPath):
		"""
			Get the files and folders at the 'folderPath'
		"""
		if (self.fVerbose):
			print( "\t  Getting metadata for folder: {}".format( folderPath));

		# list files in the root directory
		# for entry in dbx.files_list_folder('').entries:
    	#	print(entry.name)

		folder_metadata = self.client.files_list_folder(folderPath);

		# print 'metadata: ', folder_metadata
		print( folder_metadata);
		collection = folder_metadata.entries;
		print(collection);
		items = [];
 		for item in collection:
			newStorageItem = SH.AccessStorageItem(self.fVerbose);
			newStorageItem.name 	= item.name;
			newStorageItem.path 	= item.path_lower;
			if (isinstance( item, dropbox.files.FolderMetadata) ):
				newStorageItem.num_bytes= 0;
				newStorageItem.is_dir = 1;
			elif (isinstance( item, dropbox.files.FileMetadata) ):
				newStorageItem.num_bytes= item.size;
				newStorageItem.is_dir = 0;
				newStorageItem.modified_date = item.server_modified;
				newStorageItem.revision	= item.rev;
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
			print("\t ---- Folder \"{:30s}\" has {:,d} folders and {:,d} files"
				.format( path, numFolders, numFiles));

		if ( goDeep ):
			for folder in subFoldersList:
				if (self.fVerbose):
					print("\n --- Enumerating Folder {:30s}".format( folder.path));
				subItemsStart = self.GetAndShowItems( folder.path, goDeep);

				subsubFoldersList = [item for item in subItemsStart if item.isFolder()];
				inumItems = len(subItemsStart);
				inumFolders = len(subsubFoldersList);
				inumFiles = numItems - numFolders;
				allItems.extend( subItemsStart);
		
				if (self.fVerbose):
					print("\t   ####  Folder \"{:30s}\" has {:,d} folders and {:,d} files"
						.format( folder.path, inumFolders, inumFiles));
				numFiles += inumFiles;
				numItems += inumItems;
				numFolders += inumFolders;

		print( "\n{:10d} items: {:10d} folders and {:10d} items in \"{:30s}\"\n"
			.format( numItems, numFolders, numFiles, path));
		return allItems;


	def _downloadFile_v1( self, item, outputFileName):
		print( u" .... about to download file {:30s} to {:40s}"
			.format( item.path, outputFileName));
		f = self.client.get_file( item.path);
		out = open( outputFileName, 'wb');
		out.write(f.read());
		out.close();
		return;

	def _downloadFile( self, item, outputFileName):
		print( u" .... about to download file {:30s} to {:40s}"
			.format( item.path, outputFileName));
		self.client.files_download_to_file( outputFileName, item.path, item.revision);
		return;


	def DownloadItem( self, item, destRoot = u"."):
		"""
			Download the items locally within the destination root path given

		"""
		savedList = [];
		downloadInfo = { "folder": 0, "file": 0, "bytes": 0, "skipped" : 0 }		

		if (item is None):
			print(" No item was found");
		else:

			outputFileName = destRoot +  item.path;
			if ( item.isFolder()):
				self.storageHelper.CreateDirectory( outputFileName);
				downloadInfo["folder"] += 1;								
			else:
				toDownload = self.storageHelper.IsDownloadRequired( item.path, item.num_bytes, outputFileName);

				if ( toDownload):
					print( u"Downloading {:15s} {:15,d} {:40s} "
						.format( item.revision, item.num_bytes, item.path
						));
					if (not self._downloadFile( item, outputFileName)):
						downloadInfo["skipped"]	= 1;
					downloadInfo["bytes"] = item.num_bytes;
					downloadInfo["file"] = 1;
				else:
					downloadInfo["skipped"]	= 1;

			savedList = [ outputFileName];

		# return savedList;
		return [downloadInfo];

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

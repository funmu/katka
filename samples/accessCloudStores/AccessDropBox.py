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
import os; # for file access

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AccessDropBox:
	"""
		Class to access Dropbox account to list and download files.
	"""

	fVerbose = 0;
	client = None;	
	idPathDirectory = {};

	def __init__(self, verbose):
		self.fVerbose = verbose;

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
		basecount = 0;
		while (not items is None):
			count = 1;
			for count, item in enumerate( items):
				if (printItem):
					self._printItem( basecount+count + 1, item);
				itemList.append( item);

			basecount = basecount + len(items);

			# ToDo: How does pagination work in Dropbox?
			#get the next page of three elements, if none exist, returns None
			# items = None if items.next_page_request is None else items.next_page_request.get();
			# print( "\t .... fetched {} items".format( basecount));
			items = None;

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
			print( "{:10d} items had {:10d} folders".format(numItems, numFolders));

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
					print("\t ---- Folder {:30s} has {:,d} items"
						.format( folder["path"], numInFolder)); 

		print( "\nTotal of {:10d} items: {:10d} folders and {:10d} items\n"
			.format(numItems, numFolders, numFiles));
		return allItems;

	def DownloadItem( self, item):
		if (item is None):
			print(" No item was found");
		else:
			print( u"Downloading {:15s} {:15s} {:40s} "
				.format( item["rev"], 
					"Folder" if self.isFolder(item) else item["size"],
					item["path"]
				));

		outputFileName = u"." + item["path"];
		if ( self.isFolder( item)):
			print( u"\t Creating the directory {}".format(outputFileName));
			try:
				os.makedirs( outputFileName);
			except:
				print( "Directory possibly exists ... skipping");
		else:
			f = self.client.get_file( item["path"]);
			print( u"Donwload file {:30s} to {:40s}"
				.format( item["path"], outputFileName));
			out = open( outputFileName, 'wb')
			out.write(f.read())
			out.close()

		savedList = [ outputFileName];
		return savedList;

	def SampleCode(self):

		f = open('working-draft.txt', 'rb')
		response = client.put_file('/magnum-opus.txt', f)
		print 'uploaded: ', response

		f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
		out = open('magnum-opus.txt', 'wb')
		out.write(f.read())
		out.close()
		print metadata


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

	def printItemWithPath( self, index, item, itemPath = None):
		if (item is None):
			print(" No item was found");
		else:
			if (itemPath is None):
				itemFullName = item.name if item.folder is None else "/"+item.name;
			else:
				itemFullName = itemPath;

			print("{:4d}. {:10s} \"{:30s}\"".format( index, item["rev"], itemFullName));


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
		allItems = [];
		for item in list:
			foundItems = applyFunction( item);
			allItems.extend( foundItems);
		return allItems;

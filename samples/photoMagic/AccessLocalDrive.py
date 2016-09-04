#!/usr/bin/python

#
#  AccessLocalDrive.py 
#  -- Class for handling LocalDrive related access
#
#  Dependencies
#   -  OneDriveSDK
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = 'Murali Krishnan'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
import StorageHelper as SH;
import os;
import time;
import hashlib;


def printSeparator():
	print( "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	AccessOneDrive - Class to access and use OneDrive
class AccessLocalDrive:

	fVerbose = 0;
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

	def Connect( self, connectOptions):

		print( "\t  a. Creating a connection to local drive");
		# Nothing required to connect to local drive yet.

		print( "\t  e. Load up the children for root node after connection");
		# None right now
		return;

	def PrintItem( self, index, item):
		if (item is None):
			print(" No item was found");
		else:
			itemFullName = item.name if item.folder is None else "/"+item.name;
			print("{:3} {:10} {:10} \"{:30}\" {:10}"
				.format( '' if index == 0 else index, 
						item.id, item.folder,
						itemFullName, item.size));


	def _AddNewItem( self, dirPath, fileName, isDir = 0):
		newStorageItem = SH.AccessStorageItem( self.fVerbose);
		newStorageItem.name 	= fileName
		newStorageItem.id 		= "None";
		newStorageItem.path 	= os.path.join( dirPath, fileName);

		try:
			localFileInfo = os.stat( newStorageItem.path);
			if ( not isDir):
				newStorageItem.itemHash = \
					hashlib.sha256( open(newStorageItem.path, 'rb').read()).digest();

		except:
			print( u"\n Couldn't get stat for file {}"
				.format( newStorageItem.path));

		newStorageItem.num_bytes= localFileInfo.st_size;
		newStorageItem.is_dir	= isDir;
		newStorageItem.modified_date = time.ctime(localFileInfo.st_mtime);
		newStorageItem.revision	= "NoRevision";

		if (self.fVerbose):
			print( "\n\t add new item {0} at path = {1}"
				.format( newStorageItem.id, newStorageItem.path));
			newStorageItem.PrintItem(0);
		return newStorageItem;

	def GetItemForPath( self, itemPath):

		if (self.fVerbose): 
			printSeparator();
			print( "\t Accessing items using the path supplied = {0}"
				.format( itemPath));

		childItems = [];
		parentItem = None;

		if ( not self.idPathDirectory.has_key( itemPath)):
			# Enumerate through the directory to fetch items
			for cur, _dirs, _files in os.walk( itemPath):
				for dirItem in _dirs:
					childItems.append( self._AddNewItem( cur, dirItem, 1));
				for fileItem in _files:
					childItems.append( self._AddNewItem( cur, fileItem));
				for dirItem in _dirs:
					subDirItems = self.GetItemForPath( os.path.join( cur, dirItem));
					childItems.extend( subDirItems);

			# Add this parent item here ... 
			parentItem = self._AddNewItem( itemPath, "");
			parentItem.children = childItems;
			self.idPathDirectory[ itemPath] = parentItem;
		else:
			parentItem = self.idPathDirectory[ itemPath];

		if (self.fVerbose):
			print("~~~~~~~ GOT ITEM for path {}".format(itemPath));
			parentItem.PrintItem( 0);

		return parentItem;

	def GetAndShowItems( self, path):
		print("---------------------------------------------------------------");
		print(" Enumerating items in folder \"{}\"".format( path));
		item = self.GetItemForPath( path);

		allItems = [item] if (item.children is None) else item.children;
		return allItems;


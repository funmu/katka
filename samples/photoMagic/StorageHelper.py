#!/usr/bin/python

"""
	Class and helpers to handle Storage Access


	Dependencies
"""
__author__ = 'Murali Krishnan'
__version__ = "v1.0.0"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Import Section
import os; # for file access
from stat import *; # for file details

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Helper Classes for managing an Item
class AccessStorageItem:
	"""
		Individual unit of storage used in various functions
	"""

	verbose = 0;

	id 		= None;
	name 	= None;
	path 	= None;
	num_bytes = 0;
	is_dir	= False;
	modified_date = None;
	revision	= None;
	children	= None;
	itemHash	= 0;

	def __init__(self, verbose):
		self.fVerbose = verbose;

	def isFolder(self):
		"""
			Check if the given item is a folder
		"""
		return ( self.is_dir);

	def PrintItem( self, index = 0):
		print( u"{0:4d}. {1:6s} {2:12,d} [{3}] {4:60s}\n\t{5:s}\n"
			.format( index,
				"Folder" if self.is_dir else '',
				self.num_bytes if self.num_bytes else 0,
				self.modified_date,
				self.path,
				self.itemHash.encode('hex')
			));
		if (self.children):
			print("\tNumChildren: {:,d}".format( len(self.children)));

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Helper Classes for Cloud Storage Access
class AccessStorageHelper:

	fVerbose = 0;

	def __init__(self, verbose):
		self.fVerbose = verbose;

	def CreateDirectory( self, outputFolderName):
		createdDir = None;
		try:
			if (not os.path.exists( outputFolderName)):
				createdDir = os.makedirs( outputFolderName);

			print( u"\t Creating the directory {}".format(outputFolderName));
		except:
			print("\t Skipping Directory (possibly it exists): {}".format( outputFolderName));

		return createdDir;


	def IsDownloadRequired( self, itemPath, itemSize, localFileName):
		toDownload = 0;
		try:
			localFileInfo = os.stat( localFileName);
			toDownload = (localFileInfo.st_size != itemSize);
			if (self.fVerbose):
				print( u"\n Cloud File: {} at {:,d} bytes. \n Local File:{} at {:,d} bytes"
					.format( itemPath, itemSize, localFileName, localFileInfo.st_size));
			if ( toDownload == 0):
				print( u"\t SAME File: {}".format( itemPath));
		except:
			print( u"\n Couldn't get stat for file {}"
				.format( localFileName));
			toDownload = 1;

		return toDownload;

	def DownloadItems( self, foldersToDownload, getItemsFunc, downloadItemsFunc, downloadPath = u"."):
		print("\n--------------------------------------------------------")
		print(" Downloading files for folder \"{}\"".format( foldersToDownload));
		print("--------------------------------------------------------")

		self.CreateDirectory( downloadPath);
		items = self.Apply( foldersToDownload, getItemsFunc);

		for folder in foldersToDownload:
			outputFolder = downloadPath +  folder;
			self.CreateDirectory( outputFolder);

		print("\nBegin Downloading files ...\n");
		downloadItemsFuncWithPath = lambda x: downloadItemsFunc(x, downloadPath);
		downloadedStats = self.Apply( items, downloadItemsFuncWithPath);

		downloadInfo = { "folder": 0, "file": 0, "bytes": 0, "skipped": 0 }

		for stat in downloadedStats:
			downloadInfo["folder"] 	+= stat["folder"];
			downloadInfo["file"] 	+= stat["file"];
			downloadInfo["bytes"] 	+= stat["bytes"];
			downloadInfo["skipped"]	+= stat["skipped"];
		print("\n Total of {:,d} files downloaded of size {:,d} bytes."
			.format( downloadInfo["file"], downloadInfo["bytes"]));
		print("\t Skipped {:,d} files".format( downloadInfo["skipped"]));
		print("\t Skipped {:,d} folders".format( downloadInfo["folder"]));

		return downloadInfo;


	def DeleteItems( self, foldersToDelete, getItemsFunc, deleteItemsFunc, downloadPath = u"."):
		"""
			Delete items from after confirming that 
				it is locally available
				and local copy is same as Cloud copy
		"""
		print("\n--------------------------------------------------------")
		print(" Deleting files for folder \"{}\"".format( foldersToDelete));
		print("--------------------------------------------------------")
		self.CreateDirectory( downloadPath);
		items = self.Apply( foldersToDelete, getItemsFunc);

		for folder in foldersToDelete:
			outputFolder = downloadPath +  folder;
			self.CreateDirectory( outputFolder);

		confirmForAll = raw_input("Confirm delete for ALL Files? Y/N: ")
		allItemsConfirmed = 0;
		if (confirmForAll == 'Y'):
			print(" You confirmed delete for ALL files here. No more detailed confirmation.");
			allItemsConfirmed = 1;

		print("\nBegin Check and Delete files ...\n");
		deleteItemsFuncWithPath = lambda x: deleteItemsFunc(x, allItemsConfirmed, downloadPath);
		deleteStats = self.Apply( items, deleteItemsFuncWithPath);

		deleteInfo = { "folder": 0, "file": 0, "bytes": 0, "download": 0 }

		for stat in deleteStats:
			deleteInfo["folder"] 	+= stat["folder"];
			deleteInfo["file"] 		+= stat["file"];
			deleteInfo["bytes"] 	+= stat["bytes"];		
			deleteInfo["download"] 	+= stat["download"];		
		print("\n Total of {:,d} files deleted. Downloaded {:,d} files of size {:,d} bytes"
			.format( deleteInfo["file"], deleteInfo["download"], deleteInfo["bytes"]));
		print("\t Skipped {:,d} files".format( len(items) - deleteInfo["file"]));
		print("\t Skipped {:,d} folders".format( deleteInfo["folder"]));

		return deleteInfo;

	def PrintItems( self, items):
		print("\n\n-------------------------------------------");
		for count, item in enumerate( items):
			item.PrintItem( count);
		print("\n-------------------------------------------");
		print(" Total of {:,d} items \n".format( len(items)));

	def Apply( self, list, applyFunction):
		allItems = [];
		for item in list:
			foundItems = applyFunction( item);
			allItems.extend( foundItems);
		return allItems;


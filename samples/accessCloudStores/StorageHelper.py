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

	def __init__(self, verbose):
		self.fVerbose = verbose;

	def isFolder(self):
		"""
			Check if the given item is a folder
		"""
		return ( self.is_dir);

	def PrintItem( self, index = 0):
		print( u"{0:4d}. {1:10s} {2:15,d}  {3:40s} {4} {5:15s}"
			.format( index,
				"Folder" if self.is_dir else '',
				self.num_bytes if self.num_bytes else 0,
				self.path,
				self.modified_date,
				self.revision
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
		downloadedItems = self.Apply( items, downloadItemsFuncWithPath);
		return downloadedItems;

	def PrintItems( self, items):
		print("\n\n-------------------------------------------");
		count = 1;
		for count, item in enumerate( items):
			item.PrintItem( count);

	def Apply( self, list, applyFunction):
		allItems = [];
		for item in list:
			foundItems = applyFunction( item);
			allItems.extend( foundItems);
		return allItems;


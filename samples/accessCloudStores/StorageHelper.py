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

	name 	= None;
	path 	= None;
	num_bytes = 0;
	is_dir	= False;
	modified_date = None;
	revision	= None;

	def __init__(self, verbose):
		self.fVerbose = verbose;

	def isFolder(self, item):
		"""
			Check if the given item is a folder
		"""
		return ( self.is_dir);


_sampleDropBoxData = {
    'bytes': 77,
    'icon': 'page_white_text',
    'is_dir': False,
    'mime_type': 'text/plain',
    'modified': 'Wed, 20 Jul 2011 22:04:50 +0000',
    'path': '/magnum-opus.txt',
    'rev': '362e2029684fe',
    'revision': 221922,
    'root': 'dropbox',
    'size': '77 bytes',
    'thumb_exists': False
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Helper Classes for Cloud Storage Access
class AccessStorageHelper:

	fVerbose = 0;

	def __init__(self, verbose):
		print("Initialized Storage Helper object");
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

	def PrintItems( self, items, printItemFunction):
		count = 1;
		for count, item in enumerate( items):
			printItemFunction( count, item);

	def Apply( self, list, applyFunction):
		allItems = [];
		for item in list:
			foundItems = applyFunction( item);
			allItems.extend( foundItems);
		return allItems;


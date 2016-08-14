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
				print( u"\t skipping file: {}".format( itemPath));
		except:
			print( u"\n Couldn't get stat for file {}"
				.format( localFileName));
			toDownload = 1;

		return toDownload;


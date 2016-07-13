#!/usr/bin/python

#
# ------ script to access One Drive Files
#


import onedrivesdk;
from onedrivesdk.helpers import GetAuthCodeServer;
from PIL import Image
import os


class AccessOneDrive:

	fVerbpse = 0;
	client = None;	
	idPathDirectory = {};

	def __init__(self, verbose):
		self.fVerbose = verbose;

	def Connect( self, clientId, redirectUri, clientSecret):

		print( "\t  a.Creating a client object");
		self.client = onedrivesdk.get_default_client(client_id=clientId,
		                                        scopes=[
		                                        # 'wl.signin',
		                                         #       'wl.offline_access',
#		                                                "offline_access",
		                                                'onedrive.readwrite'])

		print( "\t  b.Getting an authorization URL");
		auth_url = self.client.auth_provider.get_auth_url(redirectUri);
		# print( auth_url);

		#this will block until we have the code

		print( "\t  c.Getting the Auth code");
		code = GetAuthCodeServer.get_auth_code(auth_url, redirectUri);
		# print(code);

		print( "\t  d.Complete the authentication process");
		self.client.auth_provider.authenticate(code, redirectUri, clientSecret);
		# print("\t authentication complete ...");
		return;

	def GetCollection( self, topNLevels):
		#get the top three elements of root, leaving the next page for more elements
		collection = self.client.item(drive="me", id="root").children.request(top = topNLevels).get();
		return collection;

		#get the first item in the collection
		item = collection[0];

		#get the next page of three elements, if none exist, returns None
		collection2 = collection.next_page_request.get();

	def _printItem( self, index, item):
		if (item is None):
			print(" No item was found");
		else:
			itemFullName = item.name if item.folder is None else "/"+item.name;
			print("{} {} \"{:30}\" {:,d}".format( '' if index == 0 else index, item.id, itemFullName, item.size));

	def printItemWithPath( self, index, item, itemPath = None):
		if (item is None):
			print(" No item was found");
		else:
			if (itemPath is None):
				itemFullName = item.name if item.folder is None else "/"+item.name;
			else:
				itemFullName = itemPath;

			print("{} {} \"{}\"".format( '' if index == 0 else index, item.id, itemFullName));

	def ListItems( self, items, printItem = 1):
		itemList = [];
		basecount = 1;
		while (not items is None):
			count = 0;
			for count, item in enumerate( items):
				if (printItem):
					self._printItem( basecount+count, item);
				itemList.append( item);
			items = None if items.next_page_request is None else items.next_page_request.get();
			basecount = basecount + count;
			print( "\t .... fetched {} items".format( basecount));
		return itemList;

	def GetItemsForId( self, itemId):
		if (self.fVerbose):
			print( "\n Accessing items for itemID = {0}".format( itemId));
		return self.client.item( id=itemId).children.request(top=100).get();

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

	def GetAndShowItems( self, path):
		print("\n--------------------------------------------------------")
		item = self.GetItemForPath( path);
		self.printItemWithPath( 0, item, path);

		subItemsStart = self.GetItemsForId( item.id);
		allItems = self.ListItems( subItemsStart);
		return allItems;

	def DownloadItems( self, path):
		print("\n--------------------------------------------------------")
		item = self.GetItemForPath( path);
		self.printItemWithPath( 0, item, path);

		subItemsStart = self.GetItemsForId( item.id);
		allItems = self.ListItems( subItemsStart, 0);

		parentPathEndsAt = path.rfind( '/');
		downloadPath = path[parentPathEndsAt+1:] + "/";
		if (not os.path.exists( downloadPath)):
			print("\t Creating the directory {}".format(downloadPath));
			os.makedirs( downloadPath);

		# Now let us really download each item and save it away
		for item in allItems:
			print( "Downloading \"{:40}\" Id={} size: {:,d}".format( item.name, item.id, item.size));
			fileName = downloadPath + item.name;
			if ( os.path.isfile( fileName) and (os.path.getsize( fileName) == item.size)):
				print("\tskipping same sized file");
			else:
				self.client.item( id = item.id).content.request().download( fileName);

		return allItems;


import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("myConfig.ini");
print Config.sections();

client_id = Config.get("HotmailAccount", "AppId");
client_secret =  Config.get("HotmailAccount", "AppSecret");
redirect_uri = Config.get("HotmailAccount", "WebRedirectUri");

# mobile Redirect URI does not work ... troubleshoot later.
# redirect_uri = mobile_redirect_uri;


print("\n1. Creating the Object to access One Drive");
aod = AccessOneDrive( 0);

print( "\n2. Getting connected to One Drive using my ID and secret");
aod.Connect( client_id, redirect_uri, client_secret);

# print( "\n3. Get Collections and print these out");
# coll = aod.GetCollection( 3);
# print coll;

# print("\n4. Enumerating list of items at the root");
# items = aod.GetItemsForId( "root");
# aod.ListItems(items);

# aod.ListItems( "2B25A513D5D15C04!133776");

print( "\n5. Enumerating items in a given path");
aod.GetAndShowItems( "/Public/Pictures");

aod.GetAndShowItems( "/Public/Pictures/FamilyPics");

# aod.GetAndShowItems(  "/Public/Pictures/SkyDrive camera roll");

print( "\n6. Download an Item");
IdForOviyaAug24_12_jpg = "2B25A513D5D15C04!133806"
item = aod.client.item( id = IdForOviyaAug24_12_jpg).content.request().download( "test.jpg");
print(item);

aod.DownloadItems( "/Public/Pictures/FamilyPics");

aod.DownloadItems( "/Public/Pictures/SkyDrive camera roll");

# test_dropbox_v2.py
#	Code to minimally test Dropbox V2 API
#	Created: Sep 2018
#
#	- Dropbox SDK updated from v1 API to v2 in July 2017. 
#		https://blogs.dropbox.com/developers/2016/06/api-v1-deprecated/
#
import dropbox;

ACCESS_KEY="PUT_ACCESS_KEY_HERE";

def printEntries( entries):	
	for entry in entries:
		print( entry);
		if ( isinstance( entry, dropbox.files.FolderMetadata)):
			print( "------- this is a folder");
		elif (isinstance( entry, dropbox.files.FileMetadata)):
			print( "******* this is a FILE");
	print("\n -------");

def main():
	dbx = dropbox.Dropbox( ACCESS_KEY);
	folderpath = '/invoices';
	folderpath = '/invoices/draw #8 - hemo';
	printEntries( dbx.files_list_folder(folderpath).entries);

if __name__ == '__main__':
    main()

FolderMetadata(name=u'Budget Summaries', 
 	id=u'id:cFIRWo3Iz7AAAAAAAAAAAQ', 
 	path_lower=u'/invoices/budget summaries', 
 	path_display=u'/Invoices/Budget Summaries', 
 	parent_shared_folder_id=None, 
 	shared_folder_id=None, 
 	sharing_info=None, 
 	property_groups=None)
 	

FileMetadata(name=u'Hemocoel budget Summary bottom line to draw #14.pdf', 
	id=u'id:HKZphOMe9H0AAAAAAAAD-Q', 
	client_modified=datetime.datetime(2013, 7, 8, 4, 29, 44), 
	server_modified=datetime.datetime(2016, 7, 18, 13, 33, 48), 
	rev=u'9501204f88f', size=87266, 
	path_lower=u'/invoices/budget summaries/hemocoel budget summary bottom line to draw #14.pdf', 
	path_display=u'/Invoices/Budget Summaries/Hemocoel budget Summary bottom line to draw #14.pdf', 
	parent_shared_folder_id=None, media_info=None, sharing_info=None, 
	property_groups=None, has_explicit_shared_members=None)
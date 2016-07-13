#!/usr/bin/python
# configParser Example

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("myConfig.ini");
print Config.sections();

print Config.get("HotmailAccount", "Description");
print Config.get("HotmailAccount", "Name");
print Config.get("HotmailAccount", "AppSecret");
print Config.get("HotmailAccount", "AppId");
print Config.get("HotmailAccount", "WebRedirectUri");
print Config.get("HotmailAccount", "MobileRedirectUri");

folders = Config.get("HotmailAccount", "FoldersToDownload");
folderList = folders.split('\n');
print len( folderList);

for item in folderList:
	print item;

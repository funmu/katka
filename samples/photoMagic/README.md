# PhotoMagic - View and Manage Photos

PhotoMagic will help me manage photos with least overhead.


##Problem##
There are lots of photos in my drives. It is time to have a simple way to view and manage these pictures. Most of the vendor programs are optimized for viewing and often fail when you are dealing with 1000s of pictures. I need a robust and simple way to programmatically manage photos.


##Solution Approach##

 Use custom built python code to enumerate and programmatically proces photos.

A separate configuration file is required to specify account details. For security reasons, the exact configuration file is not stored here. 

A simple class is provided for listing, differencing, and processing the photos files.



## Relevant Bash Shell Scripts

### Enumerate all files in a folder
 - list all files using the 'a' option
 - list in long format using the 'l' option
 - list all files recursively including sub-folders using the 'R' option

```
	ls -laR ~ | tee ~/log.allFiles.txt
```

### Enumerate using Find

Find all files of type 'f' such that the file size is larger than specified MAX_FILE_SIZE
Print only the size field and name field to start with.

```
	MAX_FILE_SIZE=+100000k 

	find . -type f -size $MAX_FILE_SIZE -exec ls -lh {} \; | awk '{ print $5 " : " $9 }' | tee ~/log.allBigFiles.txt

```

### Compact large Github Pack files

Go to the git repository of interest and do this ... 
```
	git gc --aggressive --prune=now
```



##Code##
 * [photoMagic.py](photoMagic.py) - scripts for accessing local storage files
 * [class AccessLocalDrive](AccessLocalDrive.py) - helper class for accessing local files
 * [class StorageHelper](StorageHelper.py) - helper class for storage related access
 

###Wish List###
 * Logging - write out log to a separate file for analysis.
 * Do hash based clsutering of identical items
 * Generate execution script for handling photo magic operations

##Contributors##
Murali Krishnan


# RandomMoviePicker

Little python script that allows you to start a random movie in a folder with alot of movies.

## DONE

this script will work in any folder which has .mp4 files. these files may be in a folder in the folder you run the script in. 
This program will find it.

## EXPECTED CRASHES

if you don't have any .mp4 files in the folder you run this script in, this will crash.
If there is a file in the folder that isn't a .mp4 file and doesn't contain "." but isn't a folder. This script will see it as a folder
and try to run it as a Folder. this will give the exception path not found.

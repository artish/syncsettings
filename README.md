Setup Settings Python Script
============================

This script will synchronize settings of all your apps in git repository.

Not only will this secure this your app settings, it will also prevent nasty duplication synchronisation errors when synching settings via Dropbox for instance.

## TODO:

  + Move the Settings into their own Repository away from the script

  + Add a setting where the symlink are added to a folder    
    Example in the After Effects Folder, where you already have a ton of preinstalled plugins and want to add onto these folders.
    `/Applications/Adobe\ After\ Effects\ CC\ 2014/Plug-ins`

  + Check if additional variables like "title" are given.     
    But don't require them like now

  + Automatically get the folder of the the sync_settings json.

  + Add Copy function for files that can't be symlinked

  + Ignore Symlinks where the parent folder doesn't exist

## Code TODO:

  + TODO 001: Remove this unecessary if condition

  + TODO 002: Replace this with a walk function



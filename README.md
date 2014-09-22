Setup Settings Python Script
============================

This script will synchronize settings of all your apps in git repository.

Not only will this secure this your app settings, it will also prevent nasty duplication synchronisation errors when synching settings via Dropbox for instance.

## VirtualEnv Instructions

### Installation & Fix:

  1. Fix & Reinstall Python with brew
     [osx - Homebrew , python installing - Stack Overflow](http://stackoverflow.com/questions/13088998/homebrew-python-installing)

  2. Install Python Environment    
     [Python Development Environment on Mac OS X Mavericks 10.9 | Hacker Codex](http://hackercodex.com/guide/python-development-environment-on-mac-osx/)

### Setup:

  1. Set up the virtual environment:    

    ```shell
    virtualenv virtpy
    ```

  2. Activate the virtual environment:

    ```shell
    . sync/bin/activate
    ```
    
    To deactivate just run:    

    ```shell
    deactivate
    ```

  3. Install in the current pip    

    \-\-editable makes sure the setup.py uses the current files and doesn't copies and duplicates all the working files.

    ```shell
    pip install --editable .
    ```


### Requirements

#### Load Requirements:
  
  ```shell
  pip install -r ./requirements.txt
  ```
  
#### Freeze Requirements:

  ```shell
  pip freeze -l > ./requirements.txt 
  ```

## TODO:

  + Check if additional variables like "title" are given.     
    But don't require them like now

  + Add Copy function for files that can't be symlinked

  + Add a setting where the symlink are added to a folder    
    Example in the After Effects Folder, where you already have a ton of preinstalled plugins and want to add onto these folders.
    `/Applications/Adobe\ After\ Effects\ CC\ 2014/Plug-ins`
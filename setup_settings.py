#!/usr/bin/python
# 
# Setup Settings
#
#==============================================================================#
# Imports
#==============================================================================#

# System Modules
import os
import sys
import glob
import json
from pprint import pprint

# Custom Modules
from lib.send2trash import send2trash # https://github.com/hsoft/send2trash

#==============================================================================#
# Global Variables
#==============================================================================#

mode = ""

# Name of the settings file
cfg_file = "sync_settings.json"

#==============================================================================#
# Functions
#==============================================================================#

# symlink(current directory, symlink source folder, symlink destination folder )
# Creates a symlink from a file/path to a give path
def symlink(cur, json, src, dst, title, overwrite_all=None):

  abpath = os.path.dirname(json)
  # print src
  # print cur
  # print abpath

  abpath = abpath.replace(cur, '')
  print abpath

  print 
  return

  if (title): 
    print title

  # Expand the paths to the current user
  dst = os.path.expanduser(dst)
  src = os.path.join(cur, src)

  # If the target is an existing file or folder
  # Ask to overwrite it or to skip it
  if any( [os.path.isfile(dst), os.path.isdir(dst), os.path.islink(dst) ] ):

    # When overwrite_all is "y" or in testing mode
    # Overwrite the file
    if any ( [overwrite_all, mode == "test"] ):

      overwrite_all = 1

    else: 

      print "File " + dst + " already exists."
      
      # Check the prompt value for
      #
      # a: Overwrite all files and don't ask anymore if files should be overwritten
      # y: Continue the function and overwrite
      # n: Exit the function and don't overwrite
      #
      # On any other input repeat the prompt
      
      prompt = ""
      
      while all ([
                   prompt != "y", 
                   prompt != "n", 
                   prompt != "a"
                  ]):
        prompt = raw_input("Overwrite (y/n/a): ")

      if (prompt == "a"):
        overwrite_all = 1 # Overwrite All
      elif (prompt == "n"):
        return # Exit
      elif (prompt == "y"):
        pass # Overwrite only this file

  # Trash the resulting destination file or dir
  # And delete symlinks so they don't crowd the trashbin
  if (os.path.islink(dst)):
    os.unlink(dst)
  else: 
    send2trash(dst)

  # Create the symlink
  os.symlink(src, dst)

  # Print the symlink creation information
  print "Creating SymLink: "
  print "  Src: " + src
  print "  Dst: " + dst + "\n"

  return overwrite_all

#==============================================================================#
# Main
#==============================================================================#

def main(argv=None):

  #----------------------------------------------------------------------------#
  # Variables
  #----------------------------------------------------------------------------#

  # If this is true all existing files will be overwriteen
  overwrite_all = 0

  # Path with the settings
  settings_dir = "~/Settings"
  settings_dir = os.path.expanduser(settings_dir)
  
  # Check if there is either a symlink or a dir ~/Settings
  # After that check if there is a Settings dir in the parent dir of the script
  # If none of these exist, exit the script
  if (os.path.islink(settings_dir)):
    settings_dir = (os.path.realpath(os.path.expanduser(settings_dir))) # Expand the user and find the symlink target path
  elif (os.path.isdir(settings_dir)):
    settings_dir = (os.path.expanduser(settings_dir)) # Expand the user and find the symlink target path
  else:
    print "No Settings folder found in either ~/ or the script dir!"
    return

  # Get all sync setting files
  cfg  = glob.glob(settings_dir + '*/' + cfg_file)
  cfg += glob.glob(settings_dir + '*/*/' + cfg_file)
  cfg += glob.glob(settings_dir + '*/*/*/' + cfg_file)

  # If there aren't any config files exit the script
  if not(cfg):
    print ("No %s files found!" % cfg_file)
    return

  #----------------------------------------------------------------------------#
  # Symlink Iteration
  #----------------------------------------------------------------------------#

  # Loop through the configuration files and create the symlinks
  for x in cfg:

    # Load the data from the json files into data
    json_data = open(x)
    data = json.load(json_data)
    json_data.close()

    for d in data["symlink"]:
      overwrite_all = symlink(settings_dir, x, d["src"], d["dst"], d["title"], overwrite_all)

# Advanced main function call
# http://www.artima.com/weblogs/viewpost.jsp?thread=4829
if __name__ == "__main__":
  sys.exit(main())
  pass
#!/usr/bin/python
#
# Setup Settings
#
#=============================================================================#
# Imports
#=============================================================================#

# System Modules
import os
import sys
import glob
import json
import fnmatch
import errno
import math
import shutil

# Custom Modules
import click
from send2trash import send2trash  # https://github.com/hsoft/send2trash

#=============================================================================#
# Functions
#=============================================================================#

def parse_data(cfg):

    """Parse a given json file and return an data Array"""

    data = ""
    json_data = open(cfg)
    try:
        data = json.load(json_data)
    except ValueError, e:
        errmsg("Faulty settings file JSON \n %s\n" % cfg)
    json_data.close()

    return data

def check_if_file_exists(file):

    """Check if a given file exists either as a file, dir or symlink"""

    if any([
            os.path.isfile(file),
            os.path.isdir(file),
            os.path.islink(file)
            ]):
        return True

def prompt_to_overwrite(overwrite, file):

    """Check to overwrite the given file"""

    if not overwrite:
        prompt = ""
        click.echo("File " + file + " already exists.")

        # Overwrite Prompt
        #
        # a: Overwrite all files and don't ask anymore
        # y: Continue the symlink function and overwrite
        # n: Exit the symlink function and don't overwrite
        #
        # On any other input repeat the prompt
        while all([
            prompt != "y",
            prompt != "n",
            prompt != "a"
                ]):

            prompt = raw_input("Overwrite (y/n/a): ")

            if (prompt == "a"):
                overwrite = True  # Overwrite All
                return overwrite
            elif (prompt == "n"):
                overwrite = False
                return overwrite
            elif (prompt == "y"):
                return overwrite


def copy(cur, json, data, mode, overwrite=False, test=False):

    """ Copy, Symlink or Rsync Files read from a json_data

    Keyword Arguments:
    cur       -- Escaped and expanded dir where all the setting files are stored
    json      -- Current looping json
    src       -- Source file specifier
    dst       -- Destination file specifier
    title     -- Title of the current application, for better output
    overwrite -- Overwrite modus
    test      -- Test Modus, preview without executing
    """

    src = data["src"]
    dst = data["dst"]
    if data["title"]:
        title = data["title"]

    # Grab the full source path from the json file and append the parent dir
    json = os.path.dirname(json)
    src = json + "/" + src

    dst = os.path.expanduser(dst)

    # Cancel when the source file doesn't exist
    if not check_if_file_exists(src):
        click.echo()
        errmsg("The requested source doesnt exist: %s" % title)
        click.secho(src, fg="red")
        click.echo()
        return

    # Prompt the User to either overwrite existing files or skip them
    if check_if_file_exists(dst) and not overwrite:
        overwrite = prompt_to_overwrite(overwrite, dst)

    # Display Additional information
    if test:
        click.echo("Creating a %s for the file: " % mode)
        click.echo("  %s" % src)
        click.echo("  %s\n" % dst)
        return overwrite

    try:
        if (mode == "symlink"):
            trash(dst)
            os.symlink(src, dst)
            return overwrite
        elif (mode == "rsync"):
            trash(dst)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
            return overwrite
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            errmsg("The destinations parent dir doesn't exist!\n%s" % dst)


def trash(dst):

    """Moves given Objects to trash or unlinks symlinks"""

    if any([os.path.isfile(dst), os.path.isdir(dst)]):
        send2trash(dst)
    elif os.path.islink(dst):
        os.unlink(dst)


def locate(src,pattern):

    """Locate files matching a pattern in a folder and its subfolders"""

    matches = []
    for root, dirnames, filenames in os.walk(src):
      for filename in fnmatch.filter(filenames, pattern):
          matches.append(os.path.join(root, filename))

    return matches

def errmsg(msg):

    """Red error message with ERROR prefix"""

    click.secho("ERROR: %s" % msg, fg='red', err=True)


#=============================================================================#
# Main
#=============================================================================#

@click.command()

@click.option('--test', is_flag=True, help="Testing Mode")

@click.option('--list', is_flag=True, help="List All Settings")

@click.option('--single', help="Synchronize the Settings for a single configuration file")

@click.option('--overwrite', default=False, is_flag=True,
              help="Overwrite all files")

@click.option('--cfg_file', default="sync_settings.json", 
              help="Alternate name for the configuration file")

@click.option('--settings_dir', default="~/Settings",
              help="Set an alternate dir for your settings.                The default folder is ~/Settings")
# Sucky workaround to show the 2nd sentence in the next line because of the automatic
# text wrapping

def cli(test, cfg_file, overwrite, list, single, settings_dir):

    """Synchronize your app Settings"""

    # Check if the given settings dir exists
    settings_dir = os.path.expanduser(settings_dir)
    if (os.path.islink(settings_dir)):
        # Expand the user and find the symlink target path
        settings_dir = (os.path.realpath(os.path.expanduser(settings_dir)))
    elif (os.path.isdir(settings_dir)):
        # Expand the user and find the symlink target path
        settings_dir = (os.path.expanduser(settings_dir))
    else:
        errmsg("No Settings found in %s" % settings_dir)
        return

    # Locate all the config files in the given directory
    cfg = locate(settings_dir,cfg_file)

    # If there aren't any config files exit the script
    if not(cfg):
        errmsg("No %s configuration files found! in %s" % (cfg_file, settings_dir))
        return

    #---------------------------------------------------------------------------#
    # List Mode
    #---------------------------------------------------------------------------#

    # Print out a list of available configurations and numberize them
    # to be used in the --single parameter option
    if list:

        for x in cfg:
            
            # Add 1 to the counter index, to make it more user friendly
            counter = cfg.index(x) + 1
            
            # Hacky even alignment of the list
            spaces = ""
            if (len(cfg) >= 10 and counter < 10):
                spaces += " " 

            data = parse_data(x)
            if data["App"]: 
                click.echo("%s: %s%s" % (counter, spaces, data["App"]))

        return

    #---------------------------------------------------------------------------#
    # Single Mode
    #---------------------------------------------------------------------------#

    # Only symlink a given object from the arguments
    # checking first if the argument exists in the list, then removing every
    # other element from the cfg list except the chosen one
    if single:

        if single.isdigit(): 
            number = int(single) - 1
            try:
                new_cfg = cfg[number]
                del cfg[:]
                cfg.append(new_cfg)
            except IndexError:
                errmsg("Invalid number")
                return

        elif isinstance(single, basestring):

            found_item = False

            for x in cfg:
                data = parse_data(x)
                if data["App"] == single:
                    new_cfg = cfg[cfg.index(x)]
                    del cfg[:]
                    cfg = new_cfg
                    cfg.append(new_cfg)

            if found_item == False:
                errmsg("Invalid Input")                        
                return

        else:
            errmsg("Invalid Input")
            return


    click.echo(cfg)


    #---------------------------------------------------------------------------#
    # Regular Mode
    #---------------------------------------------------------------------------#

    # Loop through the configuration files and create the symlinks
    for x in cfg:

        data = parse_data(x)

        if data:
            # Get the folders to trash if they are available
            if "trash" in data:
                for t in data["trash"]:
                    trash(t)

            if "symlink" in data:
                
                for data in data["symlink"]:
                    overwrite = copy(
                        settings_dir,
                        x,
                        data,
                        "symlink",
                        overwrite,
                        test)

            if "rsync" in data:

                for data in data["rsync"]:
                    overwrite = copy(
                        settings_dir,
                        x,
                        data,
                        "rsync",
                        overwrite,
                        test)


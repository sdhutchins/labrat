## -*- coding: utf-8 -*-
#"""Organize a files into folders by file extensions."""
#
#import os
#import pathlib
#import logging as log
#from datetime import datetime as d
#from shutil import move, rmtree
#import zipfile
#
## Set up the logger
#format1 = '%a %b %d %I:%M:%S %p %Y'  # Used to add as a date
#format2 = '%m-%d-%Y_%I-%M-%S-%p'  # Used to append to archives
#
#log.basicConfig(filename="logs\directory_archiving_%s.log" % str(d.now().strftime(format2)), level=log.INFO)
#log.info("#------------------------------------------------------------------")
#log.info("The script name is %s" % os.path.basename(__file__))
#log.info("The date and time is currently %s" % str(d.now().strftime(format1)))
#log.info("#------------------------------------------------------------------")
#
##------------------------------------------------------------------------------
## Use paths
#downloads = r'C:\Users\shutchins2\Downloads'
#
#os.chdir(downloads)
#
## Create an archive directory that will be used later.
#arch = 'downloads_archive_%s' % str(d.now().strftime(format2))
#os.mkdir(arch)
#log.info('The archive directory has been created.')
#
#filetypes = []
#for file in os.listdir():
#    ext = pathlib.PureWindowsPath(file).suffix or pathlib.PurePosixPath(file).suffix
#    if ext == '':
#        log.info(file + " does not end in an extension.")
#        pass
#    elif ext == '.ini':  # This is a file that windows creates
#        pass
#    else:
#        extname = ext.replace(".", "")
#        filetypes.append(extname)
#
#        for ft in filetypes:
#            root_path = downloads
#            folder = ft + '_downloads'
#            # If the filetype folder exists, move files of that type to it
#            if os.path.isdir(folder) == True:
#                log.info("The %s directory exists." % folder)
#                os.system('move *.' + ft + ' ' + folder)
#                log.info("The file, %s, was moved to the %s directory." % (file, folder))
#                continue
#            else:
#                # If the filetype folder does not exist, create it and
#                # move files of that type to it
#                os.mkdir(folder)
#                log.info("The %s directory exists." % folder)
#                os.system('move *.' + ft + ' ' + folder)
#                log.info("The file, %s, was moved to the %s directory." % (file, folder))
#                continue
#
## After moving files to each file type directory, create an
## archive with all directories in it
#directories = os.listdir()
#for directory in directories:
#    arch = 'downloads_archive_%s' % str(d.now().strftime(format2))
#os.mkdir(arch)
#log.info('The archive directory has been created.')
#move(folder, arch)
#
## Create a zip file for the directory.
#with zipfile.ZipFile('downloads_archive.zip', 'w') as dloadzip:
#    dloadzip.write(arch)
#    log.info("%s has been written as a zip file." % arch)
#
## Remove the unzipped archive directory
#rmtree(arch)
#
#log.info("The zip file, %s, has been created and saved." % dloadzip)
#log.info("This script is complete.")
#
#
#

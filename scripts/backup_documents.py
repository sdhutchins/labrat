# -*- coding: utf-8 -*-
# Modules used
from shutil import copytree, rmtree
import logging as log
from datetime import datetime as d
import os
#------------------------------------------------------------------------------
# Set up the logger
format1 = '%a %b %d %I:%M:%S %p %Y'  # Used to add as a date
format2 = '%m-%d-%Y_%I-%M-%S-%p'  # Used to append to archives

log.basicConfig(filename="logs\directory_backup_%s.log" % str(d.now().strftime(format2)), level=log.INFO)
log.info("#------------------------------------------------------------------")
log.info("The script name is %s" % os.path.basename(__file__))
log.info("The date and time is currently %s" % str(d.now().strftime(format1)))
log.info("#------------------------------------------------------------------")

#------------------------------------------------------------------------------
docsdir = 'C:\\Users\\shutchins2\\Documents'
sdh = 'U:\\Backup'

# Change to U drive
os.chdir(sdh)
log.info('The archive directory has been created.')

copytree(docsdir, sdh)
log.info('%s has been backed up.' % docsdir)
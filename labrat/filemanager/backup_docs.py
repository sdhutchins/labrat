"""Back up folders/files."""

from shutil import copytree, SameFileError
from logzero import logger as log
import logzero
from datetime import datetime as d
import os
import contextlib


class Backup(object):
    def __init__(self, sourcedir, backupdir):
        """Set up the logger."""
        format1 = '%a %b %d %I:%M:%S %p %Y'  # Used to add as a date
        format2 = '%m-%d-%Y_%I-%M-%S-%p'  # Used to append to archives
        self._f1 = format1
        self._f2 = format2
        self.sourcedir = sourcedir
        self.backupdir = backupdir

    def backup(self):
        """Backup files from source directory to destination."""

        logzero.logfile("directory_backup_%s.log" %
                        str(d.now().strftime(self._f2)))
        sep = 50*'-'
        log.info("#%s" % sep)
        log.info("The script name is %s" % os.path.basename(__file__))
        log.info("The date and time is currently %s" %
                 str(d.now().strftime(self._f1)))

        with contextlib.suppress(OSError, SameFileError):
            log.error(OSError, SameFileError)
            copytree(self.sourcedir, self.backupdir)
            log.info('%s has been backed up.' % self.sourcedir)

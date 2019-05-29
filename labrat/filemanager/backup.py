"""Back up folders/files."""

from shutil import copytree
from datetime import datetime as d
import os
import contextlib

from logzero import logger as log
import logzero

from labrat import LOGFORMAT1, LOGFORMAT2


class Backup(object):
    def __init__(self, sourcedir, backupdir):
        """Initialize logger and run backup."""
        self._f1 = LOGFORMAT1
        self._f2 = LOGFORMAT2
        self.sourcedir = sourcedir
        self.backupdir = backupdir
        self.backup()

    def backup(self):
        """Backup files from source directory to destination."""
        logzero.logfile("directory_backup_%s.log" %
                        str(d.now().strftime(self._f2)))
        sep = 50 * '-'
        log.info("#%s" % sep)
        log.info("The script name is %s" % os.path.basename(__file__))
        log.info("The date and time is currently %s" %
                 str(d.now().strftime(self._f1)))

        with contextlib.suppress(OSError):
            # TODO Add SameFileError from shutil
            # TODO Add threading
            log.error(OSError)
            copytree(self.sourcedir, self.backupdir)
            log.info('%s has been backed up.' % self.sourcedir)

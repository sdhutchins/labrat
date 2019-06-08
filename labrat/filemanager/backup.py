"""Back up folders and files."""
from shutil import copytree
from datetime import datetime as d
import os
import contextlib

from logzero import logger as log
import logzero

from labrat import _DATEFMT1, _DATEFMT2


class Backup(object):
    """Backup import files"""

    def __init__(self, source_dir, backup_dir):
        """Initialize logger and run backup.

        Args:
            source_dir (str): The directory to copy or backup.
            backup_dir (str): The destination of your file backup.
        """
        self.source_dir = source_dir
        self.backup_dir = backup_dir

    def backup(self):
        """Backup files from source directory to destination."""
        logzero.logfile("directory_backup_%s.log" %
                        str(d.now().strftime(_DATEFMT1)))
        sep = 50 * '-'
        log.info("#%s" % sep)
        log.info("The script name is %s" % os.path.basename(__file__))
        log.info("The date and time is currently %s" %
                 str(d.now().strftime(_DATEFMT2)))

        with contextlib.suppress(OSError):
            # TODO Add SameFileError from shutil
            # TODO Add threading
            log.error(OSError)
            copytree(self.source_dir, self.backup_dir)
            log.info('%s has been backed up.' % self.source_dir)

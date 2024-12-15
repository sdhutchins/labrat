from shutil import copytree, SameFileError
from datetime import datetime
import os
import contextlib
from pathlib import Path
import logzero
from logzero import logger


class Archiver:
    """Archive folders and files."""

    def __init__(self, source_dir, archive_dir):
        """
        Initialize logger and archive parameters.

        Args:
            source_dir (str or Path): The directory to copy or archive.
            archive_dir (str or Path): The destination directory for the archive.
        """
        self.source_dir = Path(source_dir).resolve()
        self.archive_dir = Path(archive_dir).resolve()

        if not self.source_dir.exists() or not self.source_dir.is_dir():
            raise ValueError(f"Source directory '{self.source_dir}' does not exist or is not a directory.")
        logger.debug(f"Source directory: {self.source_dir}")

        if not self.archive_dir.parent.exists():
            raise ValueError(f"archive directory parent '{self.archive_dir.parent}' does not exist.")
        logger.debug(f"archive directory: {self.archive_dir}")

        # Configure log file
        logzero.logfile(f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logger.info("archive initialized.")

    def archive(self):
        """
        Perform the archive by copying the source directory to the archive directory.

        Raises:
            SameFileError: If the source and destination are the same.
            OSError: For other filesystem-related errors.
        """
        logger.info("Starting archive process...")
        logger.info(f"Source: {self.source_dir}")
        logger.info(f"Destination: {self.archive_dir}")

        try:
            copytree(self.source_dir, self.archive_dir)
            logger.info(f"archive completed successfully: {self.source_dir} -> {self.archive_dir}")
        except SameFileError as e:
            logger.error(f"Source and destination are the same: {e}")
        except FileExistsError:
            logger.warning(f"archive destination already exists: {self.archive_dir}")
        except OSError as e:
            logger.error(f"Failed to complete archive: {e}")
            raise

    @staticmethod
    def get_archive_dir(base_dir, project_name):
        """
        Generate a timestamped archive directory path.

        Args:
            base_dir (str or Path): The base directory where archives are stored.
            project_name (str): The name of the project being archived.

        Returns:
            Path: A path to the timestamped archive directory.
        """
        base_dir = Path(base_dir).resolve()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = base_dir / f"{project_name}_archive_{timestamp}"
        logger.debug(f"Generated archive directory: {archive_dir}")
        return archive_dir

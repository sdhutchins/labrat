import shutil
from pathlib import Path
import datetime
import logzero
from logzero import logger
from labrat.utils import get_labrat_dir


class FileOrganizer:
    """
    A utility class for organizing files in standard directories like Downloads and Documents.
    Designed for integration into the labrat tool.
    """

    def __init__(self):
        """
        Initialize the FileOrganizer class with default directories.
        """
        self.downloads_dir = Path.home() / "Downloads"
        self.documents_dir = Path.home() / "Documents"
        self.pictures_dir = Path.home() / "Pictures"
        self.videos_dir = Path.home() / "Videos"
        self.archive_dir = self.documents_dir / "Archive"
        self.specific_dir = self.documents_dir / "Organized_Files"
        # Default science files directory for organizing scientific data files
        self.science_dir = self.documents_dir / "Research_Data"

        # Subfolders for documents and archives
        self.document_subfolders = {
            "Word": ["docx", "doc"],
            "Excel": ["xlsx", "xls"],
            "Presentations": ["pptx", "ppt"],
            "PDFs": ["pdf"],
            "Scripts": ["py", "r", "sh", "rmd"],
            "TextFiles": ["txt", "md", "csv", "tsv", "xml", "json", "yaml", "rtf"]
        }

        self.archive_subfolders = {
            "ZIP": ["zip"],
            "DMG": ["dmg"],
            "TAR": ["tar", "tgz", "gz", "bz2", "xz"],
            "RAR": ["rar"],
            "Installers": ["pkg", "exe", "msi"],
            "Certificates": ["crt"]
        }

        self.file_extensions = {
            "pictures": [
                ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff",
                ".heic", ".webp", ".svg", ".raw", ".nef", ".cr2",
                ".orf", ".arw", ".psd", ".ai"
            ],
            "videos": [
                ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv",
                ".m4v", ".mpeg", ".3gp", ".webm"
            ]
        }
        
        # Scientific data file extensions for research data files
        # Bioinformatics & Genomics
        # Astronomy & Physics
        self.science_extensions = [
            # Bioinformatics & Genomics
            "fastq", "fq",  # Sequencing data
            "fasta", "fa",  # Sequence files
            "sam", "bam", "cram",  # Alignment files
            "vcf", "bcf",  # Variant call format
            "bed", "gff", "gtf",  # Genomic annotations
            "nex", "nexus", "phylip",  # Phylogenetic data
            "pdb", "mmcif",  # Protein structures
            # Astronomy & Physics
            "fits", "fit",  # Astronomy images/data
            "hdf5", "h5",  # Hierarchical data format
            "nc", "nc4",  # NetCDF (climate/oceanography)
            "cdf",  # Common Data Format (NASA)
        ]

        # Configure logzero
        # Store logs in user's home directory under .labrat folder
        labrat_dir = get_labrat_dir()
        log_file = labrat_dir / "file_organizer.log"
        logzero.logfile(str(log_file))
        logger.info("FileOrganizer initialized.")

    def move_file(self, src_file: Path, dest_dir: Path):
        """
        Move a file to the destination directory, handling duplicates and logging actions.

        Args:
            src_file (Path): The source file to move.
            dest_dir (Path): The destination directory where the file will be moved.
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / src_file.name

        if dest_file.exists():
            if src_file.stat().st_mtime > dest_file.stat().st_mtime:
                dest_file.unlink()
                logger.info(f"Replaced older file: {dest_file}")
            else:
                logger.info(f"Skipped older file: {src_file}")
                src_file.unlink()
                return
        else:
            logger.info(f"Moving file: {src_file} -> {dest_dir}")

        shutil.move(str(src_file), str(dest_dir))

    def organize_by_year(self, file_path: Path, base_dir: Path):
        """
        Organize files into subfolders by year based on the last modified timestamp.

        Args:
            file_path (Path): The file to organize.
            base_dir (Path): The base directory where files are organized.
        """
        year = datetime.datetime.fromtimestamp(file_path.stat().st_mtime).year
        year_dir = base_dir / str(year)
        self.move_file(file_path, year_dir)

    def organize_documents(self):
        """
        Organize documents into subfolders by type and year.
        """
        logger.info("Organizing documents...")
        for subfolder, exts in self.document_subfolders.items():
            for ext in exts:
                for file_path in self.documents_dir.glob(f"*.{ext}"):
                    self.organize_by_year(file_path, self.documents_dir / subfolder)
                for file_path in self.downloads_dir.glob(f"*.{ext}"):
                    self.organize_by_year(file_path, self.documents_dir / subfolder)
        logger.info("Finished organizing documents.")

    def organize_archives(self):
        """
        Organize archives into subfolders by compression type.
        """
        logger.info("Organizing archives...")
        for subfolder, exts in self.archive_subfolders.items():
            for ext in exts:
                for file_path in self.documents_dir.glob(f"*.{ext}"):
                    self.move_file(file_path, self.archive_dir / subfolder)
                for file_path in self.downloads_dir.glob(f"*.{ext}"):
                    self.move_file(file_path, self.archive_dir / subfolder)
        logger.info("Finished organizing archives.")

    def organize_files(self):
        """
        Organize files into standard categories (e.g., Pictures, Videos).
        """
        logger.info("Organizing files into categories...")
        categories = {
            "pictures": {
                "sources": [self.downloads_dir, self.documents_dir],
                "dest": self.pictures_dir
            },
            "videos": {
                "sources": [self.downloads_dir, self.documents_dir],
                "dest": self.videos_dir
            }
        }

        for category, info in categories.items():
            for source_dir in info["sources"]:
                for ext in self.file_extensions[category]:
                    for file_path in source_dir.glob(f"*{ext}"):
                        self.move_file(file_path, info["dest"])
        logger.info("Finished organizing files.")

    def move_specific_files(self, keyword: str = "specific"):
        """
        Move files containing a specific keyword in their names to a designated folder.

        Args:
            keyword (str): Keyword to match in filenames. Default is 'specific'.
        """
        logger.info(f"Moving files containing keyword '{keyword}'...")
        for source_dir in [self.downloads_dir, self.documents_dir]:
            for file_path in source_dir.glob(f"*{keyword}*"):
                self.move_file(file_path, self.specific_dir)
        logger.info("Finished moving specific files.")

    def organize_science_files(self, science_dir=None):
        """
        Organize scientific data files into a dedicated research files folder.

        Handles common scientific file formats including:
        - Bioinformatics: fastq, fasta, sam, bam, vcf, bed, gff, gtf
        - Astronomy: fits, hdf5, nc (NetCDF)
        - General: csv, tsv, json, h5, parquet
        - Computational: ipynb, py, r, R

        Args:
            science_dir (Path, optional): Custom directory for science files.
                Defaults to Documents/Research_Data.
        """
        if science_dir is None:
            science_dir = self.science_dir
        else:
            science_dir = Path(science_dir)

        logger.info(f"Organizing scientific data files to {science_dir}...")
        
        # Search in Downloads and Documents
        for source_dir in [self.downloads_dir, self.documents_dir]:
            for ext in self.science_extensions:
                # Handle case-insensitive extensions
                # For extensions with dots (like .fq.gz), handle them specially
                if "." in ext:
                    # Multi-part extension like .fq.gz
                    pattern = f"*.{ext}"
                    for file_path in source_dir.glob(pattern):
                        self.move_file(file_path, science_dir)
                    # Also try uppercase
                    pattern_upper = f"*.{ext.upper()}"
                    for file_path in source_dir.glob(pattern_upper):
                        self.move_file(file_path, science_dir)
                else:
                    # Simple extension
                    for pattern in [f"*.{ext}", f"*.{ext.upper()}", f"*.{ext.capitalize()}"]:
                        for file_path in source_dir.glob(pattern):
                            self.move_file(file_path, science_dir)
        
        logger.info("Finished organizing scientific data files.")

    def organize_all(self):
        """
        Execute all organizational tasks in sequence.
        """
        logger.info("Starting file organization tasks...")
        self.organize_documents()
        self.organize_archives()
        self.organize_files()
        self.move_specific_files(keyword="shaurita")
        logger.info("File organization tasks completed.")

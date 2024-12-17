import unittest
from pathlib import Path
from labrat.filemanager import FileOrganizer # type: ignore
import shutil
import datetime

class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        """
        Set up temporary directories and files for testing.
        """
        self.test_dir = Path("./test_file_organizer")
        self.test_dir.mkdir(parents=True, exist_ok=True)

        self.downloads_dir = self.test_dir / "Downloads"
        self.documents_dir = self.test_dir / "Documents"
        self.pictures_dir = self.test_dir / "Pictures"

        # Simulate user directories
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.documents_dir.mkdir(parents=True, exist_ok=True)

        # Create test files
        (self.downloads_dir / "test_image.jpg").write_text("This is an image file.")
        (self.documents_dir / "test_doc.pdf").write_text("This is a PDF file.")

        # Initialize the organizer with test paths
        self.organizer = FileOrganizer()
        self.organizer.downloads_dir = self.downloads_dir
        self.organizer.documents_dir = self.documents_dir
        self.organizer.pictures_dir = self.pictures_dir

    def tearDown(self):
        """
        Clean up temporary files and directories.
        """
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_organize_files(self):
        """
        Test file organization for pictures.
        """
        self.organizer.organize_files()
        self.assertTrue((self.pictures_dir / "test_image.jpg").exists())
        self.assertFalse((self.downloads_dir / "test_image.jpg").exists())

    def test_organize_documents(self):
        """
        Test file organization for documents.
        """
        self.organizer.organize_documents()
        
        # Determine the year for organization
        year = datetime.datetime.now().year
        pdf_dir = self.documents_dir / "PDFs" / str(year)
        
        # Check if the file was moved correctly
        self.assertTrue((pdf_dir / "test_doc.pdf").exists())
        self.assertFalse((self.documents_dir / "test_doc.pdf").exists())

    def test_move_specific_files(self):
        """
        Test moving files containing specific keywords.
        """
        specific_dir = self.organizer.specific_dir
        (self.downloads_dir / "shaurita_test.txt").write_text("Specific file for testing.")
        self.organizer.move_specific_files(keyword="shaurita")
        self.assertTrue((specific_dir / "shaurita_test.txt").exists())

if __name__ == "__main__":
    unittest.main()

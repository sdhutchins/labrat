import unittest
from pathlib import Path
from labrat.filemanager import Archiver
import shutil

class TestArchiver(unittest.TestCase):
    def setUp(self):
        """
        Set up temporary directories and files for testing.
        """
        self.test_dir = Path("./test_archiver")
        self.source_dir = self.test_dir / "source"
        self.archive_base_dir = self.test_dir / "archives"

        self.source_dir.mkdir(parents=True, exist_ok=True)
        (self.source_dir / "file1.txt").write_text("This is a test file.")
        (self.source_dir / "file2.txt").write_text("Another test file.")

        self.archive_base_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        """
        Clean up temporary files and directories.
        """
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_archive(self):
        """
        Test archiving functionality.
        """
        archive_dir = Archiver.get_archive_dir(self.archive_base_dir, "test_project")
        archiver = Archiver(source_dir=self.source_dir, archive_dir=archive_dir)
        zip_path = archiver.archive()

        self.assertTrue(archive_dir.exists(), "Archive directory does not exist.")
        self.assertTrue((archive_dir / "file1.txt").exists(), "File1.txt was not archived.")
        self.assertTrue((archive_dir / "file2.txt").exists(), "File2.txt was not archived.")
        self.assertTrue(Path(zip_path).exists(), "Zip file was not created.")
        self.assertTrue(zip_path.endswith(".zip"), "Zip file does not have the correct extension.")

if __name__ == "__main__":
    unittest.main()

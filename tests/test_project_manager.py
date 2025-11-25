import unittest
from pathlib import Path
import json
import shutil
import tempfile
from unittest.mock import patch
from labrat.project import ProjectManager

class TestProjectManager(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """
        self.test_dir = Path("./test_project_manager")
        self.project_path = self.test_dir / "test_project"
        self.archive_dir = self.test_dir / "archives"
        
        # Create a temporary directory for .labrat config to avoid modifying user's real config
        self.temp_labrat_dir = Path(tempfile.mkdtemp(prefix="labrat_test_"))
        self.labrat_file = self.temp_labrat_dir / "config.json"

        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Mock get_labrat_dir to return our temporary directory for testing
        # This ensures tests don't modify the user's actual .labrat directory
        self.labrat_dir_patcher = patch('labrat.project.projectmanager.get_labrat_dir')
        self.mock_get_labrat_dir = self.labrat_dir_patcher.start()
        self.mock_get_labrat_dir.return_value = self.temp_labrat_dir

        self.manager = ProjectManager(username="test_user")

    def tearDown(self):
        """
        Clean up test environment.
        """
        # Stop the mock
        self.labrat_dir_patcher.stop()
        
        # Clean up test directories
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        # Clean up temporary .labrat directory used for testing
        if self.temp_labrat_dir.exists():
            shutil.rmtree(self.temp_labrat_dir)

    def test_new_project(self):
        """
        Test creation of a new project.
        """
        self.manager.new_project(
            project_type="computational-biology",
            project_name="Test Project",
            project_path=self.project_path,
            description="A test project"
        )
        self.assertTrue(self.project_path.exists(), "Project directory was not created.")
        with self.labrat_file.open("r") as f:
            data = json.load(f)
            self.assertEqual(len(data["projects"]), 1, "Project metadata was not updated.")
            self.assertEqual(data["projects"][0]["name"], "test_project", "Project name mismatch.")

    def test_delete_project(self):
        """
        Test deletion of a project.
        """
        self.manager.new_project(
            project_type="computational-biology",
            project_name="Test Project",
            project_path=self.project_path,
            description="A test project"
        )
        self.manager.delete_project(self.project_path, self.archive_dir)
        self.assertFalse(self.project_path.exists(), "Project directory was not deleted.")
        self.assertTrue(any(self.archive_dir.iterdir()), "Project was not archived.")

    def test_add_template(self):
        """
        Test adding a new template.
        """
        self.manager.add_template("new-template", "https://github.com/example/cookiecutter-new")
        with self.labrat_file.open("r") as f:
            data = json.load(f)
            self.assertIn("new-template", data["templates"], "Template was not added.")

if __name__ == "__main__":
    unittest.main()

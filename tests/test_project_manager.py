import unittest
from pathlib import Path
import json
from labrat.project.projectmanager import ProjectManager
import shutil

class TestProjectManager(unittest.TestCase):
    def setUp(self):
        """
        Set up test environment.
        """
        self.test_dir = Path("./test_project_manager")
        self.project_path = self.test_dir / "test_project"
        self.archive_dir = self.test_dir / "archives"
        self.labrat_file = Path.home() / ".labrat"

        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Remove existing .labrat file if it exists
        if self.labrat_file.exists():
            self.labrat_file.unlink()

        self.manager = ProjectManager(username="test_user")

    def tearDown(self):
        """
        Clean up test environment.
        """
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if self.labrat_file.exists():
            self.labrat_file.unlink()

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

import json
from pathlib import Path
from datetime import datetime
from logzero import logger
from labrat.filemanager.archive import Archiver


class ProjectManager:
    labrat_file = Path.home() / ".labrat"

    def __init__(self, username=None):
        """
        Initialize the project manager with a default username.

        Args:
            username (str, optional): The user's name. Defaults to the value in .labrat or 'default_user'.
        """
        self.username = username or self._get_default_username()
        logger.info(f"ProjectManager initialized with username: {self.username}")

    def _get_default_username(self):
        """
        Retrieve the default project manager username from the .labrat file.

        Returns:
            str: The default username.
        """
        if self.labrat_file.exists():
            try:
                with self.labrat_file.open("r") as f:
                    data = json.load(f)
                    logger.debug("Default username retrieved from .labrat file.")
                    return data.get("project_manager", "default_user")
            except Exception as e:
                logger.error(f"Failed to read .labrat file for default username: {e}")
        logger.warning("No .labrat file found. Using default username: 'default_user'")
        return "default_user"

    def _update_labrat_file(self, project_data):
        """
        Update the .labrat file with the new or updated project metadata.

        Args:
            project_data (dict): The metadata of the project to add/update.
        """
        data = {"project_manager": self.username, "projects": []}

        if self.labrat_file.exists():
            try:
                with self.labrat_file.open("r") as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to read existing .labrat file: {e}")

        # Update or add the project
        projects = data.get("projects", [])
        for idx, project in enumerate(projects):
            if project["path"] == project_data["path"]:
                projects[idx] = project_data
                logger.debug(f"Updated metadata for project: {project_data['name']}")
                break
        else:
            projects.append(project_data)
            logger.debug(f"Added new project to .labrat file: {project_data['name']}")

        data["projects"] = projects

        # Write back to .labrat
        try:
            with self.labrat_file.open("w") as f:
                json.dump(data, f, indent=4)
            logger.info(f".labrat file updated successfully.")
        except Exception as e:
            logger.error(f"Failed to update .labrat file: {e}")
            raise

    def new_project(self, project_type, project_name, project_path, description):
        """
        Create a new project and update its metadata in the .labrat file.

        Args:
            project_type (str): The type of project.
            project_name (str): The name of your project.
            project_path (str): The destination path of the project.
            description (str): A description of the project.
        """
        sanitized_name = project_name.replace(" ", "_")
        validated_path = Path(project_path).resolve()

        if not validated_path.exists():
            validated_path.mkdir(parents=True)
            logger.info(f"Created directory: {validated_path}")
        else:
            logger.info(f"Using existing directory: {validated_path}")

        now = datetime.now().isoformat()
        project_data = {
            "name": sanitized_name,
            "path": str(validated_path),
            "description": description,
            "created_at": now,
            "last_modified": now,
            "project_type": project_type,
        }

        # Update the global .labrat file
        self._update_labrat_file(project_data)

        # Simulate project creation (e.g., cookiecutter logic here)
        logger.info(f"Project '{sanitized_name}' created successfully at {validated_path}")

    def list_projects(self):
        """
        List all projects stored in the .labrat file.

        Returns:
            list: A list of project metadata dictionaries.
        """
        if self.labrat_file.exists():
            try:
                with self.labrat_file.open("r") as f:
                    data = json.load(f)
                    logger.debug(f"Retrieved {len(data.get('projects', []))} projects from .labrat file.")
                    return data.get("projects", [])
            except Exception as e:
                logger.error(f"Failed to read .labrat file: {e}")
        logger.warning("No projects found in .labrat file.")
        return []

    def update_project(self, project_path):
        """
        Update the last modified timestamp for an existing project.

        Args:
            project_path (str): The path to the project to update.
        """
        projects = self.list_projects()
        for project in projects:
            if project["path"] == str(Path(project_path).resolve()):
                project["last_modified"] = datetime.now().isoformat()
                self._update_labrat_file(project)
                logger.info(f"Updated project '{project['name']}' last modified timestamp.")
                return

        logger.warning(f"No project found at path: {project_path}")

    def list_project_files(self, project_path):
        """
        List all files within the given project directory.

        Args:
            project_path (str): The path to the project.

        Returns:
            list: A list of file paths within the project directory.
        """
        validated_path = Path(project_path).resolve()

        if not validated_path.exists() or not validated_path.is_dir():
            logger.error(f"Invalid project path: {validated_path}")
            return []

        file_list = []
        try:
            file_list = [str(file) for file in validated_path.rglob("*") if file.is_file()]
            logger.info(f"Found {len(file_list)} files in project directory: {validated_path}")
        except Exception as e:
            logger.error(f"Failed to list files in project directory: {e}")
        return file_list
    
    def archive_project(self, project_path, archive_base_dir):
        """
        Archive a project directory to a timestamped archive folder.

        Args:
            project_path (str or Path): The path to the project directory.
            archive_base_dir (str or Path): The base directory for storing archive.

        Returns:
            str: Path to the created archive directory.
        """
        project_path = Path(project_path).resolve()

        if not project_path.exists() or not project_path.is_dir():
            logger.error(f"Invalid project path: {project_path}")
            raise ValueError(f"Project path '{project_path}' does not exist or is not a directory.")

        project_name = project_path.name
        archive_dir = Archiver.get_archive_dir(archive_base_dir, project_name)

        # Perform the archive
        archive = Archiver(source_dir=project_path, archive_dir=archive_dir)
        archive.archive()

        logger.info(f"Archive completed for project '{project_name}'.")
        return str(archive_dir)
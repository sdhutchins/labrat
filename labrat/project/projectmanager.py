import json
import shutil
from pathlib import Path
from datetime import datetime
from logzero import logger
from cookiecutter.main import cookiecutter
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
        self.project_templates = self._load_templates()

    def _initialize_labrat_file(self, default_templates):
        """
        Initialize the .labrat file with default templates and structure.

        Args:
            default_templates (dict): A dictionary of default project templates.
        """
        initial_data = {
            "project_manager": self.username,
            "projects": [],
            "templates": default_templates,
        }
        try:
            with self.labrat_file.open("w") as f:
                json.dump(initial_data, f, indent=4)
            logger.info("Initialized .labrat file successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize .labrat file: {e}")
            raise

    def _load_templates(self):
        """
        Load project templates from the .labrat file or initialize with defaults.

        Returns:
            dict: A dictionary of project templates.
        """
        default_templates = {
            "computational-biology": "https://github.com/sdhutchins/cookiecutter-computational-biology",
            "data-science": "https://github.com/drivendataorg/cookiecutter-data-science",
            "andymcdgeo-streamlit": "https://github.com/andymcdgeo/cookiecutter-streamlit"

        }

        if self.labrat_file.exists():
            try:
                with self.labrat_file.open("r") as f:
                    data = json.load(f)
                    templates = data.get("templates", {})
                    if not templates:
                        logger.info("No templates found in .labrat file. Initializing with defaults.")
                        data["templates"] = default_templates
                        with self.labrat_file.open("w") as wf:
                            json.dump(data, wf, indent=4)
                    logger.debug(f"Loaded {len(data['templates'])} templates from .labrat file.")
                    return data["templates"]
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Malformed or empty .labrat file. Reinitializing: {e}")
            except Exception as e:
                logger.error(f"Failed to load templates from .labrat file: {e}")
        else:
            logger.info("No .labrat file found. Initializing with default templates.")
            self._initialize_labrat_file(default_templates)

        return default_templates

    
    def _save_templates(self):
        """
        Save the current project templates to the .labrat file.
        """
        if self.labrat_file.exists():
            try:
                with self.labrat_file.open("r") as f:
                    data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to read existing .labrat file: {e}")
                data = {}

        data["templates"] = self.project_templates

        try:
            with self.labrat_file.open("w") as f:
                json.dump(data, f, indent=4)
            logger.info("Templates saved successfully to .labrat file.")
        except Exception as e:
            logger.error(f"Failed to save templates to .labrat file: {e}")
            raise

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
    
    def _remove_project_metadata(self, project_path):
        """
        Remove a project's metadata from the .labrat file.

        Args:
            project_path (str): The path of the project to remove.
        """
        if not self.labrat_file.exists():
            logger.warning(".labrat file does not exist. No metadata to update.")
            return

        try:
            with self.labrat_file.open("r") as f:
                data = json.load(f)

            projects = data.get("projects", [])
            updated_projects = [p for p in projects if p.get("path") != project_path]

            if len(projects) == len(updated_projects):
                logger.warning(f"No metadata found for project at path: {project_path}")
            else:
                data["projects"] = updated_projects
                with self.labrat_file.open("w") as f:
                    json.dump(data, f, indent=4)
                logger.info(f"Metadata for project at '{project_path}' removed successfully.")
        except Exception as e:
            logger.error(f"Failed to update .labrat file: {e}")
            raise

    def _update_labrat_file(self, project_data):
        """
        Update the .labrat file with the new or updated project metadata.

        Args:
            project_data (dict): The metadata of the project to add/update.
        """
        if not self.labrat_file.exists():
            logger.warning(".labrat file not found. Initializing.")
            self._initialize_labrat_file(self._load_templates())

        try:
            with self.labrat_file.open("r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            logger.warning("Malformed .labrat file. Reinitializing.")
            data = {"project_manager": self.username, "projects": [], "templates": self.project_templates}
        except Exception as e:
            logger.error(f"Failed to read existing .labrat file: {e}")
            raise

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

        Raises:
            ValueError: If the project type is not valid.
        """
        if project_type not in self.project_templates:
            logger.error(f"Invalid project type: {project_type}")
            raise ValueError(
                f"{project_type} is not a valid project type. "
                f"Available types: {', '.join(self.project_templates.keys())}"
            )

        sanitized_name = project_name.replace(" ", "_")
        validated_path = Path(project_path).resolve()

        if not validated_path.exists():
            validated_path.mkdir(parents=True)
            logger.info(f"Created base directory: {validated_path}")
        else:
            logger.info(f"Using existing directory: {validated_path}")

        # Generate project structure with cookiecutter
        project_template = self.project_templates[project_type]
        project_context = {
            "full_name": self.username,
            "project_name": sanitized_name,
            "raw_project_name": project_name,
            "project_short_description": description,
        }

        try:
            logger.info(f"Using cookiecutter template: {project_template}")
            # Use the returned path from cookiecutter
            actual_project_path = Path(
                cookiecutter(
                    template=project_template,
                    no_input=True,
                    extra_context=project_context,
                    output_dir=str(validated_path),
                )
            )
            logger.info(f"Cookiecutter created project directory: {actual_project_path}")
        except Exception as e:
            logger.error(f"Failed to generate project structure: {e}")
            raise

        now = datetime.now().isoformat()
        project_data = {
            "name": actual_project_path.name,  # Use the name generated by cookiecutter
            "path": str(actual_project_path),  # Full path to the project directory
            "description": description,
            "created_at": now,
            "last_modified": now,
            "project_type": project_type,
        }

        # Update the global .labrat file
        self._update_labrat_file(project_data)

        logger.info(f"Project '{actual_project_path.name}' created successfully at {actual_project_path}")

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
            archive_base_dir (str or Path): The base directory for storing archives.

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
    
    def add_template(self, name, url):
        """
        Add a new project template.

        Args:
            name (str): The name of the template.
            url (str): The repository URL of the template.

        Raises:
            ValueError: If the template name already exists.
        """
        if name in self.project_templates:
            logger.error(f"Template '{name}' already exists.")
            raise ValueError(f"Template '{name}' already exists.")

        self.project_templates[name] = url
        self._save_templates()
        logger.info(f"Added new template: {name} -> {url}")

    def delete_project(self, project_path, archive_base_dir):
        """
        Archive and delete a project directory.

        Args:
            project_path (str or Path): The path to the project directory.
            archive_base_dir (str or Path): The base directory for storing archives.

        Raises:
            ValueError: If the project path does not exist or is not a directory.
        """
        project_path = Path(project_path).resolve()

        if not project_path.exists() or not project_path.is_dir():
            logger.error(f"Invalid project path: {project_path}")
            raise ValueError(f"Project path '{project_path}' does not exist or is not a directory.")

        project_name = project_path.name

        # Archive the project
        logger.info(f"Archiving project '{project_name}' before deletion.")
        archive_dir = self.archive_project(project_path, archive_base_dir)

        # Delete the project directory
        try:
            shutil.rmtree(project_path)
            logger.info(f"Project '{project_name}' deleted successfully from: {project_path}")
        except Exception as e:
            logger.error(f"Failed to delete project '{project_name}': {e}")
            raise

        # Remove the project metadata from .labrat
        self._remove_project_metadata(str(project_path))
        logger.info(f"Project '{project_name}' metadata removed from .labrat.")

        return archive_dir

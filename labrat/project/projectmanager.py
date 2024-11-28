import os
from pathlib import Path
from cookiecutter.main import cookiecutter
from logzero import logger


class ProjectManager:
    def __init__(self, username):
        """
        Initialize the project manager by adding a username.

        Args:
            username (str): The user's name.
        """
        self.username = username
        self.project_templates = {
            "computational-biology": "https://github.com/sdhutchins/cookiecutter-computational-biology"
        }

    def validate_path(self, path):
        """
        Ensure the given path exists or create it.

        Args:
            path (str): The directory path to validate.

        Returns:
            str: The absolute path.
        """
        abs_path = Path(path).resolve()
        if not abs_path.exists():
            abs_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {abs_path}")
        else:
            logger.info(f"Using existing directory: {abs_path}")
        return str(abs_path)

    def sanitize_name(self, name):
        """
        Sanitize the project name by removing invalid characters and spaces.

        Args:
            name (str): The project name.

        Returns:
            str: Sanitized project name.
        """
        sanitized = name.replace(" ", "_")
        logger.debug(f"Sanitized project name: {sanitized}")
        return sanitized

    def new_project(self, project_type, project_name, project_path, description):
        """
        Create a new project from an existing template.

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
            raise ValueError(f"{project_type} is not a valid project type.")
        
        project_template = self.project_templates[project_type]
        sanitized_name = self.sanitize_name(project_name)
        validated_path = self.validate_path(project_path)

        project_dict = {
            "full_name": self.username,
            "project_name": sanitized_name,
            "project_short_description": description,
        }

        try:
            logger.info(f"Creating project '{sanitized_name}' at {validated_path}...")
            cookiecutter(
                template=project_template,
                no_input=True,
                extra_context=project_dict,
                output_dir=validated_path,
            )
            logger.info(
                f"Project '{sanitized_name}' created successfully at {validated_path}"
            )
        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            raise

    def custom_project(self, template_path, project_name, project_path):
        """
        Create a custom project from a user-provided template.

        Args:
            template_path (str): Path to the custom cookiecutter template.
            project_name (str): The name of your project.
            project_path (str): The destination path of the project.
        """
        project_dict = {
            "full_name": self.username,
            "project_name": self.sanitize_name(project_name),
        }
        validated_path = self.validate_path(project_path)

        try:
            logger.info(f"Creating custom project '{project_name}' at {validated_path}...")
            cookiecutter(
                template=template_path,
                no_input=True,
                extra_context=project_dict,
                output_dir=validated_path,
            )
            logger.info(
                f"Custom project '{project_name}' created successfully at {validated_path}"
            )
        except Exception as e:
            logger.error(f"Failed to create custom project: {e}")
            raise

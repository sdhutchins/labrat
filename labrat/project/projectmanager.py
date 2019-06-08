from cookiecutter.main import cookiecutter
#from cookiecutter.prompt import prompt_for_config
#from cookiecutter.generate import generate_context
#from cookiecutter.hooks import run_script


class ProjectManager(object):
    def __init__(self, username):
        """Initialize the project manager by adding a username.

        Args:
            username (str): The user's name.
        """
        self.username = username
        self.computational_biology = 'computational-biology'
        self.project_types = [self.computational_biology]

    def new_project(self, project_type, project_name, project_path, description):
        """Create a new project from an existing template.

        Args:
            project_type (str): The type of project.
            project_name (str): The name of your project.
            project_path (str): The destination path of the project.
            description (str): A description of the project.

        Raises:
            UserWarning: Warns the user about invalid project types.
        """
        # TODO Ensure project_path exists or create the path
        # TODO Ensure project_name has no spaces
        # TODO Create codes for project_type and config or json file for each
        # project_type
        if project_type in self.project_types:
            if project_type == self.computational_biology:
                project_dict = {"full_name": self.username,
                                "project_name": project_name,
                                "project_short_description": description,
                                }
                cookiecutter(template='computational-biology', no_input=True,
                             extra_context=project_dict,
                             output_dir=project_path)
                print('Your project, %s, has been created at %s' % (project_name,
                                                                    project_path))

        else:
            raise UserWarning('%s is not a valid project type.' % project_type)

    def custom_project(self):
        """Create a custom project."""
        raise NotImplementedError

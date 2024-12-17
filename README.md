# labrat

[![Build Status](https://app.travis-ci.com/sdhutchins/labrat.svg?token=xfnbNTQhjNbir5xACn8R&branch=master)](https://app.travis-ci.com/sdhutchins/labrat)

A basic science lab framework aimed at reproducibility and lab management. This package is in the very early stages of development.

## Features

- Easily use math functions to dilute solutions, calculate molarity, etc.
- Backup your documents using the command-line
- Manage lab inventory using a GUI
- Create and manage new projects using the command-line

## Install

1. Clone this repository.
2. Change to the downloaded repository's base directory.
3. `pip install .`

If you want to develop or contribute to this package, install with `pip install -e .`

## Examples

### Dilute a stock concentration

```python
from labrat.math import dilute_stock

# Get the final concentration
dilute_stock(100, 2, **{'vF': 4})
```

### Project Management

Create a new project using the below code. This will create a `.labrat` file that contains the project information for
any project created.

```python
# Create a new project
import os
from labrat.project import ProjectManager

# Initialize the ProjectManager with a username
project_manager = ProjectManager('Dr. Jane Doe')

# Create a new project
project_manager.new_project(
    project_type='computational-biology',
    project_name='KARG Analysis',
    project_path=os.getcwd(),
    description="Analyze the KARG data."
)
```

Archive a project:

```python
from projectmanager import ProjectManager

project_manager = ProjectManager()
project_path = "/Users/shutchens/Documents/Git-Repos/labrat/karg_analysis"
archive_base_dir = "/Users/shutchens/Archive"

archive_dir = project_manager.archive_project(project_path=project_path, archive_base_dir=archive_base_dir)
```

Delete a project:

```python
# Path to the project to delete
project_path = "/Users/shutchens/Documents/Git-Repos/labrat/karg_analysis"
archive_base_dir = "/Users/shutchens/Archive"

# Delete the project
archived_path = project_manager.delete_project(project_path, archive_base_dir)
```

## ToDo

- [ ] Add a lab inventory app
- [ ] Add project report template
- [ ] Command-line functionality
- [ ] Integrate [exmemo](https://github.com/kalekundert/exmemo)

## Author

Shaurita Hutchins · [@sdhutchins](https://github.com/sdhutchins)
    · [:email:](mailto:shaurita.d.hutchins@gmail.com)

## Contributing

If you would like to contribute to this package, install the package in
development mode, and check out our [contributing
guidelines](https://github.com/sdhutchins/labrat/blob/master/CONTRIBUTING.md).

## License

[MIT](https://github.com/sdhutchins/labrat/blob/master/LICENSE)

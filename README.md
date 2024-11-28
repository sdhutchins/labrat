# labrat

[![Build Status](https://travis-ci.com/sdhutchins/labrat.svg?branch=master)](https://travis-ci.com/sdhutchins/labrat)

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

*This package is compatible with python 3.4 and up.*

## Examples

### Dilute a stock concentration

```python
from labrat.math import dilute_stock

# Get the final concentration
dilute_stock(100, 2, **{'vF': 4})
```

<br>

### Create a new computational biology project

```python
import os
from labrat.project import ProjectManager

# Initialize the ProjectManager with a username
project_manager = ProjectManager('Dr. Jane Doe')

# Create a new project
project_manager.new_project(
    project_type='computational-biology',  # Valid project type
    project_name='KARG Analysis',  # Includes a space to test sanitization
    project_path=os.getcwd(),  # Current working directory
    description="Analyze the KARG data."
)
```

## ToDo

- [ ] Add a lab inventory app
- [ ] Add project report template
- [ ] Command-line functionality
- [ ] Integrate [exmemo](https://github.com/kalekundert/exmemo)

## Author

Shaurita Hutchins · [@sdhutchins](https://github.com/sdhutchins)
    · [:email:](mailto:sdhutchins@outlook.com)

## Contributing

If you would like to contribute to this package, install the package in
development mode, and check out our [contributing
guidelines](https://github.com/sdhutchins/labrat/blob/master/CONTRIBUTING.md).

## License

[MIT](https://github.com/sdhutchins/labrat/blob/master/LICENSE)

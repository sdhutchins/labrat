# labrat
[![Build Status](https://travis-ci.org/sdhutchins/labrat.svg?branch=master)](https://travis-ci.org/sdhutchins/labrat)

A package of helpful guis and functions for genetics/psychiatry related labs. This package is in the very early stages of development.

## Features

- Easily use math functions to dilute solutions, calculate molarity, etc.
- Backup your documents with an easy one-liner
- Manage lab inventory
- Create and manage new projects

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
from labrat.project import ProjectManager
projectmanager = ProjectManager('Dr. Jane Doe')
projectmanager.newproject(project_type='computational-biology',
                          project_name='KARG Analysis',
                          project_path=os.getcwd())
```

## ToDo

- [ ] Add a lab inventory app/gui
- [ ] Add project report template
- [ ] Add GraphPad Prism 7 scripts
- [ ] Command line functionality

## Author

Shaurita Hutchins · [@sdhutchins](https://github.com/sdhutchins)
    · [:email:](mailto:sdhutchins@outlook.com)

## Contributing

If you would like to contribute to this package, install the package in
development mode, and check out our [contributing
guidelines](https://github.com/sdhutchins/labrat/blob/master/CONTRIBUTING.rst).

## License

[MIT](https://github.com/sdhutchins/labrat/blob/master/LICENSE)
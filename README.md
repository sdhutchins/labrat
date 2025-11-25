# labrat

[![Build Status](https://app.travis-ci.com/sdhutchins/labrat.svg?token=xfnbNTQhjNbir5xACn8R&branch=master)](https://app.travis-ci.com/sdhutchins/labrat)
[![codecov](https://codecov.io/gh/sdhutchins/labrat/graph/badge.svg?token=LqA1Lqf0uu)](https://codecov.io/gh/sdhutchins/labrat)
[![DOI](https://zenodo.org/badge/99277244.svg)](https://doi.org/10.5281/zenodo.17705600)

A basic science lab framework aimed at reproducibility and lab management. This package is in the very early stages of development.

## Features

- Create, list, and track/manage computational biology projects with structured templates
- Calculate solution dilutions, molarity, transmittance/absorbance conversions, and more
- Automatically organize scientific data files (FASTQ, FASTA, SAM, BAM, VCF, etc.) and others files like pictures, videos, and archives
- Archive projects and directories with timestamped backups
- Convert DNA sequences to amino acids and analyze genetic data
- Full-featured CLI for all major operations

## Install

Install from PyPI:
```bash
pip install pylabrat
```

Or install from source:
```bash
git clone https://github.com/sdhutchins/labrat.git
cd labrat
pip install .
```

For development, install in editable mode:
```bash
pip install -e .
```

## Examples

### Command-Line Interface

Create a new project:
```bash
labrat project new --type computational-biology --name "KARG Analysis" \
  --path ./karg_analysis --description "Analyze the KARG data"
```

List all projects:
```bash
labrat project list
```

Archive files or directories:
```bash
labrat archive --source ./my_project --destination ~/Archive --name "project_backup"
```

Organize scientific data files:
```bash
labrat organize --science
```

### Python API

Calculate solution dilutions:
```python
from labrat.math import dilute_stock

# Calculate final concentration
final_conc = dilute_stock(100, 2, vF=4)  # Returns 50.0
```

Manage projects programmatically:
```python
from labrat.project import ProjectManager

# Create a new project
manager = ProjectManager('Dr. Jane Doe')
manager.new_project(
    project_type='computational-biology',
    project_name='KARG Analysis',
    project_path='./karg_analysis',
    description="Analyze the KARG data."
)

# List all projects
projects = manager.list_projects()
```

## Tests

Before running tests, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

Or if installing the package:

```bash
pip install .
```

Run all tests using unittest:

```bash
python -m unittest discover -s tests
```

Or run tests with pytest (if installed):

```bash
pytest tests/
```

To run a specific test file:

```bash
python -m unittest tests.test_archiver
python -m unittest tests.test_file_organizer
python -m unittest tests.test_project_manager
```

## ToDo

- [ ] Add a lab inventory app
- [ ] Add project report template
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

<div align="center">
  <img
    src="https://raw.githubusercontent.com/sdhutchins/labrat/main/assets/labrat-logo.png"
    alt="Labrat logo"
    width="175"
  >

[![Test Package Build](https://github.com/sdhutchins/labrat/actions/workflows/test-build.yml/badge.svg?branch=main)](https://github.com/sdhutchins/labrat/actions/workflows/test-build.yml)
[![codecov](https://codecov.io/gh/sdhutchins/labrat/graph/badge.svg?token=LqA1Lqf0uu)](https://codecov.io/gh/sdhutchins/labrat)
[![PyPI - Version](https://img.shields.io/pypi/v/pylabrat)](https://pypi.org/project/pylabrat/)
[![DOI](https://zenodo.org/badge/99277244.svg)](https://doi.org/10.5281/zenodo.17705600)
</div>

# labrat

Labrat is a Python framework designed to improve reproducibility, simplify
laboratory management, and support common biomedical research tasks.

## Features

- Create, list, and track computational biology projects from reusable templates
- Calculate solution dilutions, molarity, transmittance/absorbance conversions, and more
- Organize scientific data, images, videos, and archives by file type
- Archive projects and directories with timestamped backups
- Count canonical nucleotides, create DNA complements, and translate FASTA sequences
- Query gene, variant, and biomedical literature resources with provenance
- Use the same tools from the command line or Python

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

Query genes through MyGene, variants through MyVariant, and literature through
PubTator 3:

```bash
labrat query gene BMPR2
labrat query gene BMPR2 --all-matches
labrat query variant rs429358
labrat query literature "BMPR2 pulmonary arterial hypertension"
labrat query literature --gene BMPR2 \
  --disease "pulmonary arterial hypertension"
```

Add `--format json` to retain the complete provider response and query
provenance for downstream analysis. The default output uses terminal-aware
Rich tables and panels that remain readable when output is redirected.

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

## Documentation

The complete documentation is available at
[www.shauritahutchins.com/labrat](https://www.shauritahutchins.com/labrat/).

Great Docs requires Python 3.11 or later and Quarto. Build the documentation
locally with:

```bash
pip install -e ".[docs]"
great-docs build
```

The generated site is written to `great-docs/_site/` and is not committed.

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

## Roadmap

- [ ] Add a lab inventory app
- [ ] Add project report template
- [ ] Integrate [exmemo](https://github.com/kalekundert/exmemo)

## Author

Shaurita Hutchins · [@sdhutchins](https://github.com/sdhutchins)
    · [:email:](mailto:shaurita.d.hutchins@gmail.com)

## Contributing

If you would like to contribute to this package, install the package in
development mode, and check out our [contributing
guidelines](https://github.com/sdhutchins/labrat/blob/main/CONTRIBUTING.md).

## License

[MIT](https://github.com/sdhutchins/labrat/blob/main/LICENSE)

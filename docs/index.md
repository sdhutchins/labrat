# labrat

A basic science lab framework aimed at reproducibility and lab management.

## Features

- Math functions for dilutions, molarity calculations, and more
- Command-line tools for archiving and organizing files
- Project management for computational biology workflows
- DNA and protein analysis utilities

## Quick Start

Install labrat:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Usage

### Command Line

```bash
# Create a new project
labrat project new --type computational-biology --name "My Project"

# List projects
labrat project list

# Archive a directory
labrat archive --source /path/to/source --destination /path/to/archive --name project_name

# Organize files
labrat organize --science --all
```

### Python API

```python
from labrat.math import dilute_stock

# Calculate final concentration
final_conc = dilute_stock(100, 2, vF=4)
```

## Documentation

- [Installation Guide](installation.md)
- [CLI Reference](cli.md)
- [API Reference](api.md)

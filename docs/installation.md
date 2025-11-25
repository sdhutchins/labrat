# Installation

## Requirements

- Python 3.8 or higher
- pip

## Install from Source

1. Clone the repository:

```bash
git clone https://github.com/sdhutchins/labrat.git
cd labrat
```

2. Install the package:

```bash
pip install .
```

For development mode:

```bash
pip install -e .
```

## Install Dependencies

Install all required dependencies:

```bash
pip install -r requirements.txt
```

## Install Documentation Dependencies

To build and serve the documentation locally:

```bash
pip install -e ".[docs]"
```

Or install manually:

```bash
pip install mkdocs-material mkdocs-click mkdocstrings[python] pymdown-extensions
```

## Verify Installation

Run the tests to verify everything is working:

```bash
pytest tests/
```

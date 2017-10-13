# labrat
[![Build Status](https://travis-ci.com/sdhutchins/lab-management.svg?token=xfnbNTQhjNbir5xACn8R&branch=master)](https://travis-ci.com/sdhutchins/lab-management)

A package of helpful guis and functions for genetics/psychiatry related labs. This package is in the very early stages of development.

## Features
- Easily math functions to dilute solutions.

<br>

## Install
1. Clone this repository.
2. Change to the downloaded repository's base directory.
3. `pip install .`

If you want to develop or contribute to this package, install with `pip install -e .`

*This package is compatible with python 3.4 and up.*

## Examples

#### *Dilute a stock concentration*
```python
from labrat.math import dilute_stock

# Get the final concentration
dilute_stock(100, 2, **{'vF': 4})
```
<br>

## TODO
- Add a lab inventory app/gui
- Add project report template
- Add GraphPad Prism 7 scripts
- Command line functionality
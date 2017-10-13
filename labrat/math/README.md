## math
This labrat module includes common lab (molecular and otherwise) functions.

### Examples

*Dilute a stock concentration*
```python
from labrat.math import dilute_stock

# Get the final concentration
dilute_stock(100, 2, **{'vF': 4})
Out[71]: 50.0

# Get the final concentration
dilute_stock(100, 2, **{'cF': 50})
Out[71]: 4.0
```
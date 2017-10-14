import math
import numbers

"""Reusable math functions for the molecular scientists."""


def dilute_stock(cI, vI, **values):
    """Dilute a stock concentration."""
    if not values:
        raise UserWarning('You did not enter any values.')
    for key, value in values.items():
        if key == 'vF' or 'vf':
            value = values['vF']
            final_concentration = (cI * vI) / value
            return final_concentration
        elif key == 'cF' or 'cf':
            value = values['cF']
            final_volume = (cI * vI) / value
            return final_volume
        else:
            raise KeyError('%s is not a valid key.' % key)


def transmittance_to_absorbance(T):
    if isinstance(T, numbers.Number):
        T = T / 100
        return math.log(T ** -1)
    else:
        raise UserWarning("{} must be a number (percentage).")

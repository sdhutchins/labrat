"""Reusable math functions for the molecular scientists."""


def dilute_stock(cI, vI, **values):
    """Dilute a stock concentration."""
    if not values:
        raise UserWarning('You did not enter any values.')
    for key, value in values.items():
        if key == 'vF' or 'vf':
            value = values['vF']
            final_concentration = (cI*vI)/value
            return final_concentration
        elif key == 'cF' or 'cf':
            value = values['cF']
            final_volume = (cI*vI) / value
            return final_volume
        else:
            raise KeyError('%s is not a valid key.' % key)
            
# Calculate the molarity of a solution given moles and liters or milliliters
def calculate_molarity(moles, volume, unit_of_volume):
    if (unit_of_volume == 'ml' or unit_of_volume == 'mL'):
        volume = volume * 1000
    elif (unit_of_volume != 'l' and unit_of_volume != 'L'):
        raise UserWarning('This unit of measurement is not supported.')
    return moles/volume            

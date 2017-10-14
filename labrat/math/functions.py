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
 
def mass_recorder(grams, item, Sigfigs):
    "Record the mass of different items"
    item_Dict = {}
    if isinstance(grams, float) and isinstance(item, str) and isinstance(Sigfigs, int):
        if item in item_Dict:
            formatter = "{0:."+Str(Sigfigs)+"f}"
            grams = formatter.format(grams)
            item_Dict[item] = grams
        else:
            formatter = "{0:."+Str(Sigfigs)+"f}"
            grams = formatter.format(grams)
            item_Dict[item]+= grams
    else:
        raise UserWarning('Please print grams as a float value, item as a string, and sigfigs as an integer value")

"""Reusable math functions for the molecular scientists."""
import math
import numbers


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


def mass_recorder(grams, item, sigfigs):
    """Record the mass of different items."""
    item_dict = {}
    if isinstance(grams, float) and isinstance(item, str) and isinstance(sigfigs, int):
        if item in item_dict:
            formatter = "{0:." + str(Sigfigs) + "f}"
            grams = formatter.format(grams)
            item_Dict[item] = grams
        else:
            formatter = "{0:." + str(sigfigs) + "f}"
            grams = formatter.format(grams)
            item_dict[item] += grams
    else:
        raise ValueError('Please input grams as a float value, item as a string, and sigfigs as an integer value")


def transmittance_to_absorbance(transmittance):
    if isinstance(transmittance, numbers.Number):
        t = transmittance / 100
        return math.log(t ** -1)
    else:
        raise ValueError("{} must be a number (percentage).")


def calculate_molarity(moles, volume, units):
    """Calculate the molarity of a solution given moles and liters or mL."""
    if (units == 'ml' or units == 'mL'):
        volume = volume * 1000
    elif (units != 'l' and units != 'L'):
        raise ValueError('This unit of measurement is not supported.')
    return moles/volume


def refractive_index_prism(prism, deviation, angle_measurement):
    """Calculate the refractive index of prism.

    This function uses the angle of prism and minimum angle of deviation.
    """
    if (angle_measurement == 'rad'):
        refractive_index = (math.sin((prism + deviation) / 2)) / math.sin(prism / 2)
        return refractive_index

    elif (angle_measurement == 'deg'):
        p = math.radians(prism)
        d = math.radians(deviation)
        refractive_index = (math.sin((p + d)/2)) / math.sin(p/2)
        return refractive_index

    else:
        raise ValueError('The angle measurement has to be in deg or rad format.')

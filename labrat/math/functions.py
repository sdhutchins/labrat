"""Reusable math functions for scientists."""
import math
import numbers


def dilute_stock(cI, vI, **values):
    """Dilute a stock concentration.

    Args:
        cI ([type]): [description]
        vI ([type]): [description]

    Raises:
        UserWarning: [description]
        KeyError: [description]

    Returns:
        [type]: [description]
    """
    if not values:
        raise UserWarning('You did not enter any values.')
    for key, value in values.items():
        if key in ('vF', 'vf'):
            final_concentration = (cI * vI) / value
            return final_concentration
        elif key in ('cF', 'cf'):
            final_volume = (cI * vI) / value
            return final_volume
        else:
            raise KeyError('%s is not a valid key.' % key)


def mass_recorder(grams, item, sigfigs):
    """Record the mass of different items.

    Args:
        grams ([type]): [description]
        item ([type]): [description]
        sigfigs ([type]): [description]

    Raises:
        ValueError: [description]
    """
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
        raise ValueError('Please input grams as a float value, item as a string, and sigfigs as an integer value')


def transmittance_to_absorbance(transmittance):
    """Convert transmittance to absorbance.

    Args:
        transmittance ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if isinstance(transmittance, numbers.Number):
        if transmittance == 0:
            return float('inf')
        t = transmittance / 100
        return math.log(t ** -1)
    else:
        raise ValueError("{} must be a number (percentage).")


def calculate_molarity(moles, volume, units):
    """Calculate the molarity of a solution given moles and liters or mL.

    Args:
        moles ([type]): [description]
        volume ([type]): [description]
        units ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if (units == 'ml' or units == 'mL'):
        volume = volume * 1000
    elif (units != 'l' and units != 'L'):
        raise ValueError('This unit of measurement is not supported.')
    return moles / volume


def refractive_index_prism(prism, deviation, angle_measurement):
    """Calculate the refractive index of prism.

    This function uses the angle of prism and minimum angle of deviation.

    Args:
        prism ([type]): [description]
        deviation ([type]): [description]
        angle_measurement ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    if (angle_measurement == 'rad'):
        refractive_index = (math.sin((prism + deviation) / 2)) / math.sin(prism / 2)
        return refractive_index

    elif (angle_measurement == 'deg'):
        p = math.radians(prism)
        d = math.radians(deviation)
        refractive_index = (math.sin((p + d) / 2)) / math.sin(p / 2)
        return refractive_index

    else:
        raise ValueError('The angle measurement has to be in deg or rad format.')

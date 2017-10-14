"""Reusable math functions for the molecular scientists."""
import math

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

def refractive_index_prism(A, D, angle_measurement)
	"""Calculate the refractive index of prism using angle of prism and minimum angle of deviation."""
	
	if (angle_measurement == 'rad'):
		refractive_index = (math.sin((A + D)/2)) / math.sin(A/2)
		return refractive_index
			
	elif (angle_measurement == 'deg'):
		A = math.radians(A)
		D = math.radians(D)
			
		refractive_index = (math.sin((A + D)/2)) / math.sin(A/2)
		return refractive_index

	else:
		raise ValueError('The angle measurement has to be done in deg or rad format.')

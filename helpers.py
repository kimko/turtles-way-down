import re
import numpy as np

def recode_species(species_value):
    """Takes a string and returns classified species"""
    if species_value in ['Cpb', 'C.p.b.']:
        return 'Cpb'
    elif species_value in ['Red-eared slider', 'RES']:
        return 'Res'
    else:
        return 'unknown'

def recode_sex(sex_value):
    """Takes a string and returns f, m or unknown"""
    if sex_value in ['Male','male?','m','M']:
        return 'm'
    elif sex_value in ['Female','F','f']:
        return 'f'
    else:
        return 'unknown'

def recode_decimal(dirty_decimal=''):
    """Takes a string and returns a decimal"""
    _ = []
    if not dirty_decimal:
        return 0
    if str(dirty_decimal):
        _ = re.findall(r"[-+]?\d*\.\d+|\d+",str(dirty_decimal))
    if _:
        return _[0]
    else:
        return 0

def ecdf(data):
        """Compute ECDF for a one-dimensional array of measurements."""
        # Number of data points: n
        n = len(data)
        # x-data for the ECDF: x
        x = np.sort(data)
        # y-data for the ECDF: y
        y = np.arange(1, len(x)+1) / len(x)
        return x, y
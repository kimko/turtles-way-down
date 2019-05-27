import re
import numpy as np


def recode_species(species_value):
    """Takes a string and returns classified species"""
    if species_value in ['Cpb', 'cpb', 'C.p.b.']:
        return 'Cpb'
    elif species_value in ['Red-eared slider', 'RES', 'REs']:
        return 'Res'
    else:
        return species_value


def recode_gravid(gravid_value):
    if str(gravid_value).upper() == "YES":
        return True
    else:
        return False


def recode_sex(sex_value):
    """Takes a string and returns f, m or unknown"""
    if sex_value in ['Male', 'male?', 'm', 'M']:
        return 'm'
    elif sex_value in ['Female', 'F', 'f']:
        return 'f'
    else:
        return 'unknown'


def recode_season(date):
    if date.month <= 6:
        return 'spr'
    else:
        return 'fal'


def recode_decimal(dirty_decimal=''):
    """Takes a string and returns a decimal"""
    _ = []
    if not dirty_decimal:
        return 0
    if str(dirty_decimal):
        _ = re.findall(r"[-+]?\d*\.\d+|\d+", str(dirty_decimal))
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
    y = np.arange(1, n + 1) / n
    return x, y


def permutation_sample(data1, data2):
    """Generate a permutation sample from two data sets."""
    """simulate the hypothesis that two variables have identical probability distributions."""
    # Concatenate the data sets: data
    data = np.concatenate((data1, data2))

    # Permute the concatenated array: permuted_data
    permuted_data = np.random.permutation(data)

    # Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]

    return perm_sample_1, perm_sample_2

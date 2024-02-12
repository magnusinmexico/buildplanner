# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_utils.py
# Author: Magnus Pettersson
#
# This module provides utility functions for rounding numbers, checking list
# contents, and converting data structures. It includes functions for rounding
# individual values, rounding vectors of values, checking if lists contain
# specific types of elements, and converting keys in dictionaries to floats.
#
#------------------------------------------------------------------------------

def sround(value: float, significance: int) -> float:
    """
    Round a floating-point number to a specified number of significant digits.

    Args:
        value (float): The value to round.
        significance (int): The number of significant digits.

    Returns:
        float: The rounded value.
    """
    return float(f"{value:.{significance - 1}e}")


def svround(vect: list[float], significance: int) -> tuple:
    """
    Round each element of a vector to a specified number of significant digits.

    Args:
        vect (list[float]): The vector of values to round.
        significance (int): The number of significant digits.

    Returns:
        tuple: The rounded vector.
    """
    rounded_vect = []
    for i in range(len(vect)):
        rounded_vect.append(sround(vect[i], significance))
    return tuple(rounded_vect)


def vround(vect: list[float], precision: int) -> tuple:
    """
    Round each element of a vector to a specified precision.

    Args:
        vect (list[float]): The vector of values to round.
        precision (int): The number of decimal places to round to.

    Returns:
        tuple: The rounded vector.
    """
    rounded_vect = []
    for i in range(len(vect)):
        rounded_vect.append(round(vect[i], precision))
    return tuple(rounded_vect)


def list_contains_numbers(lst):
    """
    Check if all elements in a list are numbers (integers or floats).

    Args:
        lst: The list to check.

    Returns:
        bool: True if all elements are numbers, False otherwise.
    """
    return all(isinstance(item, (int, float)) for item in lst)


def list_contains_dicts(lst):
    """
    Check if all elements in a list are dictionaries.

    Args:
        lst: The list to check.

    Returns:
        bool: True if all elements are dictionaries, False otherwise.
    """
    return all(isinstance(item, dict) for item in lst)


def dict_contains_number_keys_and_int_values(d):
    """
    Check if a dictionary contains number keys and integer values.

    Args:
        d: The dictionary to check.

    Returns:
        bool: True if all keys are numbers and all values are integers, False 
              otherwise.
    """
    return all(isinstance(key, (int, float)) and isinstance(value, int) for key, value in d.items())


def convert_keys_to_float(d):
    """
    Convert dictionary keys to floats.

    Args:
        d: The dictionary whose keys are to be converted.

    Returns:
        dict: The dictionary with float keys.
    """
    return {float(key): value for key, value in d.items()}


def convert_list_elements_to_float(lst):
    """
    Convert each element in a list to a float.

    Args:
        lst: The list to convert.

    Returns:
        list: The list with float elements.
    """
    return [float(item) for item in lst]


def make_list_quantitative_dict(lst):
    """
    Create a dictionary where keys are unique elements from a list and values
    represent the frequency of each element in the list.

    Args:
        lst: The list of values.

    Returns:
        dict: A dictionary where keys are unique elements from the list and
              values represent the frequency of each element.
    """
    d = {}
    for n in lst:
        if float(n) in d:
            d[float(n)] += 1
        else:
            d[float(n)] = 1
    return d

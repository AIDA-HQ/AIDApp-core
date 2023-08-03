"""This module contains the functions that handle the input and output data."""

from numpy import array, reshape, transpose
from aidapp.utils import rd


def generate_array(coordinate_file):
    """
    This function takes a string containing values separated
    one from the other by a newline and returns a numpy array.
    """
    # Strip \n and \t from text
    data = filter(None, coordinate_file.splitlines())
    data_array = [float(element.replace(",", ".")) for element in data]
    return rd(data_array)


def generate_zonation_array(zonation_data):
    """
    This function takes a string containing 3 columns of numbers, each
    separated by a space from the following one and generate 3 arrays.
    Converts the commas to dots too.
    """
    # Strip \n and \t from text
    filtered_data = filter(None, zonation_data.splitlines())
    data = [element.replace(",", ".").split() for element in filtered_data]
    zonation_array = [float(item) for sublist in data for item in sublist]
    return transpose(reshape(array(zonation_array), (9, 3)))


def generate_storey_data(storey_input_data):
    """
    This function takes a string containing a column
    of numbers to generate a lists of floats.
    Converts the commas to dots too.
    """
    # Strip \n and \t from text
    data = filter(None, storey_input_data.splitlines())
    storey_data = [float(element.replace(",", ".")) for element in data]
    return storey_data

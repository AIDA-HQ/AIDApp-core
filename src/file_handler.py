"""This module contains the functions that handle the input and output data."""

from numpy import array, reshape, transpose
from qtpy import QtWidgets


class InputHandler:
    """This class contains the functions that handle the input data."""

    @staticmethod
    def generate_array(coordinate_file):
        """
        This function takes a string containing values separated
        one from the other by a newline and returns a numpy array.
        """
        # Strip \n and \t from text
        data = filter(None, coordinate_file.splitlines())
        array = [float(element.replace(",", ".")) for element in data]
        return array

    @staticmethod
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

    @staticmethod
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


class ExportHandler:
    """This class contains the functions that handle the output data."""

    @staticmethod
    def generate_output_file(kc_n_s_array_arg, Fc_n_s_array_arg):
        """
        This function takes two arrays and generates a file containing
        the values of the kc and Fc for each story.
        """
        name_dialog, _ = QtWidgets.QFileDialog.getSaveFileName(
            caption="Save File", filter="Text Files(*.txt)"
        )

        kc_n_s_array = "kc,i,s array: \n"
        for element in kc_n_s_array_arg:
            kc_n_s_array += str(element) + "\n"
        Fc_n_s_array = "Fc,i,s array: \n"
        for element in Fc_n_s_array_arg:
            Fc_n_s_array += str(element) + "\n"
        if name_dialog:
            with open(name_dialog, "w") as f:
                f.write(kc_n_s_array + "\n" + Fc_n_s_array)

from numpy import loadtxt, float_
from qtpy import QtWidgets


class InputHandler:
    @staticmethod
    def generate_pushover_array(coordinate_file):
        """
        This function takes a string containing coordinates separated
        one from the other by a newline and returns a numpy array.
        """
        # Strip \n and \t from text
        data = filter(None, coordinate_file.splitlines())
        pushover_array = [float(element.replace(",", ".")) for element in data]
        return pushover_array

    @staticmethod
    def generate_zonation_array(coordinate_file):
        """
        This function takes a file containing 3 coloumns of numbers, each
        separated by a space from the following one and generate 3 arrays.
        Converts the commas to a dots too.
        """
        zonation_array = loadtxt(
            fname=coordinate_file,
            converters={
                0: lambda s: float(s.decode("UTF-8").replace(",", ".")),
                1: lambda s: float(s.decode("UTF-8").replace(",", ".")),
                2: lambda s: float(s.decode("UTF-8").replace(",", ".")),
            },
            unpack=True,
        )
        return zonation_array

    @staticmethod
    def generate_storey_data(storey_input_data):
        """
        This function takes a string containing a coloumn
        of numbers to generate a lists of floats.
        Converts the commas to dots too.
        """
        data = storey_input_data.splitlines()
        # Strip \n and \t from text
        data = filter(None, data)
        data = [element.replace(",", ".") for element in data]
        return list(float_(data))


class ExportHandler:
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

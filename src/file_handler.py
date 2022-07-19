from numpy import loadtxt
from qtpy import QtWidgets


class InputHandler:
    @staticmethod
    def generate_pushover_array(coordinate_file):
        """
        This function takes a file containing coordinates separated
        one from the other by a newline and returns a numpy array.
        """
        pushover_array = loadtxt(
            fname=coordinate_file,
            delimiter="\n",
            converters={0: lambda s: float(s.decode("UTF-8").replace(",", "."))},
        )
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
    def generate_storey_data(storey_input_data_file):
        """
        This function takes a file containing a coloumns of numbers,
        divided in 3 groups, each group separated by a comment from
        the preceding one and generate 3 lists of floats.
        Converts the commas to a dots too.
        """
        mass_line = "#### Storey Masses ####"
        eigenvalues_line = "#### Storey Eigenvalues ####"
        upwinds_line = "#### Storey Upwinds ####"
        dict = {}

        with open(storey_input_data_file, "r") as f:
            values = [
                line.strip() for line in f.readlines()
            ]  # Strip \n and \t from text
            values = list(filter(None, values))
            values = [element.replace(",", ".") for element in values]

            for i, line in enumerate(
                values
            ):  # enumerate will count and keep track of the lines
                if line == mass_line:
                    dict[mass_line] = i
                elif line == eigenvalues_line:
                    dict[eigenvalues_line] = i
                elif line == upwinds_line:
                    dict[upwinds_line] = i

            masses = [
                float(element)
                for element in (values[dict[mass_line] + 1 : dict[eigenvalues_line]])
            ]
            eigenvalues = [
                float(element)
                for element in (values[dict[eigenvalues_line] + 1 : dict[upwinds_line]])
            ]
            upwinds = [float(element) for element in (values[dict[upwinds_line] + 1 :])]

            return masses, eigenvalues, upwinds


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

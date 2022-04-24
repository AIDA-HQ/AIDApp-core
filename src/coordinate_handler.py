from numpy import loadtxt


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

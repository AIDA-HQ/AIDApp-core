from numpy import loadtxt


class CoordinateHandler:
    @staticmethod
    def generate_array(coordinate_file):
        """
        This function takes a file containing coordinates separated
        one from the other by a newline and returns a numpy array.
        """
        array = loadtxt(
            fname=coordinate_file,
            delimiter="\n",
            converters={0: lambda s: float(s.decode("UTF-8").replace(",", "."))},
        )
        return array

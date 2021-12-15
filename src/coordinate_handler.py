from numpy import fromfile, float64
import warnings
warnings.filterwarnings("error")

class CoordinateHandler:

    def generate_array(self, coordinate_file):
        """
        This function takes a file containing coordinates (with the dot as decimal 
        separator) separated one from the other by commas and returns a numpy array.
        """
        try:
            return fromfile(file=coordinate_file, sep=',')
        except DeprecationWarning:
            return "Something wrong happened, check your file"

from numpy import loadtxt

class CoordinateHandler:
  
    def generate_array(self, coordinate_file):
        """
        This function takes a file containing coordinates separated 
        one from the other by a newline and returns a numpy array.
        """
        return loadtxt(fname=coordinate_file, delimiter='\n', converters = {0: lambda s: float(s.decode("UTF-8").replace(",", "."))})

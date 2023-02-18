"""Coordinates module."""
from numpy import absolute, array, linspace, polyfit, column_stack
from shapely.geometry.linestring import LineString


class Coords:
    """Class to calculate coordinates of the curves."""

    @staticmethod
    def y_kn_eff(sd_m, kn_eff):
        """
        Calculate the y coordinates of kn_eff curve (line),
        by taking the sd_m value list and kn_eff as input values.
        """
        return array([element * kn_eff for element in sd_m])

    # Generate SDOF pushover curve
    @staticmethod
    def x_p_sdof(gamma, x_p_mdof):
        """Return the x coordinates of the SDOF pushover curve."""
        return array([element / gamma for element in x_p_mdof])

    @staticmethod
    def y_p_sdof(gamma, y_p_mdof):
        """Return the y coordinates of the SDOF pushover curve."""
        return array([element / gamma for element in y_p_mdof])

    ##

    @staticmethod
    def x_bilinear_line(start_graph, end_graph):
        """Return the x coordinates of the bilinear line."""
        return linspace(start_graph, end_graph, 1000)

    @staticmethod
    def find_intersections(curve_1, curve_2):
        """Find the intersection points of two curves."""
        intersection = curve_1.intersection(curve_2)
        intersection_coords = []
        if intersection.geom_type == "Point":
            intersection_coords.append((intersection.x, intersection.y))
        if intersection.geom_type == "MultiPoint":
            individual_points = [(pt.x, pt.y) for pt in intersection.geoms]
            for element in individual_points:
                intersection_coords.append(element)
        return intersection_coords

    @staticmethod
    def find_nearest_coordinate_index(curve_coordinates, coord):
        """Find the index of the minimum/lowest element from the array."""
        difference_array_x = absolute(curve_coordinates - coord)
        index = difference_array_x.argmin()
        return index

    def find_nearest_coordinate(self, curve_coordinates, coord):
        """
        Enter array of X or Y coordinates of a curve and X or Y coordinate of
        a point_a to find the nearest X or Y point_a to in the curve array.
        """
        index = self.find_nearest_coordinate_index(curve_coordinates, coord)
        return curve_coordinates[index]

    @staticmethod
    def bilinear_m_q(x_1, x_2, y_1, y_2):
        """
        Enter coordinates of two points.
        Returns a tuple with m and q to generate one
        straight line which composes the bilinear line.
        """
        m, q = polyfit(x=[x_1, x_2], y=[y_1, y_2], deg=1)
        return m, q

    def generate_line(self, x_p_sdof, x_1_array, x_2_array, y_1_array, y_2_array):
        """
        Generate part of the bilinear curve: 1st or 2nd line that compose it.
        Returns a tuple with X and Y coordinates.
        """
        m = self.bilinear_m_q(x_1_array, x_2_array, y_1_array, y_2_array)[0]
        q = self.bilinear_m_q(x_1_array, x_2_array, y_1_array, y_2_array)[1]
        x = self.x_bilinear_line(x_p_sdof[0], x_p_sdof[-1])
        y = m * x + q
        return x, y

    @staticmethod
    def interpolate_curve(x_coords, y_coords):
        """Interpolate the curve."""
        curve = LineString(column_stack((x_coords, y_coords)))
        return curve

    def find_range_pushover(self, pushover_coord, line_1_coord, line_2_coord):
        """
        Method to list all the coordinates defined by
        the two intersections with the bilinear curve.
        """
        index_0 = self.find_nearest_coordinate_index(pushover_coord, line_1_coord)
        index_1 = self.find_nearest_coordinate_index(pushover_coord, line_2_coord)
        list_fitting = [pushover_coord[index_0 : index_1 + 1]]
        return list_fitting

    def bilinear_line(
        self,
        x_p_sdof,
        x_bilinear_coord_0,
        x_bilinear_coord_1,
        y_bilinear_coord_0,
        y_bilinear_coord_1,
    ):
        """Generate the bilinear line."""
        x_bilinear_line = self.generate_line(
            x_p_sdof,
            x_bilinear_coord_0,
            x_bilinear_coord_1,
            y_bilinear_coord_0,
            y_bilinear_coord_1,
        )[0]
        y_bilinear_line = self.generate_line(
            x_p_sdof,
            x_bilinear_coord_0,
            x_bilinear_coord_1,
            y_bilinear_coord_0,
            y_bilinear_coord_1,
        )[1]
        bilinear_line = self.interpolate_curve(x_bilinear_line, y_bilinear_line)
        return bilinear_line

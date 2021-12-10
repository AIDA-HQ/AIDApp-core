import numpy as np
from shapely.geometry.linestring import LineString
from input_coordinates import Input

input_coord = Input()


class Coords:
    @staticmethod
    def y_kn_eff(sd_m, kn_eff):
        """
        Calculate the y coordinates of kn_eff curve (line),
        by taking the sd_m value list and kn_eff as input values.
        """
        y_kn_eff_list = []
        for element in sd_m:
            new_coord = element * kn_eff
            y_kn_eff_list.append(new_coord)
        return np.array(y_kn_eff_list)

    # Generate SDOF pushover curve
    @staticmethod
    def x_p_sdof(gamma):
        x_p_sdof_list = []
        for element in input_coord.x_p_mdof:
            new_coord = element / gamma
            x_p_sdof_list.append(new_coord)
        return np.array(x_p_sdof_list)

    @staticmethod
    def y_p_sdof(gamma):
        y_p_sdof_list = []
        for element in input_coord.y_p_mdof:
            new_coord = element / gamma
            y_p_sdof_list.append(new_coord)
        return np.array(y_p_sdof_list)

    ##

    @staticmethod
    def x_bilinear_line(start_graph, end_graph):
        return np.linspace(start_graph, end_graph, 1000)

    @staticmethod
    def find_intersections(curve_1, curve_2):
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
        """
        Find the index of the minimum/lowest element from the array.
        """
        difference_array_x = np.absolute(curve_coordinates - coord)
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
        m, q = np.polyfit(x=[x_1, x_2], y=[y_1, y_2], deg=1)
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
        curve = LineString(np.column_stack((x_coords, y_coords)))
        return curve

    def find_range_pushover(self, pushover_coord, line_1_coord, line_2_coord):
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
import matplotlib.pyplot as plt
from coordinates import Coords

coord = Coords()

# TODO Create different functions for different types of curves /kN, m/s^2, etc.)


class Graphs:
    def plot_all(
        self,
        x_bilinear,
        y_bilinear_ms2,
        x_p_sdof,
        y_p_sdof,
        x_bilinear_line_1,
        y_bilinear_line_1,
        x_bilinear_line_2,
        y_bilinear_line_2,
    ):

        plt.plot(coord.x_ADRS_meters, coord.y_ADRS_meters, label="ADRS meters curve")
        plt.plot(coord.x_K1_eff, coord.y_K1_eff, label="K1 eff curve")
        plt.plot(x_bilinear, y_bilinear_ms2, label="Bilinear curve in m/s^2")
        plt.plot(x_p_sdof, y_p_sdof, label="SDOF Pushover Curve")

        plt.plot(
            x_bilinear_line_1,
            y_bilinear_line_1,
            "-r",
            label="1st line of the bilinear curve",
        )
        plt.plot(
            x_bilinear_line_2,
            y_bilinear_line_2,
            "-r",
            label="2nd line of the bilinear curve",
        )
        plt.legend()

    def plot_pushover_bilinear(
        self,
        x_p_sdof,
        y_p_sdof,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
        intersection_dy_coords,
    ):
        plt.plot(x_p_sdof, y_p_sdof, label="SDOF Pushover Curve")
        self.plot_limited_bilinear(
            intersection_bilinear1_psdof_coords,
            intersection_bilinear2_psdof_coords,
            intersection_dy_coords,
        )

        plt.xlabel("Displacement* [m]", fontsize="large")
        plt.ylabel("Base Shear* [kN]", fontsize="large")

        plt.legend()

    def plot_intersections(self, intersection_list):
        if len(intersection_list) == 1:
            plt.plot(*zip(*intersection_list), "go", label="Intersection Point")
        if len(intersection_list) > 1:
            for element in intersection_list:
                plt.plot(*zip(*intersection_list), "go", label="Intersection Point")

    def plot_limited_bilinear(
        self,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
        intersection_dy_coords,
    ):
        points = []
        for element in intersection_bilinear1_psdof_coords:
            points.append(element)
        for element in intersection_bilinear2_psdof_coords:
            points.append(element)
        points.append(*intersection_dy_coords)
        tp = sorted(points, key=lambda x: x[0])
        plt.plot(*zip(*tp), "-o", color="red", label="Bilinear")
        plt.legend()

    def plot_final(self, x_bilinear, y_bilinear_ms2, sd_meters, sa_ms2, kn_eff_list, i):
        """
        Function to plot the final graph, meant to be displayed when 
        all the curves are calculated in the final iteration.
        """
        plt.plot(sd_meters, sa_ms2, color="#002260", label="ξ=5%")
        plt.plot(x_bilinear, y_bilinear_ms2, color="#FF0000", label="Bare Frame")
        plt.plot(
            sd_meters,
            kn_eff_list,
            color="#00B050",
            label=("K" + str(i) + "eff"),
        )
        plt.xlabel("Sd [m]", fontsize="large")
        plt.ylabel("Sa [m/s^2]", fontsize="large")
        plt.legend()

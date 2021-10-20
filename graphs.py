import numpy as np
import matplotlib.pyplot as plt
from coord import Coords

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
        plt.show()

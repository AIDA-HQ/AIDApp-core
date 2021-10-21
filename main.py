import numpy as np
from numpy import trapz
import matplotlib.pyplot as plt

from coordinates import Coords
from calcs import Calculations, Print
from graphs import Graphs

coord = Coords()
values = Calculations()
graphs = Graphs()
display = Print()


def find_dy(dy):
    # Store data from user input
    number_storeys = int(input("Enter the number of storeys: "))

    storey_masses = []
    eigenvalues = []

    i = 0
    while i < number_storeys:
        i = i + 1
        storey_masses.append(float(input("Enter the mass of storey #", i, ": ")))
    print("\n")
    n = 0
    while n < number_storeys:
        n = n + 1
        eigenvalues.append(float(input("Enter the eigenvalues #", n, ": ")))
    print("\n")

    # 3rd x coordinate of bilinear curve
    dp = float(input("\nEnter the value of d*p [m]: "))

    Γ = values.get_Γ(storey_masses, eigenvalues)
    me = values.get_me()  # [ton]
    y_p_sdof = coord.y_p_sdof(Γ)
    x_p_sdof = coord.x_p_sdof(Γ)

    Vp_kN = y_p_sdof[coord.find_nearest_coordinate_index(x_p_sdof, dp)]
    Vp_ms2 = Vp_kN / me  # ms2

    # Slope of first n values of SDOF Pushover Curve
    a = np.array([x_p_sdof[2:10]])
    b = np.array([y_p_sdof[2:10]])
    K1 = values.get_K1(a, b)  # kN
    Vy_kN = values.get_Vy_kN(K1, dy)

    # X coordinates of the bilinear curve
    x_bilinear = np.array([0, dy, dp])

    # Y coords of the bilinear curve in [kN]
    y_bilinear_kN = np.array([0, Vy_kN, Vp_kN])

    # Y coords of the bilinear curve in [m/s^2]
    y_bilinear_ms2 = np.array(
        [y_bilinear_kN[0] / me, y_bilinear_kN[1] / me, y_bilinear_kN[2] / me]
    )

    # Graphs
    adrs_spectrum = coord.interpolate_curve(coord.x_ADRS_meters, coord.y_ADRS_meters)
    k1_eff_curve = coord.interpolate_curve(coord.x_k1_eff, coord.y_k1_eff)
    p_sdof = coord.interpolate_curve(x_p_sdof, y_p_sdof)

    # TODO switch from kN bilinear to the ms2 one
    # Straight line passing through 1st and 2nd point of bilinear curve
    # Generate the 1st part of the bilinear
    x_bilinear_line_kN_1 = coord.generate_line(
        x_p_sdof, x_bilinear[0], x_bilinear[1], y_bilinear_kN[0], y_bilinear_kN[1]
    )[0]
    y_bilinear_line_kN_1 = coord.generate_line(
        x_p_sdof, x_bilinear[0], x_bilinear[1], y_bilinear_kN[0], y_bilinear_kN[1]
    )[1]
    bilinear_line_kN_1 = coord.interpolate_curve(
        x_bilinear_line_kN_1, y_bilinear_line_kN_1
    )
    # Intersections of bilinear #1
    intersection_bilinear1_psdof_coords = coord.find_intersections(
        p_sdof, bilinear_line_kN_1
    )

    # Straight line passing through 2nd and 3rd point of the bilinear curve
    # Generate the 2nd part of the bilinear
    x_bilinear_line_kN_2 = coord.generate_line(
        x_p_sdof, x_bilinear[1], x_bilinear[2], y_bilinear_kN[1], y_bilinear_kN[2]
    )[0]
    y_bilinear_line_kN_2 = coord.generate_line(
        x_p_sdof, x_bilinear[1], x_bilinear[2], y_bilinear_kN[1], y_bilinear_kN[2]
    )[1]
    bilinear_line_kN_2 = coord.interpolate_curve(
        x_bilinear_line_kN_2, y_bilinear_line_kN_2
    )
    # Intersections of bilinear #2
    intersection_bilinear2_psdof_coords = coord.find_intersections(
        p_sdof, bilinear_line_kN_2
    )

    # Intersection of the two straight lines (dy)
    intersection_dy_coords = coord.find_intersections(
        bilinear_line_kN_1, bilinear_line_kN_2
    )

    # Calculate A1 and A2

    list_fitting_1_x_pushover = coord.find_range_pushover(
        x_p_sdof,
        intersection_bilinear1_psdof_coords[-1][0],
        intersection_bilinear2_psdof_coords[0][0],
    )  # List of all the X coordinates between the two intersections with the bilinear curve. A1

    list_fitting_1_y_pushover = coord.find_range_pushover(
        y_p_sdof,
        intersection_bilinear1_psdof_coords[-1][1],
        intersection_bilinear2_psdof_coords[0][1],
    )  # List of all the Y coordinates between the two intersections with the bilinear curve. A1

    list_fitting_2_x_pushover = coord.find_range_pushover(
        x_p_sdof,
        intersection_bilinear2_psdof_coords[0][0],
        intersection_bilinear2_psdof_coords[-1][0],
    )  # List of all the X coordinates between the two intersections with the bilinear curve. A2
    list_fitting_2_y_pushover = coord.find_range_pushover(
        y_p_sdof,
        intersection_bilinear2_psdof_coords[0][1],
        intersection_bilinear2_psdof_coords[-1][1],
    )  # List of all the Y coordinates between the two intersections with the bilinear curve. A2

    # Compute the area using the composite trapezoidal rule.
    area_1_under_bilinear_y_coords = np.array(
        [
            intersection_bilinear1_psdof_coords[-1][1],
            Vy_kN,
            intersection_bilinear2_psdof_coords[0][1],
        ]
    )
    area_1_under_bilinear_x_coords = np.array(
        [
            intersection_bilinear1_psdof_coords[-1][0],
            dy,
            intersection_bilinear2_psdof_coords[0][0],
        ]
    )

    area_2_under_bilinear_y_coords = np.array(
        [
            intersection_bilinear2_psdof_coords[0][1],
            intersection_bilinear2_psdof_coords[1][1],
        ]
    )
    area_2_under_bilinear_x_coords = np.array(
        [
            intersection_bilinear2_psdof_coords[0][0],
            intersection_bilinear2_psdof_coords[1][0],
        ]
    )
    area_tot = trapz(y_p_sdof, x_p_sdof)
    area_1_under_pushover = trapz(
        np.array(list_fitting_1_y_pushover), np.array(list_fitting_1_x_pushover)
    )
    area_2_under_pushover = trapz(
        np.array(list_fitting_2_y_pushover), np.array(list_fitting_2_x_pushover)
    )
    area_1_under_bilinear = trapz(
        area_1_under_bilinear_y_coords, area_1_under_bilinear_x_coords
    )
    area_2_under_bilinear = trapz(
        area_2_under_bilinear_y_coords, area_2_under_bilinear_x_coords
    )

    a1 = np.absolute(area_1_under_pushover - area_1_under_bilinear)
    a2 = np.absolute(area_2_under_pushover - area_2_under_bilinear)
    area_diff = np.absolute(a1 - a2)

    if area_diff < 0.0004:

        print(
            display.print_all(
                Vp_kN,
                dp,
                dy,
                Vy_kN,
                Vp_ms2,
                intersection_bilinear1_psdof_coords,
                intersection_bilinear2_psdof_coords,
                intersection_dy_coords,
                area_tot,
                a1,
                a2,
                area_diff,
            )
        )

        graphs.plot_pushover_bilinear(
            x_p_sdof,
            y_p_sdof,
            intersection_bilinear1_psdof_coords,
            intersection_bilinear2_psdof_coords,
            intersection_dy_coords,
        )
        plt.show()

        return dy
    else:
        dy = dy + 0.00001

        return find_dy(dy)


find_dy(0.0100)

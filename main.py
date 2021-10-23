import numpy as np
from numpy import trapz
import matplotlib.pyplot as plt

from coordinates import Coords
from calcs import Calculations, Print, Area
from graphs import Graphs

coord = Coords()
values = Calculations()
area = Area()
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
    K1 = values.get_K1(x_p_sdof, y_p_sdof)  # kN
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
    p_sdof = coord.interpolate_curve(x_p_sdof, y_p_sdof)

    # Straight line passing through 1st and 2nd point of bilinear curve
    # Generate the 1st part of the bilinear
    bilinear_line_kN_1 = coord.bilinear_line(
        x_p_sdof, x_bilinear[0], x_bilinear[1], y_bilinear_kN[0], y_bilinear_kN[1]
    )

    # Intersections of bilinear #1
    intersection_bilinear1_psdof_coords = coord.find_intersections(
        p_sdof, bilinear_line_kN_1
    )

    # Straight line passing through 2nd and 3rd point of the bilinear curve
    # Generate the 2nd part of the bilinear
    bilinear_line_kN_2 = coord.bilinear_line(
        x_p_sdof, x_bilinear[1], x_bilinear[2], y_bilinear_kN[1], y_bilinear_kN[2]
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
    fitting_lists = area.calculate_fitting_list(
        x_p_sdof,
        y_p_sdof,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
    )
    fitting_list_1_x_pushover = fitting_lists[0]
    fitting_list_1_y_pushover = fitting_lists[1]
    fitting_list_2_x_pushover = fitting_lists[2]
    fitting_list_2_y_pushover = fitting_lists[3]

    # Compute the area using the composite trapezoidal rule.
    areas_kN = area.calculate_areas(
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
        dy,
        Vy_kN,
        fitting_list_1_y_pushover,
        fitting_list_2_y_pushover,
        fitting_list_1_x_pushover,
        fitting_list_2_x_pushover,
    )

    a1 = areas_kN[0]
    a2 = areas_kN[1]
    area_diff = areas_kN[2]

    if area_diff < 0.0004:
        sd_meters = coord.sd_meters(coord.x_adrs_input)
        sd_ms2 = coord.sa_ms2(coord.y_adrs_input)

        adrs_spectrum = coord.interpolate_curve(sd_meters, sd_ms2)
        k_eff = Vp_ms2 / dp

        k1_eff_curve = coord.interpolate_curve(
            sd_meters,
            coord.y_k_eff(sd_meters, k_eff),
        )

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

        graphs.plot_adrs(
            sd_meters,
            sd_ms2,
            x_bilinear,
            y_bilinear_ms2,
            sd_meters,
            coord.y_k_eff(sd_meters, k_eff),
            values.get_de(adrs_spectrum, k1_eff_curve),
        )
        plt.show()

        return dy
    else:
        dy = dy + 0.00001

        return find_dy(dy)


find_dy(0.0100)

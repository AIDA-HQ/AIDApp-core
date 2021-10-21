import numpy as np
from numpy import trapz
import matplotlib.pyplot as plt

from coord import Coords
from calcs import Calculations
from graphs import Graphs

coord = Coords()
values = Calculations()
graphs = Graphs()


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
    # print(np.polyfit(a, b, 1))
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
    ADRS_spectrum = coord.interpolate_curve(coord.x_ADRS_meters, coord.y_ADRS_meters)
    K1_eff_curve = coord.interpolate_curve(coord.x_K1_eff, coord.y_K1_eff)
    p_sdof = coord.interpolate_curve(x_p_sdof, y_p_sdof)

    # TODO switch from kN bilinear to the ms2 one
    # Straight line passing through 1st and 2nd point of bilinear curve
    # Generate the 1st part of the bilinear
    x_bilinear_line_1 = coord.generate_line(
        x_p_sdof, x_bilinear[0], x_bilinear[1], y_bilinear_kN[0], y_bilinear_kN[1]
    )[0]
    y_bilinear_line_1 = coord.generate_line(
        x_p_sdof, x_bilinear[0], x_bilinear[1], y_bilinear_kN[0], y_bilinear_kN[1]
    )[1]
    bilinear_line_1 = coord.interpolate_curve(x_bilinear_line_1, y_bilinear_line_1)
    # Intersections of bilinear #1
    intersection_bilinear1_psdof_coords = coord.find_intersections(
        p_sdof, bilinear_line_1
    )
    intersection_bilinear1_psdof_coords

    # Straight line passing through 2nd and 3rd point of the bilinear curve
    # Generate the 2nd part of the bilinear
    x_bilinear_line_2 = coord.generate_line(
        x_p_sdof, x_bilinear[1], x_bilinear[2], y_bilinear_kN[1], y_bilinear_kN[2]
    )[0]
    y_bilinear_line_2 = coord.generate_line(
        x_p_sdof, x_bilinear[1], x_bilinear[2], y_bilinear_kN[1], y_bilinear_kN[2]
    )[1]
    bilinear_line_2 = coord.interpolate_curve(x_bilinear_line_2, y_bilinear_line_2)
    # Intersections of bilinear #2
    intersection_bilinear2_psdof_coords = coord.find_intersections(
        p_sdof, bilinear_line_2
    )
    intersection_bilinear2_psdof_coords

    # Intersection of the two straight lines (dy)
    intersection_dy_coords = coord.find_intersections(bilinear_line_1, bilinear_line_2)
    intersection_dy_coords

    # Calculate A1 and A2

    list_fitting_x = coord.find_range_pushover(
        x_p_sdof,
        intersection_bilinear1_psdof_coords[-1][0],
        intersection_bilinear2_psdof_coords[0][0],
    )

    list_fitting_y = coord.find_range_pushover(
        y_p_sdof,
        intersection_bilinear1_psdof_coords[-1][1],
        intersection_bilinear2_psdof_coords[0][1],
    )
    list_fitting_x_b = coord.find_range_pushover(
        x_p_sdof,
        intersection_bilinear2_psdof_coords[0][0],
        intersection_bilinear2_psdof_coords[-1][0],
    )
    list_fitting_y_b = coord.find_range_pushover(
        y_p_sdof,
        intersection_bilinear2_psdof_coords[0][1],
        intersection_bilinear2_psdof_coords[-1][1],
    )

    # Compute the area using the composite trapezoidal rule.
    area_1_y_coords = np.array(
        [
            intersection_bilinear1_psdof_coords[-1][1],
            Vy_kN,
            intersection_bilinear2_psdof_coords[0][1],
        ]
    )
    area_1_x_coords = np.array(
        [
            intersection_bilinear1_psdof_coords[-1][0],
            dy,
            intersection_bilinear2_psdof_coords[0][0],
        ]
    )

    area_2_y_coords = np.array(
        [
            intersection_bilinear2_psdof_coords[0][1],
            intersection_bilinear2_psdof_coords[1][1],
        ]
    )
    area_2_x_coords = np.array(
        [
            intersection_bilinear2_psdof_coords[0][0],
            intersection_bilinear2_psdof_coords[1][0],
        ]
    )
    area_tot = trapz(y_p_sdof, x_p_sdof)
    area_1 = trapz(np.array(list_fitting_y), np.array(list_fitting_x))
    area_2 = trapz(np.array(list_fitting_y_b), np.array(list_fitting_x_b))

    a1 = np.absolute(area_1 - trapz(area_1_y_coords, area_1_x_coords))
    a2 = np.absolute(area_2 - trapz(area_2_y_coords, area_2_x_coords))
    area_diff = np.absolute(a1 - a2)

    if area_diff < 0.0004:
        print("Storey masses Matrix:\n", values.get_m_matrix(), "\n")
        print("Eigenvalues Matrix:\n", values.get_φ(), "\n")
        print("Modal pattern:\n", values.get_Mφ())
        print("\nφTMτ:", values.get_φTMτ())
        print("φTMφ:", values.get_φTMφ())
        print("Γ: ", Γ)
        print("Vp_kn:", Vp_kN)

        print(
            "\nIntersection(s) between First line of bilinear and SDOF Pushover Curve:",
            intersection_bilinear1_psdof_coords,
        )
        print(
            "Intersection(s) between Second line of bilinear and SDOF Pushover Curve:",
            intersection_bilinear2_psdof_coords,
        )
        print("Intersection of the two lines of the bilinear:", intersection_dy_coords)
        print("Total Area under pushover curve:", area_tot)

        print("dy:", dy)
        print("A1 =", a1)
        print("A2 =", a2)
        print("A1-A2:", area_diff)
        print("%:", area_diff / a1)

        graphs.plot_intersections(intersection_dy_coords)
        graphs.plot_intersections(intersection_bilinear1_psdof_coords)
        graphs.plot_intersections(intersection_bilinear2_psdof_coords)
        graphs.plot_all(
            x_bilinear,
            y_bilinear_ms2,
            x_p_sdof,
            y_p_sdof,
            x_bilinear_line_1,
            y_bilinear_line_1,
            x_bilinear_line_2,
            y_bilinear_line_2,
        )
        plt.show()

        return dy
    else:
        dy = dy + 0.00001

        return find_dy(dy)


find_dy(0.0100)

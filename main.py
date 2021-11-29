import numpy as np
import matplotlib.pyplot as plt

from calcs import Values, Area
from coordinates import Coords
from display import Print
from graphs import Graphs
from input_coordinates import Input

area = Area()
coord = Coords()
graphs = Graphs()
input_coord = Input()
display = Print()
values = Values()


def main():
    global storey_masses
    global eigenvalues
    global dp
    global μ_DB
    global k_DB
    global Kf
    global Γ
    global me
    global y_p_sdof
    global x_p_sdof
    global Vp_kN
    global Vp_ms2
    global K1

    # Store data from user input
    number_storeys = int(input("Enter the number of storeys: "))

    storey_masses = []
    eigenvalues = []
    i = 0
    while i < number_storeys:
        i = i + 1
        storey_masses.append(
            float(input("Enter the mass of storey #" + str(i) + " [ton]: "))
        )
    n = 0
    while n < number_storeys:
        n = n + 1
        eigenvalues.append(float(input("Enter the eigenvalues #" + str(n) + ": ")))

    # 3rd x coordinate of bilinear curve
    dp = float(input("\nEnter the value of d*p [m]:"))

    μ_DB = float(input("\nEnter the value of μ(DB):"))
    k_DB = float(input("\nEnter the value of k(DB):"))
    Kf = float(input("Enter the value of K(F):"))

    Γ = values.get_Γ(storey_masses, eigenvalues)
    me = values.get_me()  # [ton]
    y_p_sdof = coord.y_p_sdof(Γ)
    x_p_sdof = coord.x_p_sdof(Γ)
    Vp_kN = y_p_sdof[coord.find_nearest_coordinate_index(x_p_sdof, dp)]
    Vp_ms2 = Vp_kN / me  # m/s^2

    # Slope of first n values of SDOF Pushover Curve
    K1 = values.get_K1(x_p_sdof, y_p_sdof)  # [kN/m]
    find_dy(0.0100)


def find_dy(dy):
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

    # Calculate A1 and A2
    fitting_lists = area.calculate_fitting_list(
        x_p_sdof,
        y_p_sdof,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
    )

    (
        fitting_list_1_x_pushover,
        fitting_list_1_y_pushover,
        fitting_list_2_x_pushover,
        fitting_list_2_y_pushover,
    ) = fitting_lists

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

    a1, a2, area_diff = areas_kN

    if area_diff < 0.0004:
        sd_meters_0 = values.convert_to_meters(input_coord.x_adrs_input)
        sa_ms2_0 = values.convert_to_ms2(input_coord.y_adrs_input)
        plt.plot(sd_meters_0, sa_ms2_0, color="#FFC000", label="Sa(5%)")

        adrs_spectrum = coord.interpolate_curve(sd_meters_0, sa_ms2_0)
        k_eff = Vp_ms2 / dp

        k1_eff_curve = coord.interpolate_curve(
            sd_meters_0,
            coord.y_kn_eff(sd_meters_0, k_eff),
        )

        # Sui generis first iteraction
        ξFrame = values.get_ξFrame(Kf, dp, dy, Vy_kN, Vp_ms2)

        ξn_eff = values.get_ξn_eff_0(dp, adrs_spectrum, k1_eff_curve)
        ξ_DB = values.get_ξ_DB(μ_DB, k_DB)
        Vp_DB_prev_iteraction = values.get_Vp_DB_0(ξn_eff, Vp_kN, ξ_DB, ξFrame)

        check = values.get_check(ξFrame, ξn_eff)
        Vp_DB = Vp_DB_prev_iteraction
        display.print_first_iteration(ξFrame, ξn_eff, Vp_DB, check)

        # Recursive function to calculate what's needed
        def get_calcs_recursive(
            Vp_DB, check, i, sd_meters, sa_ms2, Vy_F_DB, Vp_F_DB, kn_eff
        ):
            if check > 0.5:
                i = i + 1
                ξ_eff_F_DB = values.get_ξ_eff_F_DB(Vp_kN, ξ_DB, Vp_DB, ξFrame)
                sa_ms2 = values.convert_to_ms2(
                    values.get_Sa(input_coord.y_adrs_input, ξ_eff_F_DB)
                )
                sd_meters = values.get_Sd(sa_ms2_0, sd_meters_0, sa_ms2)

                adrs_spectrum = coord.interpolate_curve(sd_meters, sa_ms2)

                Vp_DB_prev_iteraction = Vp_DB

                Vy_F_DB = values.get_Vy_F_DB(Vp_DB)
                Vp_F_DB = values.get_Vp_F_DB(Vp_kN, Vp_DB)
                kn_eff = values.get_kn_eff(Vp_F_DB, dp)
                kn_eff_curve = coord.interpolate_curve(
                    sd_meters,
                    coord.y_kn_eff(sd_meters, kn_eff),
                )
                ξn_eff = values.get_ξn_eff(dp, adrs_spectrum, kn_eff_curve, ξ_eff_F_DB)
                Vp_DB = values.get_Vp_DB(
                    ξn_eff, Vp_kN, ξFrame, ξ_DB, Vp_DB_prev_iteraction
                )

                check = values.get_check(ξ_eff_F_DB, ξn_eff)
                check_Vp_DB = values.get_check_Vp_DB(Vp_DB, Vp_DB_prev_iteraction)
                display.print_brief(
                    i,
                    Vy_F_DB,
                    Vp_F_DB,
                    ξ_eff_F_DB,
                    Vp_DB_prev_iteraction,
                    ξn_eff,
                    Vp_DB,
                    check,
                    check_Vp_DB
                )

                return get_calcs_recursive(
                    Vp_DB, check, i, sd_meters, sa_ms2, Vy_F_DB, Vp_F_DB, kn_eff
                )

            if check <= 0.5:
                kn_eff_list = coord.y_kn_eff(sd_meters, kn_eff)
                y_bilinear_ms2 = np.array([0, Vy_F_DB, Vp_F_DB])

                plt.plot(sd_meters, sa_ms2, color="#002260", label="ξ=5%")
                plt.plot(
                    x_bilinear, y_bilinear_ms2, color="#FF0000", label="Bare Frame"
                )
                plt.plot(
                    sd_meters,
                    kn_eff_list,
                    color="#00B050",
                    label=("K" + str(i) + "eff"),
                )
                plt.xlabel("Sd [m]", fontsize="large")
                plt.ylabel("Sa [m/s^2]", fontsize="large")
                plt.legend()
                plt.show()

                print("DONE!")

        get_calcs_recursive(Vp_DB, check, 1, None, None, None, None, None)

        return dy
    else:
        dy = dy + 0.00001

        return find_dy(dy)


main()

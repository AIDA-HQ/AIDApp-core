import numpy as np
from numpy import trapz
from scipy.stats import linregress

from coordinates import Coords

coord = Coords()


class Calculations:
    def get_Γ(self, storey_masses, eigenvalues):
        global m_tot
        global φ
        global Mφ
        global φTMτ
        global φTMφ
        global m_matrix
        global Γ

        m_matrix = np.diagflat(
            storey_masses
        )  # Storey masses displayed in a diagonal matrix
        m_tot = sum(storey_masses)  # Sum all storey masses together
        φ = np.array(eigenvalues)  # Eigenvalues displayed in a 1-coloumn matrix
        Mφ = np.matmul(m_matrix, φ)
        φTMτ = np.matmul(φ, storey_masses)
        φTMφ = np.matmul(φ, Mφ)
        Γ = φTMτ / φTMφ
        return Γ

    def get_m_matrix(self):
        return m_matrix

    def get_m_tot(self):
        return m_tot

    def get_φ(self):
        return φ

    def get_Mφ(self):
        return Mφ

    def get_φTMτ(self):
        return φTMτ

    def get_φTMφ(self):
        return φTMφ

    def get_K1(self, x_p_sdof, y_p_sdof):
        """
        Slope of first 7 values of SDOF Pushover Curve
        """
        a = np.array([x_p_sdof[2:10]])
        b = np.array([y_p_sdof[2:10]])

        k1 = linregress(a, b)[0]  # kN
        return k1  # Slope

    def get_Vy_kN(self, K1, dy):
        Vy_kN = K1 * dy  # kN
        return Vy_kN

    def get_me(self):
        global me
        me = m_tot / Γ
        return me

    def get_Vy_F_ms2(self, Vy_kN):
        Vy_F_ms2 = Vy_kN / me  # [m/s^2]
        return Vy_F_ms2

    def get_de(self, adrs_spectrum, kn_eff_curve):
        # X coords of K1eff intercepting ADRS spectrum
        intersection_adrs_kn = adrs_spectrum.intersection(kn_eff_curve)
        de = float(intersection_adrs_kn.x)  # [m]
        return de

    def get_ξ1eff(self, dp, ADRS_spectrum, K1_eff_curve):
        de = self.get_de(ADRS_spectrum, K1_eff_curve)
        ξ1eff = 10 * (de / dp) ** 2 - 10
        return ξ1eff

    def get_ξFrame(self, Kf, dp, dy, Vy_kN, Vp_ms2):
        dyF = dy  # [m]
        Vy_F_ms2 = self.get_Vy_F_ms2(Vy_kN)
        VpF_ms2 = Vp_ms2  # [m/s^2]
        ξFrame = (Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp)
        return ξFrame


class Print:
    def print_all(
        self,
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
    ):
        values = Calculations()
        print("Storey masses Matrix:\n", values.get_m_matrix(), "\n")
        print("Eigenvalues Matrix:\n", values.get_φ(), "\n")
        print("Modal pattern:\n", values.get_Mφ())
        print("\nφTMτ:", values.get_φTMτ())
        print("φTMφ:", values.get_φTMφ())
        print("Γ: ", Γ)
        print("Vp_kn:", Vp_kN)
        Kf = float(input("Enter the value of K(F): "))
        print("k(F): ", Kf)
        """
        print("Vy(F): ", Vy_F_ms2, "m/s^2")
        print("dp(F): ", dp, "m")
        print("Vp(F): ", VpF_ms2, "m/s^2")
        print("de: ", de, "m")
        print("\nξ1eff: ", self..get_ξ1eff(), "%")
        """

        print("ξFrame: ", values.get_ξFrame(Kf, dp, dy, Vy_kN, Vp_ms2), "%")
        # print("Check:", check * 100, "%")
        print(
            "\nIntersection(s) between First line of bilinear and SDOF Pushover Curve:",
            intersection_bilinear1_psdof_coords,
        )
        print(
            "Intersection(s) between Second line of bilinear and SDOF Pushover Curve:",
            intersection_bilinear2_psdof_coords,
        )
        print("Intersection of the two lines of the bilinear:", intersection_dy_coords)

        print("dy:", dy)
        print("A1 =", a1)
        print("A2 =", a2)
        print("A1-A2:", area_diff)
        print("%:", area_diff / a1)


class Area:
    def calculate_fitting_list(
        self,
        x_p_sdof,
        y_p_sdof,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
    ):

        fitting_list_1_x_pushover = coord.find_range_pushover(
            x_p_sdof,
            intersection_bilinear1_psdof_coords[-1][0],
            intersection_bilinear2_psdof_coords[0][0],
        )  # List of all the X coordinates between the two intersections with the bilinear curve. A1

        list_fitting_1_y_pushover = coord.find_range_pushover(
            y_p_sdof,
            intersection_bilinear1_psdof_coords[-1][1],
            intersection_bilinear2_psdof_coords[0][1],
        )  # List of all the Y coordinates between the two intersections with the bilinear curve. A1

        fitting_list_2_x_pushover = coord.find_range_pushover(
            x_p_sdof,
            intersection_bilinear2_psdof_coords[0][0],
            intersection_bilinear2_psdof_coords[-1][0],
        )  # List of all the X coordinates between the two intersections with the bilinear curve. A2
        fitting_list_2_y_pushover = coord.find_range_pushover(
            y_p_sdof,
            intersection_bilinear2_psdof_coords[0][1],
            intersection_bilinear2_psdof_coords[-1][1],
        )  # List of all the Y coordinates between the two intersections with the bilinear curve. A2
        return (
            fitting_list_1_x_pushover,
            list_fitting_1_y_pushover,
            fitting_list_2_x_pushover,
            fitting_list_2_y_pushover,
        )

    def calculate_areas(
        self,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
        dy,
        Vy,
        fitting_list_1_y_pushover,
        fitting_list_2_y_pushover,
        fitting_list_1_x_pushover,
        fitting_list_2_x_pushover,
    ):
        area_1_under_bilinear_y_coords = np.array(
            [
                intersection_bilinear1_psdof_coords[-1][1],
                Vy,
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
        area_1_under_pushover = trapz(
            np.array(fitting_list_1_y_pushover), np.array(fitting_list_1_x_pushover)
        )
        area_2_under_pushover = trapz(
            np.array(fitting_list_2_y_pushover), np.array(fitting_list_2_x_pushover)
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
        return a1, a2, area_diff

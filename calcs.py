import numpy as np
from numpy import trapz
from scipy.stats import linregress

from coordinates import Coords

coord = Coords()


class Calculations:
    def convert_to_meters(self, coord_mm):
        """
        Convert the input value to m
        """
        coord_m_list = []
        for element in coord_mm:
            new_coord = element / 1000
            coord_m_list.append(new_coord)
        return np.array(coord_m_list) #[m]

    def convert_to_ms2(self, coord_g):
        """
        Convert the input value to m/s^2
        """
        ms2_list = []
        for element in coord_g:
            new_coord = element * 9.81
            ms2_list.append(new_coord)
        return np.array(ms2_list) #[m/s^2]

    def get_Γ(self, storey_masses, eigenvalues):
        """
        return Γ
        """
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
        """
        return m_matrix
        """
        return m_matrix

    def get_m_tot(self):
        """
        return m_tot
        """
        return m_tot

    def get_φ(self):
        """
        return φ
        """
        return φ

    def get_Mφ(self):
        """
        return Mφ
        """
        return Mφ

    def get_φTMτ(self):
        """
        Return φTMτ
        """
        return φTMτ

    def get_φTMφ(self):
        """
        return φTMφ
        """
        return φTMφ

    def get_K1(self, x_p_sdof, y_p_sdof):
        """
        Calculate the slope of first 7 values of SDOF Pushover Curve
        """
        a = np.array([x_p_sdof[2:10]])
        b = np.array([y_p_sdof[2:10]])

        # TODO - Find an alternative to linregress
        slope, intercept, r, p, se = linregress(a, b)  # kN
        return slope  # Slope

    def get_Vy_kN(self, K1, dy):
        """
        Return the value of Vy(F) in kN
        """
        global Vy_F_kN
        Vy_F_kN = K1 * dy  # kN
        return Vy_F_kN

    def get_me(self):
        """
        Get the mass of the storeys
        """
        global me
        me = m_tot / Γ
        return me

    def get_de(self, adrs_spectrum, kn_eff_curve):
        """
        X coord of Kn_eff intercepting ADRS spectrum
        """
        intersection_adrs_kn = adrs_spectrum.intersection(kn_eff_curve)
        de = float(intersection_adrs_kn.x)  # [m]
        return de

    #
    # ADRS methods
    #

    def get_Vy_F_ms2(self, Vy_F_kN):
        """
        Return the value of Vy(F) in m/s^2
        """
        global Vy_F_ms2
        Vy_F_ms2 = Vy_F_kN / me  # [m/s^2]
        return Vy_F_ms2

    def get_Vy_F_DB(self, Vp_DB):
        """
        Return the value of Vy(F + DB)
        """
        Vy = Vy_F_kN / me + Vp_DB / me
        return Vy  # [m/s^2]

    def get_Vp_F_DB(self, Vp_kN, Vp_DB):
        """
        Return the value of Vp(F + DB)
        Vp_kN is a constant, defined initally
        Vp_DB changes every iteration
        """
        Vp = Vp_kN / me + Vp_DB / me
        return Vp

    def get_ξFrame(self, Kf, dp, dy, Vy_kN, Vp_ms2):
        """
        Calculate the first value of ξFrame
        """
        dyF = dy  # [m]
        Vy_F_ms2 = self.get_Vy_F_ms2(Vy_kN)
        VpF_ms2 = Vp_ms2  # [m/s^2]
        global ξFrame
        ξFrame = (Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp)
        return ξFrame #[%]

    def get_ξ_eff_F_DB(self, Vp_kN, ξ_DB, Vp_DB):
        """
        Return the value of ξ_eff(F + DB), which,
        for the first iteration, was called "ξFrame"
        ξFrame and Vp_kN are constants, defined initally
        ξ_DB and Vp_DB change every iteration
        """
        ξ_eff_F_DB = (ξFrame * Vp_kN + ξ_DB * Vp_DB) / (Vp_kN + Vp_DB)
        return ξ_eff_F_DB #[%]

    def get_ξn_eff(self, dp, ADRS_spectrum, K1_eff_curve):
        """
        Calculate iterated values of ξn_eff
        """
        de = self.get_de(ADRS_spectrum, K1_eff_curve)
        ξn_eff = 10 * (de / dp) ** 2 - 10
        return ξn_eff #[%]

    def get_Sa(self, y_adrs_input, ξ_eff_F_DB):
        """
        Calculate the value of Sa coordinates after 
        the first iteration
        """
        Sa_list = []
        for element in y_adrs_input:
            Sa_element = element *(10/(10+ξ_eff_F_DB)) ** 0.5
            Sa_list.append(Sa_element)
        return np.array(Sa_list) #[g]
    
    # TODO Convert the Sa values to m/s^2

    def get_T(self, sa_ms2, sd_meters):
        """
        Calculate the value of T period
        """
        T_list = []
        for sd, sa in zip(sd_meters, sa_ms2):
            T_element = 2 * np.pi * (sd/sa) ** 0.5 
            T_list.append(T_element)
        return np.array(T_list) #[s]

    def get_Sd(self, Sa_ms2, T):
        """
        Calculate the value of Sd after the first iteration
        """
        Sd_list = []
        for sa, T in zip(Sa_ms2, T):
            Sd_element = sa * (T/2/np.pi) ** 2
            Sd_list.append(Sd_element)
        return np.array(Sd_list) #[m]

    #
    # Dissipative Brace (DB) methods
    #

    def get_ξ_DB(self, μ_DB, k_DB):
        ξ_DB = 63.7 * k_DB * ((μ_DB - 1) / μ_DB)
        return ξ_DB  # [%]

    def get_dy_DB(self, μ_DB, dp_DB):
        dy_DB = dp_DB / μ_DB
        return dy_DB  # [m]

    def get_Vp_DB_1(self, ξn_eff, ξFrame, Vp_kN, ξ_DB):
        """
        Vy(DB) = VP(DB)
        Return the very first value of Vp_DB, which will be used
        by the following iterations.
        """
        global Vp_DB_1
        Vp_DB_1 = (ξn_eff - ξFrame) * (Vp_kN / ξ_DB)
        return Vp_DB_1  # [kN]

    def get_Vp_DB(ξn_eff, Vp_kN, ξFrame, ξ_DB):
        """
        Vy(DB) = VP(DB)
        Return the value of Vp_DB [kN] which will be iterated various times
        """
        Vp_DB = (ξn_eff * (Vp_kN + Vp_DB_1) - ξFrame * Vp_kN) / ξ_DB
        return Vp_DB  # [kN]

    def get_Kb(self, dy_DB, Vp_DB):
        Kb = Vp_DB / dy_DB
        return Kb  # [kN/m]

    def get_check(self, ξ_eff, ξn_eff):
        """
        Get the perecentage difference between ξ_eff and ξn_eff
        """
        check = np.absolute(ξn_eff - ξ_eff) / ξ_eff
        return check #[%]


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
        adrs_spectrum,
        k1_eff_curve
    ):
        values = Calculations()
        print("Storey masses Matrix:\n", values.get_m_matrix(), "\n")
        print("Eigenvalues Matrix:\n", values.get_φ(), "\n")
        print("Modal pattern:\n", values.get_Mφ())
        print("\nφTMτ:", values.get_φTMτ())
        print("φTMφ:", values.get_φTMφ())
        print("Γ:", Γ)
        print("Vp_kn:", Vp_kN)
        Kf = float(input("Enter the value of K(F):"))
        print("k(F):", Kf)
        print("de:", values.get_de(adrs_spectrum, k1_eff_curve))

        """
        print("Vy(F):", Vy_F_ms2, "m/s^2")
        print("dp(F):", dp, "m")
        print("Vp(F):", VpF_ms2, "m/s^2")
        print("de:", de, "m")
        print("\nξn_eff:", self.get_ξn_eff(), "%")
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

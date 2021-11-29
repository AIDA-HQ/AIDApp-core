import numpy as np
from numpy import trapz
from scipy.stats import linregress

from coordinates import Coords

coord = Coords()


class Values:
    def convert_to_meters(self, coord_mm):
        """
        Convert the input array values to m
        """
        coord_m_list = []
        for element in coord_mm:
            new_coord = element / 1000
            coord_m_list.append(new_coord)
        return np.array(coord_m_list)  # [m]

    def convert_to_ms2(self, coord_g):
        """
        Convert the input array values to m/s^2
        """
        ms2_list = []
        for element in coord_g:
            new_coord = element * 9.81
            ms2_list.append(new_coord)
        return np.array(ms2_list)  # [m/s^2]

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
        Returns φTMφ
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
        Returns the value of Vy(F) in kN.
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
        Vy_F_DB = Vy_F_kN / me + Vp_DB / me
        return Vy_F_DB  # [m/s^2]

    def get_Vp_F_DB(self, Vp_kN, Vp_DB):
        """
        Return the value of Vp(F + DB)
        Vp_kN is a constant, defined initally.
        Vp_DB changes every iteration.
        """
        Vp_F_DB = Vp_kN / me + Vp_DB / me
        return Vp_F_DB  # [m/s2]

    def get_kn_eff(self, Vp_F_DB, dp):
        kn_eff = Vp_F_DB / dp
        return kn_eff

    def get_ξFrame(self, Kf, dp, dy, Vy_kN, Vp_ms2):
        """
        Calculate the first value of ξFrame
        """
        dyF = dy  # [m]
        Vy_F_ms2 = self.get_Vy_F_ms2(Vy_kN)
        VpF_ms2 = Vp_ms2  # [m/s^2]
        ξFrame = (Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp)
        return ξFrame  # [%]

    def get_ξ_eff_F_DB(self, Vp_kN, ξ_DB, Vp_DB, ξFrame):
        """
        Return the value of ξ_eff(F + DB), which,
        for the first iteration, was called "ξFrame"
        ξFrame and Vp_kN are constants, defined initally.
        ξ_DB and Vp_DB change every iteration.
        """
        ξ_eff_F_DB = (ξFrame * Vp_kN + ξ_DB * Vp_DB) / (Vp_kN + Vp_DB)
        return ξ_eff_F_DB  # [%]

    def get_ξn_eff_0(self, dp, adrs_spectrum, k1_eff):
        """
        Calculate first ever value of ξn_eff
        """
        de = self.get_de(adrs_spectrum, k1_eff)

        ξn_eff_0 = 10 * (de / dp) ** 2 - 10
        return ξn_eff_0  # [%]

    def get_ξn_eff(self, dp, adrs_spectrum, k1_eff_curve, ξ_eff_F_DB):
        """
        Calculate iterated values of ξn_eff
        """
        de = self.get_de(adrs_spectrum, k1_eff_curve)
        ξn_eff = (10 + ξ_eff_F_DB) * (de / dp) ** 2 - 10
        return ξn_eff  # [%]

    def get_Sa(self, y_adrs_input, ξ_eff_F_DB):
        """
        Calculate the value of Sa (ξeff)
        coordinates after the first iteration.
        """
        Sa_list = []
        for element in y_adrs_input:
            Sa_element = element * (10 / (10 + ξ_eff_F_DB)) ** 0.5
            Sa_list.append(Sa_element)
        return np.array(Sa_list)  # [g]

    # TODO Convert the Sa values to m/s^2

    def get_T(self, sa_ms2_0, sd_meters_0):
        """
        Calculate the value of T period
        """
        T_list = []
        for sd, sa in zip(sd_meters_0, sa_ms2_0):
            T_element = 2 * np.pi * (sd / sa) ** 0.5
            T_list.append(T_element)
        return np.array(T_list)  # [s]

    def get_Sd(self, sa_ms2_0, sd_meters_0, sa_ms2):
        """
        Calculate the value of Sd after the first iteration
        """
        # sa_ms2_0 is the initial array of Sa, the one input by the user
        # sa_ms2 is the array calculated by the program
        t_array = self.get_T(sa_ms2_0, sd_meters_0)
        Sd_list = []
        for sa, t in zip(sa_ms2, t_array):
            Sd_element = sa * ((t / 2 / np.pi) ** 2)
            Sd_list.append(Sd_element)
        return np.array(Sd_list)  # [m]

    #
    # Dissipative Brace (DB) methods
    #

    def get_ξ_DB(self, μ_DB, k_DB):
        ξ_DB = 63.7 * k_DB * ((μ_DB - 1) / μ_DB)
        return ξ_DB  # [%]

    def get_dy_DB(self, μ_DB, dp_DB):
        dy_DB = dp_DB / μ_DB
        return dy_DB  # [m]

    def get_Vp_DB_0(self, ξn_eff, Vp_kN, ξ_DB, ξFrame):
        """
        Vy(DB) = VP(DB)
        Return the very first value of Vp_DB, which
        will be used by the following iteration.
        """
        Vp_DB_1 = (ξn_eff - ξFrame) * (Vp_kN / ξ_DB)
        return Vp_DB_1  # [kN]

    def get_Vp_DB(self, ξn_eff, Vp_kN, ξFrame, ξ_DB, Vp_DB_prev_iteraction):
        """
        Vy(DB) = VP(DB)
        Return the value of Vp_DB [kN] which will be iterated various times
        """
        # Vp_DB_prev_iteraction: previos value of Vp_DB
        Vp_DB = (ξn_eff * (Vp_kN + Vp_DB_prev_iteraction) - ξFrame * Vp_kN) / ξ_DB
        return Vp_DB  # [kN]

    def get_Kb(self, dy_DB, Vp_DB):
        Kb = Vp_DB / dy_DB
        return Kb  # [kN/m]

    def get_check(self, ξ_eff, ξn_eff):
        """
        Get the perecentage difference between ξ_eff(F+DB)/ξFrame and ξn_eff
        """
        check = (np.absolute(ξn_eff - ξ_eff) / ξ_eff) * 100
        return check  # [%]

    def get_check_Vp_DB(self, Vp_DB, Vp_DB_prev_iteraction):
        """
        Get the perecentage difference between Vp_DB and Vp_DB_prev_iteraction
        """
        check_Vp_DB = (np.absolute(Vp_DB - Vp_DB_prev_iteraction) / Vp_DB) * 100
        return check_Vp_DB


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
        """
        Return the values of the two areas generated by the
        intersection of the pushover curve with the bilinear curve
        and their difference.
        """
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

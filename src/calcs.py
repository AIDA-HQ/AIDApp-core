import numpy as np
from numpy import trapz
from scipy.stats import linregress

from coordinates import Coords

coord = Coords()


class Values:
    @staticmethod
    def convert_to_meters(coord_mm):
        """
        Convert the input array values to m
        """
        coord_m_list = []
        for element in coord_mm:
            new_coord = element / 1000
            coord_m_list.append(new_coord)
        return np.array(coord_m_list)  # [m]

    @staticmethod
    def convert_to_ms2(coord_g):
        """
        Convert the input array values to m/s^2
        """
        ms2_list = []
        for element in coord_g:
            new_coord = element * 9.81
            ms2_list.append(new_coord)
        return np.array(ms2_list)  # [m/s^2]

    @staticmethod
    def get_gamma(storey_masses, eigenvalues):
        """
        return gamma
        """
        global m_tot
        global Phi
        global MPhi
        global PhiTMTau
        global PhiTMPhi
        global m_matrix
        global gamma

        m_matrix = np.diagflat(
            storey_masses
        )  # Storey masses displayed in a diagonal matrix
        m_tot = sum(storey_masses)  # Sum all storey masses together
        Phi = np.array(eigenvalues)  # Eigenvalues displayed in a 1-coloumn matrix
        MPhi = np.matmul(m_matrix, Phi)
        PhiTMTau = np.matmul(Phi, storey_masses)
        PhiTMPhi = np.matmul(Phi, MPhi)
        gamma = PhiTMTau / PhiTMPhi
        return gamma

    @staticmethod
    def get_m_matrix():
        """
        return m_matrix
        """
        return m_matrix

    @staticmethod
    def get_m_tot():
        """
        return m_tot
        """
        return m_tot

    @staticmethod
    def get_Phi():
        """
        return Phi
        """
        return Phi

    @staticmethod
    def get_MPhi():
        """
        return MPhi
        """
        return MPhi

    @staticmethod
    def get_PhiTMTau():
        """
        Return PhiTMTau
        """
        return PhiTMTau

    @staticmethod
    def get_PhiTMPhi():
        """
        Returns PhiTMPhi
        """
        return PhiTMPhi

    @staticmethod
    def get_K1(x_p_sdof, y_p_sdof):
        """
        Calculate the slope of first 7 values of SDOF Pushover Curve
        """
        a = np.array(x_p_sdof[2:10])
        b = np.array(y_p_sdof[2:10])

        slope, _intercept, _r, _p, _se = linregress(a, b)  # kN
        return slope  # Slope

    @staticmethod
    def get_Vy_kN(K1, dy):
        """
        Returns the value of Vy(F) in kN.
        """
        global Vy_F_kN
        Vy_F_kN = K1 * dy  # kN
        return Vy_F_kN

    @staticmethod
    def get_me():
        """
        Get the mass of the storeys
        """
        global me
        me = m_tot / gamma
        return me

    @staticmethod
    def get_de(adrs_spectrum, kn_eff_curve):
        """
        X coord of Kn_eff intercepting ADRS spectrum
        """
        intersection_adrs_kn = adrs_spectrum.intersection(kn_eff_curve)
        de = float(intersection_adrs_kn.x)  # [m]
        return de

    #
    # ADRS methods
    #

    @staticmethod
    def get_Vy_F_ms2(Vy_F_kN):
        """
        Return the value of Vy(F) in m/s^2
        """
        Vy_F_ms2 = Vy_F_kN / me  # [m/s^2]
        return Vy_F_ms2

    @staticmethod
    def get_Vy_F_DB(Vp_DB):
        """
        Return the value of Vy(F + DB)
        """
        Vy_F_DB = Vy_F_kN / me + Vp_DB / me
        return Vy_F_DB  # [m/s^2]

    @staticmethod
    def get_Vp_F_DB(Vp_kN, Vp_DB):
        """
        Return the value of Vp(F + DB)
        Vp_kN is a constant, defined initally.
        Vp_DB changes every iteration.
        """
        Vp_F_DB = Vp_kN / me + Vp_DB / me
        return Vp_F_DB  # [m/s2]

    @staticmethod
    def get_kn_eff(Vp_F_DB, dp):
        kn_eff = Vp_F_DB / dp
        return kn_eff

    def get_xiFrame(self, Kf, dp, dy, Vy_kN, Vp_ms2):
        """
        Calculate the first value of xiFrame
        """
        dyF = dy  # [m]
        Vy_F_ms2 = self.get_Vy_F_ms2(Vy_kN)
        VpF_ms2 = Vp_ms2  # [m/s^2]
        xiFrame = (Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp)
        return xiFrame  # [%]

    @staticmethod
    def get_xi_eff_F_DB(Vp_kN, xi_DB, Vp_DB, xiFrame):
        """
        Return the value of xi_eff(F + DB), which,
        for the iteration 0, was called "xiFrame"
        xiFrame and Vp_kN are constants, defined initally.
        xi_DB and Vp_DB change every iteration.
        """
        xi_eff_F_DB = (xiFrame * Vp_kN + xi_DB * Vp_DB) / (Vp_kN + Vp_DB)
        return xi_eff_F_DB  # [%]

    def get_xi_n_eff_0(self, dp, adrs_spectrum, k1_eff):
        """
        Calculate first ever value of xi_n_eff
        """
        de = self.get_de(adrs_spectrum, k1_eff)

        xi_n_eff_0 = 10 * (de / dp) ** 2 - 10
        return xi_n_eff_0  # [%]

    def get_xi_n_eff(self, dp, adrs_spectrum, k1_eff_curve, xi_eff_F_DB):
        """
        Calculate iterated values of xi_n_eff
        """
        de = self.get_de(adrs_spectrum, k1_eff_curve)
        xi_n_eff = (10 + xi_eff_F_DB) * (de / dp) ** 2 - 10
        return xi_n_eff  # [%]

    @staticmethod
    def get_Sa(y_adrs_input, xi_eff_F_DB):
        """
        Calculate the value of Sa (xieff)
        coordinates after the iteration 0.
        """
        Sa_list = []
        for element in y_adrs_input:
            Sa_element = element * (10 / (10 + xi_eff_F_DB)) ** 0.5
            Sa_list.append(Sa_element)
        return np.array(Sa_list)  # [g]

    # TODO Convert the Sa values to m/s^2

    @staticmethod
    def get_T(sa_ms2_0, sd_meters_0):
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
        Calculate the value of Sd after the iteration 0.
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

    @staticmethod
    def get_xi_DB(mi_DB, k_DB):
        xi_DB = 63.7 * k_DB * ((mi_DB - 1) / mi_DB)
        return xi_DB  # [%]

    @staticmethod
    def get_dy_DB(mi_DB, dp_DB):
        dy_DB = dp_DB / mi_DB
        return dy_DB  # [m]

    @staticmethod
    def get_Vp_DB_0(xi_n_eff, Vp_kN, xi_DB, xiFrame):
        """
        Vy(DB) = VP(DB)
        Return the very first value of Vp_DB, which
        will be used by the following iteration.
        """
        Vp_DB_1 = (xi_n_eff - xiFrame) * (Vp_kN / xi_DB)
        return Vp_DB_1  # [kN]

    @staticmethod
    def get_Vp_DB(xi_n_eff, Vp_kN, xiFrame, xi_DB, Vp_DB_prev_iteration):
        """
        Vy(DB) = VP(DB)
        Return the value of Vp_DB [kN] which will be iterated various times
        """
        # Vp_DB_prev_iteration: previos value of Vp_DB
        Vp_DB = (xi_n_eff * (Vp_kN + Vp_DB_prev_iteration) - xiFrame * Vp_kN) / xi_DB
        return Vp_DB  # [kN]

    @staticmethod
    def get_Kb(dy_DB, Vp_DB):
        Kb = Vp_DB / dy_DB
        return Kb  # [kN/m]

    @staticmethod
    def get_check(xi_eff, xi_n_eff):
        """
        Get the perecentage difference between xi_eff(F+DB)/xiFrame and xi_n_eff
        """
        check = (np.absolute(xi_n_eff - xi_eff) / xi_eff) * 100
        return check  # [%]

    @staticmethod
    def get_check_Vp_DB(Vp_DB, Vp_DB_prev_iteration):
        """
        Get the perecentage difference between Vp_DB and Vp_DB_prev_iteration
        """
        check_Vp_DB = (np.absolute(Vp_DB - Vp_DB_prev_iteration) / Vp_DB) * 100
        return check_Vp_DB


class Area:
    @staticmethod
    def calculate_fitting_list(
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

    @staticmethod
    def calculate_areas(
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

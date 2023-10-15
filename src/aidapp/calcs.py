"""Main calculations for the program."""

import logging

from numpy import absolute, array, cov, cumsum, diagflat, matmul, pi, trapz

from aidapp.coordinates import Coords
from aidapp.utils import rd

coord = Coords()


class Values:
    """Class containing all the main calculations for the program."""

    def __init__(self):
        # Init all the self variables
        self.m_matrix = None
        self.m_tot = None
        self.Phi = None
        self.MPhi = None
        self.sum_MPhi = None
        self.PhiTMTau = None
        self.PhiTMPhi = None
        self.gamma = None
        self.Vy_F_kN = None
        self.me = None
        self.Vy_DB_final = None
        self.Fy_n_DB_array = None
        self.dy_DB_final = None
        self.Vy_DB_array = None
        self.dy_n_array = None
        self.dy_n_array = None

    @staticmethod
    def convert_to_meters(coord_mm):
        """Convert the input array values to m."""
        return array([(element) / 1000 for element in coord_mm])  # [m]

    @staticmethod
    def convert_to_ms2(coord_g):
        """Convert the input array values to m/s^2."""
        return array([(element) * 9.81 for element in coord_g])  # [m/s^2]

    def get_gamma(self, storey_masses, eigenvalues):
        """Return gamma."""
        self.m_matrix = diagflat(
            storey_masses
        )  # Storey masses displayed in a diagonal matrix
        self.m_tot = rd(sum(storey_masses))  # Sum all storey masses together
        self.Phi = array((eigenvalues))  # Eigenvalues displayed in a 1-column matrix
        self.MPhi = rd(
            (matmul(self.m_matrix, self.Phi))
        )  # narray containing the values of masses * eigenvalues
        self.PhiTMTau = rd(matmul(self.Phi, storey_masses))
        self.PhiTMPhi = rd(matmul(self.Phi, self.MPhi))
        self.gamma = rd(self.PhiTMTau / self.PhiTMPhi)
        return self.gamma

    def get_m_matrix(self):
        """Return m_matrix."""
        return self.m_matrix

    def get_m_tot(self):
        """Return m_tot."""
        return self.m_tot

    def get_Phi(self):
        """Return Phi."""
        return self.Phi

    def get_MPhi(self):
        """Return MPhi."""
        return self.MPhi

    def get_sum_MPhi(self):
        """Return the sum of all the values in MPhi array."""
        self.sum_MPhi = sum(self.MPhi)
        return self.sum_MPhi

    def get_PhiTMTau(self):
        """Return PhiTMTau."""
        return self.PhiTMTau

    def get_PhiTMPhi(self):
        """Returns PhiTMPhi"""
        return self.PhiTMPhi

    @staticmethod
    def get_K1(x_p_sdof, y_p_sdof):
        """Calculate the slope of first 7 values of SDOF Pushover Curve."""
        a = array(x_p_sdof[2:10])
        b = array(y_p_sdof[2:10])
        ssam, ssabm, _, _ = cov(a, b, bias=1).flat
        slope = ssabm / ssam
        return rd(slope)  # Slope

    def get_Vy_kN(self, K1, dy):
        """Returns the value of Vy(F) in kN."""
        self.Vy_F_kN = rd(K1 * dy)  # kN
        return self.Vy_F_kN

    def get_me(self):
        """Get the mass of the storeys."""
        self.me = rd(self.m_tot / self.gamma)
        logging.debug("me = %s", self.me)
        return self.me

    @staticmethod
    def get_de(adrs_spectrum, kn_eff_curve):
        """X coord of Kn_eff intercepting ADRS spectrum."""
        intersection_adrs_kn = adrs_spectrum.intersection(kn_eff_curve)
        de_x = rd(float(intersection_adrs_kn.x))  # [m]
        de_y = rd(float(intersection_adrs_kn.y))  # [m]
        return de_x, de_y

    #
    # ADRS methods
    #

    def get_Vy_F_ms2(self, Vy_F_kN):
        """Return the value of Vy(F) in m/s^2."""
        return rd(Vy_F_kN / self.me)  # [m/s^2]

    def get_Vy_F_DB(self, Vp_DB):
        """Return the value of Vy(F + DB)."""
        return rd(self.Vy_F_kN / self.me + Vp_DB / self.me)

    def get_Vp_F_DB(self, Vp_kN, Vp_DB):
        """
        Return the value of Vp(F + DB)
        Vp_kN is a constant, defined initally.
        Vp_DB changes every iteration.
        """
        return rd(Vp_kN / self.me + Vp_DB / self.me)  # [m/s2]

    @staticmethod
    def get_kn_eff(Vp_F_DB, dp):
        """Return the value of Kn_eff."""
        return rd(Vp_F_DB / dp)

    def get_xiFrame(self, Kf, dp, dy, Vy_kN, Vp_ms2):
        """Calculate the first value of xiFrame."""
        dyF = dy  # [m]
        Vy_F_ms2 = self.get_Vy_F_ms2(Vy_kN)
        VpF_ms2 = Vp_ms2  # [m/s^2]
        return rd((Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp))

    @staticmethod
    def get_xi_eff_F_DB(Vp_kN, xi_DB, Vp_DB, xiFrame):
        """
        Return the value of xi_eff(F + DB), which,
        for the iteration 0, was called "xiFrame"
        xiFrame and Vp_kN are constants, defined initally.
        xi_DB and Vp_DB change every iteration.
        """
        return rd((xiFrame * Vp_kN + xi_DB * Vp_DB) / (Vp_kN + Vp_DB))

    def get_xi_n_eff_0(self, dp, adrs_spectrum, k1_eff):
        """Calculate first ever value of xi_n_eff."""
        de_x, _ = self.get_de(adrs_spectrum, k1_eff)
        return rd(10 * (de_x / dp) ** 2 - 10)

    def get_xi_n_eff(self, dp, adrs_spectrum, k1_eff_curve):
        """Calculate iterated values of xi_n_eff."""
        de_x, _ = self.get_de(adrs_spectrum, k1_eff_curve)
        return rd(10 * ((de_x / dp) ** 2) - 10)

    @staticmethod
    def get_Sa(y_adrs_input, xi_eff_F_DB):
        """
        Calculate the value of Sa (xieff)
        coordinates after the iteration 0.
        """
        return array(
            [element * (10 / (10 + xi_eff_F_DB)) ** 0.5 for element in y_adrs_input]
        )  # [g]

    # TODO Convert the Sa values to m/s^2

    @staticmethod
    def get_T(sa_ms2_0, sd_meters_0):
        """Calculate the value of T period."""
        return rd(
            array([2 * pi * (sd / sa) ** 0.5 for sd, sa in zip(sd_meters_0, sa_ms2_0)])
        )  # [s]

    def get_Sd(self, sa_ms2_0, sd_meters_0, sa_ms2):
        """Calculate the value of Sd after the iteration 0."""
        # sa_ms2_0 is the initial array of Sa, the one input by the user
        # sa_ms2 is the array calculated by the program
        t_array = self.get_T(sa_ms2_0, sd_meters_0)
        return array(
            [sa * ((t / 2 / pi) ** 2) for sa, t in zip(sa_ms2, t_array)]
        )  # [m]

    #
    # Dissipative Brace (DB) methods
    #

    @staticmethod
    def get_xi_DB(mu_DB, k_DB):
        """
        Return the value of xi_DB [%], which remains constant
        throughout the iterations.
        """
        return rd(63.7 * k_DB * ((mu_DB - 1) / mu_DB))  # [%]

    @staticmethod
    def get_dy_DB(mu_DB, dp_DB):
        """
        Return the value of dy_DB [m], which remains constant
        throughout the iterations.
        """
        return rd(dp_DB / mu_DB)  # [m]

    @staticmethod
    def get_Vp_DB_0(xi_n_eff, Vp_kN, xi_DB, xiFrame):
        """
        Return the very first value of Vp_DB, which
        will be used by the following iteration.
        """
        return rd((xi_n_eff - xiFrame) * (Vp_kN / xi_DB))

    @staticmethod
    def get_Vp_DB(xi_n_eff, Vp_kN, xiFrame, xi_DB, Vp_DB_prev_iteration):
        """Return the value of Vp_DB [kN] which will be iterated various times."""
        # Vp_DB_prev_iteration: previos value of Vp_DB
        return rd((xi_n_eff * (Vp_kN + Vp_DB_prev_iteration) - xiFrame * Vp_kN) / xi_DB)

    @staticmethod
    def get_Kb(dy_DB, Vp_DB):
        """Return the value of Kb [kN/m]."""
        return rd(Vp_DB / dy_DB)  # [kN/m]

    @staticmethod
    def get_check(xi_eff, xi_n_eff):
        """Get the perecentage difference between xi_eff(F+DB)/xiFrame and xi_n_eff."""
        return rd((absolute(xi_n_eff - xi_eff) / xi_eff) * 100, 2)  # [%]

    @staticmethod
    def get_check_Vp_DB(Vp_DB, Vp_DB_prev_iteration):
        """Get the perecentage difference between Vp_DB and Vp_DB_prev_iteration."""
        return rd((absolute(Vp_DB - Vp_DB_prev_iteration) / Vp_DB) * 100, 2)  # [%]

    # Upwind methods

    def get_Vy_DB_final(self, Vp_DB):
        """Calculate the value of Vy(DB)."""
        self.Vy_DB_final = rd(Vp_DB * self.gamma)
        return self.Vy_DB_final

    def get_Fy_n_DB_array(self):
        """Calculate the values of Fy(DB)."""
        self.Fy_n_DB_array = []
        for element in self.MPhi:
            Fy_n_DB = rd((self.Vy_DB_final * element) / self.get_sum_MPhi())
            self.Fy_n_DB_array.append(Fy_n_DB)
        return self.Fy_n_DB_array

    def get_dy_DB_final(self, mu_DB, dp_DB):
        """Calculate the value of dy(DB)."""
        dy_db = self.get_dy_DB(mu_DB, dp_DB)
        self.dy_DB_final = rd(dy_db * self.gamma)
        return self.dy_DB_final

    def get_Vy_n_DB_array(self):
        """Calculate the values of Vy(DB)."""
        self.Vy_DB_array = rd((cumsum(self.Fy_n_DB_array[::-1]))[::-1])
        return self.Vy_DB_array

    def get_dy_n_array(self, eigenvalues):
        """Calculate the values of dy,n."""
        self.dy_n_array = []
        self.dy_n_array = [eigenvalues[0] * self.dy_DB_final] + (
            [(y - x) * self.dy_DB_final for x, y in zip(eigenvalues, eigenvalues[1:])]
        )
        return self.dy_n_array

    def get_K_storey_n_array(self):
        """Calculate the values of K_storey,n."""
        K_storey_n_array = rd(self.Vy_DB_array / self.dy_n_array)
        return K_storey_n_array

    # Frame data
    def get_K_n_DB_array(self):
        """Calculate the values of K_n(DB)."""
        K_n_DB_array = rd(self.Vy_DB_array / self.dy_n_array)
        return K_n_DB_array

    def get_Ny_n_DB_array(self):
        """Calculate the values of Ny(DB)."""
        return self.Vy_DB_array


class Area:
    """Class for the calculation to the areas under the curves."""

    @staticmethod
    def calculate_fitting_list(
        x_p_sdof,
        y_p_sdof,
        intersection_bilinear1_psdof_coords,
        intersection_bilinear2_psdof_coords,
    ):
        """
        Return the list of the X and Y coordinates between the two intersections with
        the bilinear curve, for both the first and the second area.
        """
        # List of all the X coordinates between the
        # two intersections with the bilinear curve. A1
        fitting_list_1_x_pushover = coord.find_range_pushover(
            x_p_sdof,
            intersection_bilinear1_psdof_coords[-1][0],
            intersection_bilinear2_psdof_coords[0][0],
        )

        # List of all the Y coordinates between the
        # two intersections with the bilinear curve. A1
        list_fitting_1_y_pushover = coord.find_range_pushover(
            y_p_sdof,
            intersection_bilinear1_psdof_coords[-1][1],
            intersection_bilinear2_psdof_coords[0][1],
        )

        # List of all the X coordinates between the
        # two intersections with the bilinear curve. A2
        fitting_list_2_x_pushover = coord.find_range_pushover(
            x_p_sdof,
            intersection_bilinear2_psdof_coords[0][0],
            intersection_bilinear2_psdof_coords[-1][0],
        )

        # List of all the Y coordinates between the
        # two intersections with the bilinear curve. A2
        fitting_list_2_y_pushover = coord.find_range_pushover(
            y_p_sdof,
            intersection_bilinear2_psdof_coords[0][1],
            intersection_bilinear2_psdof_coords[-1][1],
        )

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
        area_1_under_bilinear_y_coords = array(
            [
                intersection_bilinear1_psdof_coords[-1][1],
                Vy,
                intersection_bilinear2_psdof_coords[0][1],
            ]
        )
        area_1_under_bilinear_x_coords = array(
            [
                intersection_bilinear1_psdof_coords[-1][0],
                dy,
                intersection_bilinear2_psdof_coords[0][0],
            ]
        )

        area_2_under_bilinear_y_coords = array(
            [
                intersection_bilinear2_psdof_coords[0][1],
                intersection_bilinear2_psdof_coords[1][1],
            ]
        )
        area_2_under_bilinear_x_coords = array(
            [
                intersection_bilinear2_psdof_coords[0][0],
                intersection_bilinear2_psdof_coords[1][0],
            ]
        )
        area_1_under_pushover = rd(
            trapz(array(fitting_list_1_y_pushover), array(fitting_list_1_x_pushover))
        )
        logging.debug("fitting_list_1_y_pushover: %s", fitting_list_1_y_pushover)  # ok
        logging.debug("fitting_list_1_x_pushover: %s", fitting_list_1_x_pushover)
        logging.debug("area_1_under_pushover: %s", area_1_under_pushover)
        area_2_under_pushover = rd(
            trapz(array(fitting_list_2_y_pushover), array(fitting_list_2_x_pushover))
        )
        area_1_under_bilinear = rd(
            trapz(area_1_under_bilinear_y_coords, area_1_under_bilinear_x_coords)
        )
        area_2_under_bilinear = rd(
            trapz(area_2_under_bilinear_y_coords, area_2_under_bilinear_x_coords)
        )

        a1 = rd(absolute(area_1_under_pushover - area_1_under_bilinear))
        a2 = rd(absolute(area_2_under_pushover - area_2_under_bilinear))
        area_diff = rd(absolute(a1 - a2))
        return a1, a2, area_diff

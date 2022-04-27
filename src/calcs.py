from numpy import (
    absolute,
    arctan,
    array,
    cov,
    cumsum,
    diagflat,
    matmul,
    pi,
    sqrt,
    trapz,
)

from coordinates import Coords

coord = Coords()


class Values:
    @staticmethod
    def convert_to_meters(coord_mm):
        """
        Convert the input array values to m
        """
        return array([element / 1000 for element in coord_mm])  # [m]

    @staticmethod
    def convert_to_ms2(coord_g):
        """
        Convert the input array values to m/s^2
        """
        return array([element * 9.81 for element in coord_g])  # [m/s^2]

    def get_gamma(self, storey_masses, eigenvalues):
        """
        Return gamma
        """
        self.m_matrix = diagflat(
            storey_masses
        )  # Storey masses displayed in a diagonal matrix
        self.m_tot = sum(storey_masses)  # Sum all storey masses together
        self.Phi = array(eigenvalues)  # Eigenvalues displayed in a 1-coloumn matrix
        self.MPhi = matmul(
            self.m_matrix, self.Phi
        )  # narray containing the values of masses * eigenvalues
        self.PhiTMTau = matmul(self.Phi, storey_masses)
        self.PhiTMPhi = matmul(self.Phi, self.MPhi)
        self.gamma = self.PhiTMTau / self.PhiTMPhi
        return self.gamma

    def get_m_matrix(self):
        """
        return m_matrix
        """
        return self.m_matrix

    def get_m_tot(self):
        """
        return m_tot
        """
        return self.m_tot

    def get_Phi(self):
        """
        return Phi
        """
        return self.Phi

    def get_MPhi(self):
        """
        return MPhi
        """
        return self.MPhi

    def get_sum_MPhi(self):
        """
        Return the sum of all the values in MPhi array
        """
        self.sum_MPhi = sum(self.MPhi)
        return self.sum_MPhi

    def get_PhiTMTau(self):
        """
        Return PhiTMTau
        """
        return self.PhiTMTau

    def get_PhiTMPhi(self):
        """
        Returns PhiTMPhi
        """
        return self.PhiTMPhi

    @staticmethod
    def get_K1(x_p_sdof, y_p_sdof):
        """
        Calculate the slope of first 7 values of SDOF Pushover Curve
        """
        a = array(x_p_sdof[2:10])
        b = array(y_p_sdof[2:10])
        ssam, ssabm, _, _ssbm = cov(a, b, bias=1).flat
        slope = ssabm / ssam

        return slope  # Slope

    def get_Vy_kN(self, K1, dy):
        """
        Returns the value of Vy(F) in kN.
        """
        self.Vy_F_kN = K1 * dy  # kN
        return self.Vy_F_kN

    def get_me(self):
        """
        Get the mass of the storeys
        """
        self.me = self.m_tot / self.gamma
        return self.me

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

    def get_Vy_F_ms2(self, Vy_F_kN):
        """
        Return the value of Vy(F) in m/s^2
        """
        Vy_F_ms2 = Vy_F_kN / self.me  # [m/s^2]
        return Vy_F_ms2

    def get_Vy_F_DB(self, Vp_DB):
        """
        Return the value of Vy(F + DB)
        """
        Vy_F_DB = self.Vy_F_kN / self.me + Vp_DB / self.me
        return Vy_F_DB  # [m/s^2]

    def get_Vp_F_DB(self, Vp_kN, Vp_DB):
        """
        Return the value of Vp(F + DB)
        Vp_kN is a constant, defined initally.
        Vp_DB changes every iteration.
        """
        Vp_F_DB = Vp_kN / self.me + Vp_DB / self.me
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
        return array(
            [element * (10 / (10 + xi_eff_F_DB)) ** 0.5 for element in y_adrs_input]
        )  # [g]

    # TODO Convert the Sa values to m/s^2

    @staticmethod
    def get_T(sa_ms2_0, sd_meters_0):
        """
        Calculate the value of T period
        """
        return array(
            [2 * pi * (sd / sa) ** 0.5 for sd, sa in zip(sd_meters_0, sa_ms2_0)]
        )  # [s]

    def get_Sd(self, sa_ms2_0, sd_meters_0, sa_ms2):
        """
        Calculate the value of Sd after the iteration 0.
        """
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
        xi_DB = 63.7 * k_DB * ((mu_DB - 1) / mu_DB)
        return xi_DB  # [%]

    @staticmethod
    def get_dy_DB(mu_DB, dp_DB):
        dy_DB = dp_DB / mu_DB
        return dy_DB  # [m]

    @staticmethod
    def get_Vp_DB_0(xi_n_eff, Vp_kN, xi_DB, xiFrame):
        """
        Return the very first value of Vp_DB, which
        will be used by the following iteration.
        """
        Vp_DB_1 = (xi_n_eff - xiFrame) * (Vp_kN / xi_DB)
        return Vp_DB_1  # [kN]

    @staticmethod
    def get_Vp_DB(xi_n_eff, Vp_kN, xiFrame, xi_DB, Vp_DB_prev_iteration):
        """
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
        check = (absolute(xi_n_eff - xi_eff) / xi_eff) * 100
        return check  # [%]

    @staticmethod
    def get_check_Vp_DB(Vp_DB, Vp_DB_prev_iteration):
        """
        Get the perecentage difference between Vp_DB and Vp_DB_prev_iteration
        """
        check_Vp_DB = (absolute(Vp_DB - Vp_DB_prev_iteration) / Vp_DB) * 100
        return check_Vp_DB

    # Upwinds methods

    def get_Vy_DB_final(self, Vp_DB):
        """
        Calculate the value of Vy(DB)
        """
        self.Vy_DB_final = Vp_DB * self.gamma
        return self.Vy_DB_final

    def get_Fy_n_DB_array(self):
        """
        Calculate the values of Fy(DB)
        """
        self.Fy_n_DB_array = []
        for element in self.MPhi:
            Fy_n_DB = (self.Vy_DB_final * element) / self.get_sum_MPhi()
            self.Fy_n_DB_array.append(Fy_n_DB)
        return self.Fy_n_DB_array

    def get_dy_DB_final(self, mu_DB, dp_DB):
        """
        Calculate the value of dy(DB)
        """
        dy_db = self.get_dy_DB(mu_DB, dp_DB)
        self.dy_DB_final = dy_db * self.gamma
        return self.dy_DB_final

    def get_Vy_n_DB_array(self):
        """
        Calculate the values of Vy(DB)
        """
        self.Vy_DB_array = (cumsum(self.Fy_n_DB_array[::-1]))[::-1]
        return self.Vy_DB_array

    def get_dy_n_array(self, eigenvalues):
        """
        Calculate the values of dy,n
        """
        self.dy_n_array = []
        self.dy_n_array = [eigenvalues[0] * self.dy_DB_final] + (
            [(y - x) * self.dy_DB_final for x, y in zip(eigenvalues, eigenvalues[1:])]
        )
        return self.dy_n_array

    def get_K_storey_n_array(self):
        """
        Calculate the values of K_storey,n
        """
        K_storey_n_array = self.Vy_DB_array / self.dy_n_array
        return K_storey_n_array

    ## Frame data
    def get_upwind_lenght(self, span_length, interfloor_height):
        """
        Calculate the lenght of the upwind
        """
        upwind_lenght = sqrt(span_length**2 + interfloor_height**2)
        return upwind_lenght

    def get_slope(self, span_length, interfloor_height):
        """
        Calculate the slope of the upwind
        """
        slope = arctan(interfloor_height / span_length)
        return slope

    def cos_alpha(self, span_length, upwind_lenght):
        """
        Calculate the cos(alpha) of the upwind
        """
        cos_alpha = span_length / upwind_lenght
        return cos_alpha

    def get_K_n_DB_array(self, span_length, interfloor_height):
        """
        Calculate the values of K_n(DB)
        """
        upwind_lenght = self.get_upwind_lenght(span_length, interfloor_height)
        self.K_n_DB_array = self.Vy_DB_array / (
            self.dy_n_array * array(self.cos_alpha(span_length, upwind_lenght) ** 2)
        )
        return self.K_n_DB_array

    def get_Ny_n_DB_array(self, span_length, interfloor_height):
        """
        Calculate the values of Ny(DB)
        """
        Ny_n_DB_array = []
        upwind_lenght = self.get_upwind_lenght(span_length, interfloor_height)
        for element in self.Vy_DB_array:
            Ny_n_DB = element / self.cos_alpha(span_length, upwind_lenght)
            Ny_n_DB_array.append(Ny_n_DB)
        return Ny_n_DB_array

    def get_kc_n_s_array(self, brace_number):
        """
        Calculate the values of the brace rigidity for each floor (kc_n_s)
        """
        kc_n_s_array = []
        k = 0
        for element in self.K_n_DB_array:
            kc_n_s = element / brace_number[0 + k]
            k = k + 1
            kc_n_s_array.append(kc_n_s)
        return kc_n_s_array

    def get_Fc_n_s_array(self, brace_number, span_length, interfloor_height):
        """
        Calculate the values of the brace force for each floor (Fc_n_s)
        """
        Fc_n_s_array = []
        k = 0
        for element in self.get_Ny_n_DB_array(span_length, interfloor_height):
            Fc_n_s = element / brace_number[0 + k]
            k = k + 1
            Fc_n_s_array.append(Fc_n_s)
        return Fc_n_s_array


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
        area_1_under_pushover = trapz(
            array(fitting_list_1_y_pushover), array(fitting_list_1_x_pushover)
        )
        area_2_under_pushover = trapz(
            array(fitting_list_2_y_pushover), array(fitting_list_2_x_pushover)
        )
        area_1_under_bilinear = trapz(
            area_1_under_bilinear_y_coords, area_1_under_bilinear_x_coords
        )
        area_2_under_bilinear = trapz(
            area_2_under_bilinear_y_coords, area_2_under_bilinear_x_coords
        )

        a1 = absolute(area_1_under_pushover - area_1_under_bilinear)
        a2 = absolute(area_2_under_pushover - area_2_under_bilinear)
        area_diff = absolute(a1 - a2)
        return a1, a2, area_diff

"""Main module of the AIDApp."""

from numpy import array

from aidapp.calcs import Area, Values
from aidapp.coordinates import Coords
from aidapp.file_handler import InputHandler
from aidapp.ntc import Ntc
from aidapp.utils import rd
import logging

area = Area()
coord = Coords()
values = Values()
handlr = InputHandler()


class AIDApp:
    """Class to run the app backend."""

    def __init__(self):
        # Init all the self variables
        self.dp = None
        self.mu_DB = None
        self.k_DB = None
        self.Kf = None
        self.storey_masses = None
        self.eigenvalues = None
        self.pushover_x = None
        self.pushover_y = None
        self.ag_input = None
        self.fo_input = None
        self.tc_input = None
        self.span_length = None
        self.interfloor_height = None
        self.brace_number = None
        self.nominal_age = None
        self.functional_class = None
        self.topographic_factor = None
        self.soil_class = None
        self.limit_state = None
        self.damping_coeff = None
        self.gamma = None
        self.me = None
        self.y_p_sdof = None
        self.x_p_sdof = None
        self.y_kn_eff = None
        self.x_kn_eff = None
        self.Vp_kN = None
        self.Vp_ms2 = None
        self.K1 = None
        self.de_n = None

    def main(
        self,
        arg_dp,
        arg_mu_DB,
        arg_k_DB,
        arg_Kf,
        arg_storey_masses,
        arg_eigenvalues,
        arg_brace_number,
        arg_path_zonation,
        arg_pushover_x,
        arg_pushover_y,
        arg_span_length,
        arg_interfloor_height,
        arg_nominal_age,
        arg_functional_class,
        arg_topographic_factor,
        arg_soil_class,
        arg_limit_state,
        arg_damping_coeff,
    ):
        """Main function of the app."""
        self.mu_DB = arg_mu_DB
        self.k_DB = arg_k_DB
        self.Kf = arg_Kf
        self.storey_masses = rd(arg_storey_masses)
        self.eigenvalues = rd(arg_eigenvalues)
        self.pushover_x = handlr.generate_array(arg_pushover_x)
        self.pushover_y = handlr.generate_array(arg_pushover_y)
        self.ag_input = handlr.generate_array(arg_path_zonation[0])
        self.fo_input = handlr.generate_array(arg_path_zonation[1])
        self.tc_input = handlr.generate_array(arg_path_zonation[2])
        self.span_length = arg_span_length
        self.interfloor_height = arg_interfloor_height
        self.brace_number = arg_brace_number
        self.nominal_age = arg_nominal_age
        self.functional_class = arg_functional_class
        self.topographic_factor = arg_topographic_factor
        self.soil_class = arg_soil_class
        self.limit_state = arg_limit_state
        self.damping_coeff = arg_damping_coeff

        self.gamma = values.get_gamma(self.storey_masses, self.eigenvalues)
        self.dp = rd(arg_dp / self.gamma)  # [m]
        logging.debug("dp: %s", self.dp)
        self.me = values.get_me()  # [ton]
        self.y_p_sdof = coord.y_p_sdof(self.gamma, self.pushover_y)
        self.x_p_sdof = coord.x_p_sdof(self.gamma, self.pushover_x)
        self.Vp_kN = self.y_p_sdof[
            coord.find_nearest_coordinate_index(self.x_p_sdof, self.dp)
        ]
        self.Vp_ms2 = rd(self.Vp_kN / self.me)  # m/s^2

        # Slope of first n values of SDOF Pushover Curve
        self.K1 = values.get_K1(self.x_p_sdof, self.y_p_sdof)  # [kN/m]
        logging.debug("K1: %s", self.K1)
        return self.find_dy(0.0100)

    def find_dy(self, dy):
        """
        Find the dy value, by iterating over the function 'get_calcs_recursive' until
        the difference between the areas is less than 0.0004.
        """
        Vy_kN = values.get_Vy_kN(self.K1, dy)

        # X coordinates of the bilinear curve
        x_bilinear = array([0, dy, self.dp])

        # Y coords of the bilinear curve in [kN]
        y_bilinear_kN = array([0, Vy_kN, self.Vp_kN])

        # Graphs
        p_sdof = coord.interpolate_curve(self.x_p_sdof, self.y_p_sdof)

        # Straight line passing through 1st and 2nd point of bilinear curve
        # Generate the 1st part of the bilinear
        bilinear_line_kN_1 = coord.bilinear_line(
            self.x_p_sdof,
            x_bilinear[0],
            x_bilinear[1],
            y_bilinear_kN[0],
            y_bilinear_kN[1],
        )
        # Intersections of bilinear #1
        intersection_bilinear1_psdof_coords = coord.find_intersections(
            p_sdof, bilinear_line_kN_1
        )

        # Straight line passing through 2nd and 3rd point of the bilinear curve
        # Generate the 2nd part of the bilinear
        bilinear_line_kN_2 = coord.bilinear_line(
            self.x_p_sdof,
            x_bilinear[1],
            x_bilinear[2],
            y_bilinear_kN[1],
            y_bilinear_kN[2],
        )

        # Intersections of bilinear #2
        intersection_bilinear2_psdof_coords = coord.find_intersections(
            p_sdof, bilinear_line_kN_2
        )

        (
            fitting_list_1_x_pushover,
            fitting_list_1_y_pushover,
            fitting_list_2_x_pushover,
            fitting_list_2_y_pushover,
        ) = area.calculate_fitting_list(
            self.x_p_sdof,
            self.y_p_sdof,
            intersection_bilinear1_psdof_coords,
            intersection_bilinear2_psdof_coords,
        )

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
        logging.debug("a1: %s", a1)
        logging.debug("a2: %s", a2)
        logging.debug("area_diff: %s", area_diff)

        if rd(area_diff, 2) <= rd(0.01):
            logging.debug("area_diff: %s", area_diff)
            ntc = Ntc(
                self.limit_state,
                self.nominal_age,
                self.functional_class,
                self.soil_class,
                self.topographic_factor,
                self.ag_input,
                self.fo_input,
                self.tc_input,
                self.damping_coeff,
            )
            sd_meters = ntc.get_movement_curve_SDe()
            sa_ms2_0 = values.convert_to_ms2(ntc.get_acceleration_curve_Se())
            adrs_spectrum = coord.interpolate_curve(sd_meters, sa_ms2_0)
            k_eff = rd(self.Vp_ms2 / self.dp)

            k1_eff_curve = coord.interpolate_curve(
                sd_meters,
                coord.y_kn_eff(sd_meters, k_eff),
            )

            # Sui generis first iteration
            xiFrame = values.get_xiFrame(self.Kf, self.dp, dy, Vy_kN, self.Vp_ms2)

            xi_n_eff = values.get_xi_n_eff_0(self.dp, adrs_spectrum, k1_eff_curve)
            xi_DB = values.get_xi_DB(self.mu_DB, self.k_DB)
            Vp_DB_prev_iteration = values.get_Vp_DB_0(
                xi_n_eff, self.Vp_kN, xi_DB, xiFrame
            )

            check = values.get_check(xiFrame, xi_n_eff)
            Vp_DB = Vp_DB_prev_iteration

            Vp_F = rd(self.Vp_kN / self.me)
            logging.debug("Vp_F: %s", Vp_F)
            de_0 = values.get_de(adrs_spectrum, k1_eff_curve)
            logging.debug("de_0: %s", de_0)

            def get_calcs_recursive(
                Vp_DB,
                check,
                i,
                sa_ms2,
                Vy_F_DB,
                Vp_F_DB,
                kn_eff,
                xi_eff_F_DB,
                xi_n_eff,
                check_Vp_DB,
            ):
                """Recursive function to calculate what's needed.
                If the difference is more than 0.5 keep iterating,
                otherwise return the values.
                """
                if check > 0.5:
                    i = i + 1
                    xi_eff_F_DB = values.get_xi_eff_F_DB(
                        self.Vp_kN, xi_DB, Vp_DB, xiFrame
                    )
                    sa_ms2 = values.convert_to_ms2(ntc.get_acceleration_curve_Se())

                    Vp_DB_prev_iteration = Vp_DB

                    Vy_F_DB = values.get_Vy_F_DB(Vp_DB)
                    Vp_F_DB = values.get_Vp_F_DB(self.Vp_kN, Vp_DB)
                    kn_eff = values.get_kn_eff(Vp_F_DB, self.dp)
                    kn_eff_curve = coord.interpolate_curve(
                        sd_meters,
                        coord.y_kn_eff(sd_meters, kn_eff),
                    )
                    xi_n_eff = values.get_xi_n_eff(self.dp, adrs_spectrum, kn_eff_curve)
                    Vp_DB = values.get_Vp_DB(
                        xi_n_eff, self.Vp_kN, xiFrame, xi_DB, Vp_DB_prev_iteration
                    )
                    self.de_n = values.get_de(adrs_spectrum, kn_eff_curve)

                    check = values.get_check(xi_eff_F_DB, xi_n_eff)
                    check_Vp_DB = values.get_check_Vp_DB(Vp_DB, Vp_DB_prev_iteration)

                    return get_calcs_recursive(
                        Vp_DB,
                        check,
                        i,
                        sa_ms2,
                        Vy_F_DB,
                        Vp_F_DB,
                        kn_eff,
                        xi_eff_F_DB,
                        xi_n_eff,
                        check_Vp_DB,
                    )

                # If the difference between ViP(DB) and V(i-1)P(DB) is less
                # than 5% return the values
                values.get_Vy_DB_final(Vp_DB)
                values.get_Fy_n_DB_array()
                values.get_dy_DB_final(self.mu_DB, self.dp)
                values.get_Vy_n_DB_array().tolist()
                values.get_dy_n_array(self.eigenvalues)
                values.get_K_storey_n_array().tolist()
                values.get_K_n_DB_array(self.span_length, self.interfloor_height)
                kc_n_s_array = values.get_kc_n_s_array(self.brace_number)
                Fc_n_s_array = values.get_Fc_n_s_array(
                    self.brace_number, self.span_length, self.interfloor_height
                )
                return [
                    i,
                    kc_n_s_array,
                    Fc_n_s_array,
                    de_0,
                    self.de_n,
                    self.dp,
                ]

            return get_calcs_recursive(
                Vp_DB, check, 1, None, None, None, None, None, None, None
            )
        dy = rd(dy + 0.00001)
        logging.debug("dy: %s", dy)

        return self.find_dy(dy)

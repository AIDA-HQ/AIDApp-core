"""Main module of the AIDApp."""

import logging
from numpy import array

from aidapp.calcs import Area, Values
from aidapp.coordinates import Coords
import aidapp.file_handler as fh
from aidapp.ntc import Ntc
from aidapp.utils import rd

area = Area()
coord = Coords()
values = Values()


def main(input_values):
    """Main function of the app."""
    storey_masses = rd(input_values.storey_masses)
    eigenvalues = rd(input_values.eigenvalues)
    pushover_x = rd(input_values.pushover_x)
    pushover_y = rd(input_values.pushover_y)
    ag_input = rd(input_values.zonation_0)
    fo_input = rd(input_values.zonation_1)
    tc_input = rd(input_values.zonation_2)

    gamma = values.get_gamma(storey_masses, eigenvalues)
    dp = rd(input_values.dp / gamma)  # [m]
    logging.debug("dp: %s", dp)
    me = values.get_me()  # [ton]
    y_p_sdof = coord.y_p_sdof(gamma, pushover_y)
    x_p_sdof = coord.x_p_sdof(gamma, pushover_x)
    Vp_kN = y_p_sdof[coord.find_nearest_coordinate_index(x_p_sdof, dp)]
    Vp_ms2 = rd(Vp_kN / me)  # m/s^2

    # Slope of first n values of SDOF Pushover Curve
    k1 = values.get_K1(x_p_sdof, y_p_sdof)  # [kN/m]
    logging.debug("K1: %s", k1)

    def find_dy(dy):
        """
        Find the dy value, by iterating over the function 'get_calcs_recursive' until
        the difference between the areas is less than 0.0004.
        """
        Vy_kN = values.get_Vy_kN(k1, dy)

        # X coordinates of the bilinear curve
        x_bilinear = array([0, dy, dp])

        # Y coords of the bilinear curve in [kN]
        y_bilinear_kN = array([0, Vy_kN, Vp_kN])

        # Graphs
        p_sdof = coord.interpolate_curve(x_p_sdof, y_p_sdof)

        # Straight line passing through 1st and 2nd point of bilinear curve
        # Generate the 1st part of the bilinear
        bilinear_line_kN_1 = coord.bilinear_line(
            x_p_sdof,
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
            x_p_sdof,
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
            x_p_sdof,
            y_p_sdof,
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
                input_values.limit_state,
                input_values.nominal_age,
                input_values.functional_class,
                input_values.soil_class,
                input_values.topographic_factor,
                ag_input,
                fo_input,
                tc_input,
                input_values.damping_coeff,
            )
            sd_meters = ntc.get_movement_curve_SDe()
            sa_ms2_0 = values.convert_to_ms2(ntc.get_acceleration_curve_Se())
            adrs_spectrum = coord.interpolate_curve(sd_meters, sa_ms2_0)
            k_eff = rd(Vp_ms2 / dp)

            k1_eff_curve = coord.interpolate_curve(
                sd_meters,
                coord.y_kn_eff(sd_meters, k_eff),
            )

            # Sui generis first iteration
            xiFrame = values.get_xiFrame(input_values.kf, dp, dy, Vy_kN, Vp_ms2)

            xi_n_eff = values.get_xi_n_eff_0(dp, adrs_spectrum, k1_eff_curve)
            xi_DB = values.get_xi_DB(input_values.mu_DB, input_values.k_DB)
            Vp_DB_prev_iteration = values.get_Vp_DB_0(xi_n_eff, Vp_kN, xi_DB, xiFrame)

            check = values.get_check(xiFrame, xi_n_eff)
            Vp_DB = Vp_DB_prev_iteration

            Vy_F_DB_0 = values.get_Vy_F_ms2(Vy_kN)
            Vp_F = rd(Vp_kN / me)
            kn_eff_list_0 = coord.y_kn_eff(sd_meters, k_eff)
            y_bilinear_ms2_0 = array([0, Vy_F_DB_0, Vp_F])
            logging.debug("Vp_F: %s", Vp_F)
            de_0 = values.get_de(adrs_spectrum, k1_eff_curve)
            logging.debug("de_0: %s", de_0)
            sa_ms2 = values.convert_to_ms2(ntc.get_acceleration_curve_Se())

            def get_calcs_recursive(Vp_DB, check, i, Vy_F_DB, Vp_F_DB, kn_eff, de_n):
                """
                Recursive function to calculate what's needed.
                If the difference is more than 0.5 keep iterating,
                otherwise return the values.
                """
                if check > 0.5:
                    i = i + 1
                    xi_eff_F_DB = values.get_xi_eff_F_DB(Vp_kN, xi_DB, Vp_DB, xiFrame)
                    Vp_DB_prev_iteration = Vp_DB
                    Vy_F_DB = values.get_Vy_F_DB(Vp_DB)
                    Vp_F_DB = values.get_Vp_F_DB(Vp_kN, Vp_DB)
                    kn_eff = values.get_kn_eff(Vp_F_DB, dp)
                    kn_eff_curve = coord.interpolate_curve(
                        sd_meters,
                        coord.y_kn_eff(sd_meters, kn_eff),
                    )
                    xi_n_eff = values.get_xi_n_eff(dp, adrs_spectrum, kn_eff_curve)
                    Vp_DB = values.get_Vp_DB(
                        xi_n_eff, Vp_kN, xiFrame, xi_DB, Vp_DB_prev_iteration
                    )
                    de_n = values.get_de(adrs_spectrum, kn_eff_curve)
                    check = values.get_check(xi_eff_F_DB, xi_n_eff)

                    return get_calcs_recursive(
                        Vp_DB, check, i, Vy_F_DB, Vp_F_DB, kn_eff, de_n
                    )

                # If the difference between ViP(DB) and V(i-1)P(DB) is less
                # than 5% return the values
                kn_eff_list = coord.y_kn_eff(sd_meters, kn_eff)
                y_bilinear_ms2 = array([0, Vy_F_DB, Vp_F_DB])
                values.get_Vy_DB_final(Vp_DB)
                values.get_Fy_n_DB_array()
                values.get_dy_DB_final(input_values.mu_DB, dp)
                values.get_Vy_n_DB_array().tolist()
                values.get_dy_n_array(eigenvalues)
                values.get_K_storey_n_array().tolist()
                values.get_K_n_DB_array(
                    input_values.span_length, input_values.interfloor_height
                )
                kc_n_s_array = values.get_kc_n_s_array(input_values.brace_number)
                Fc_n_s_array = values.get_Fc_n_s_array(
                    input_values.brace_number,
                    input_values.span_length,
                    input_values.interfloor_height,
                )

                return [
                    kc_n_s_array,
                    Fc_n_s_array,
                    i,
                    x_bilinear,
                    y_bilinear_ms2,
                    sd_meters,
                    sa_ms2,
                    kn_eff_list,
                    y_bilinear_ms2_0,
                    kn_eff_list_0,
                    de_0,
                    de_n,
                    dp,
                ]

            return get_calcs_recursive(Vp_DB, check, 1, None, None, None, None)
        dy = rd(dy + 0.00001)
        logging.debug("dy: %s", dy)
        return find_dy(dy)

    return find_dy(0.0100)

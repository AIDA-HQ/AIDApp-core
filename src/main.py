from numpy import array

from calcs import Area, Values
from coordinates import Coords
from input_coordinates import Input
from coordinate_handler import CoordinateHandler

area = Area()
coord = Coords()
input_coord = Input()
values = Values()
handlr = CoordinateHandler()


class AIDApp:
    def main(
        self, arg_dp, arg_mu_DB, arg_k_DB, arg_Kf, arg_storey_masses, arg_eigenvalues, arg_path_x, arg_path_y
    ):

        self.dp = arg_dp
        self.mu_DB = arg_mu_DB
        self.k_DB = arg_k_DB
        self.Kf = arg_Kf
        self.storey_masses = arg_storey_masses
        self.eigenvalues = arg_eigenvalues
        self.path_x = handlr.generate_array(arg_path_x)
        self.path_y = handlr.generate_array(arg_path_y)

        self.gamma = values.get_gamma(self.storey_masses, self.eigenvalues)
        self.me = values.get_me()  # [ton]
        self.y_p_sdof = coord.y_p_sdof(self.gamma, self.path_y)
        self.x_p_sdof = coord.x_p_sdof(self.gamma, self.path_x)
        self.Vp_kN = self.y_p_sdof[coord.find_nearest_coordinate_index(self.x_p_sdof, self.dp)]
        self.Vp_ms2 = self.Vp_kN / self.me  # m/s^2

        # Slope of first n values of SDOF Pushover Curve
        self.K1 = values.get_K1(self.x_p_sdof, self.y_p_sdof)  # [kN/m]
        return self.find_dy(0.0100)

    def find_dy(self, dy):
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
            self.x_p_sdof, x_bilinear[0], x_bilinear[1], y_bilinear_kN[0], y_bilinear_kN[1]
        )
        # Intersections of bilinear #1
        intersection_bilinear1_psdof_coords = coord.find_intersections(
            p_sdof, bilinear_line_kN_1
        )

        # Straight line passing through 2nd and 3rd point of the bilinear curve
        # Generate the 2nd part of the bilinear
        bilinear_line_kN_2 = coord.bilinear_line(
            self.x_p_sdof, x_bilinear[1], x_bilinear[2], y_bilinear_kN[1], y_bilinear_kN[2]
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

        _a1, _a2, area_diff = areas_kN

        if area_diff < 0.0004:
            sd_meters_0 = values.convert_to_meters(input_coord.x_adrs_input)
            sa_ms2_0 = values.convert_to_ms2(input_coord.y_adrs_input)
            adrs_spectrum = coord.interpolate_curve(sd_meters_0, sa_ms2_0)
            k_eff = self.Vp_ms2 / self.dp

            k1_eff_curve = coord.interpolate_curve(
                sd_meters_0,
                coord.y_kn_eff(sd_meters_0, k_eff),
            )

            # Sui generis first iteration
            xiFrame = values.get_xiFrame(self.Kf, self.dp, dy, Vy_kN, self.Vp_ms2)

            xi_n_eff = values.get_xi_n_eff_0(self.dp, adrs_spectrum, k1_eff_curve)
            xi_DB = values.get_xi_DB(self.mu_DB, self.k_DB)
            Vp_DB_prev_iteration = values.get_Vp_DB_0(xi_n_eff, self.Vp_kN, xi_DB, xiFrame)

            check = values.get_check(xiFrame, xi_n_eff)
            Vp_DB = Vp_DB_prev_iteration

            # Recursive function to calculate what's needed
            def get_calcs_recursive(
                Vp_DB,
                check,
                i,
                sd_meters,
                sa_ms2,
                Vy_F_DB,
                Vp_F_DB,
                kn_eff,
                xi_eff_F_DB,
                xi_n_eff,
                check_Vp_DB,
            ):
                if check > 0.5:
                    i = i + 1
                    xi_eff_F_DB = values.get_xi_eff_F_DB(self.Vp_kN, xi_DB, Vp_DB, xiFrame)
                    sa_ms2 = values.convert_to_ms2(
                        values.get_Sa(input_coord.y_adrs_input, xi_eff_F_DB)
                    )
                    sd_meters = values.get_Sd(sa_ms2_0, sd_meters_0, sa_ms2)

                    adrs_spectrum = coord.interpolate_curve(sd_meters, sa_ms2)

                    Vp_DB_prev_iteration = Vp_DB

                    Vy_F_DB = values.get_Vy_F_DB(Vp_DB)
                    Vp_F_DB = values.get_Vp_F_DB(self.Vp_kN, Vp_DB)
                    kn_eff = values.get_kn_eff(Vp_F_DB, self.dp)
                    kn_eff_curve = coord.interpolate_curve(
                        sd_meters,
                        coord.y_kn_eff(sd_meters, kn_eff),
                    )
                    xi_n_eff = values.get_xi_n_eff(
                        self.dp, adrs_spectrum, kn_eff_curve, xi_eff_F_DB
                    )
                    Vp_DB = values.get_Vp_DB(
                        xi_n_eff, self.Vp_kN, xiFrame, xi_DB, Vp_DB_prev_iteration
                    )

                    check = values.get_check(xi_eff_F_DB, xi_n_eff)
                    check_Vp_DB = values.get_check_Vp_DB(Vp_DB, Vp_DB_prev_iteration)

                    return get_calcs_recursive(
                        Vp_DB,
                        check,
                        i,
                        sd_meters,
                        sa_ms2,
                        Vy_F_DB,
                        Vp_F_DB,
                        kn_eff,
                        xi_eff_F_DB,
                        xi_n_eff,
                        check_Vp_DB,
                    )

                if check <= 0.5:
                    kn_eff_list = coord.y_kn_eff(sd_meters, kn_eff)
                    y_bilinear_ms2 = array([0, Vy_F_DB, Vp_F_DB])
                    dy_DB = values.get_dy_DB(self.mu_DB, self.dp)
                    kb = values.get_Kb(dy_DB, Vp_DB)
                    Vy_DB_final = values.get_Vy_DB_final(Vp_DB)
                    Fy_n_DB_array = values.get_Fy_n_DB_array()
                    return [
                        Vp_DB,
                        Vy_DB_final,
                        Fy_n_DB_array,
                        check,
                        i,
                        Vy_F_DB,
                        Vp_F_DB,
                        kn_eff,
                        xi_eff_F_DB,
                        xi_n_eff,
                        check_Vp_DB,
                        x_bilinear,
                        y_bilinear_ms2,
                        sd_meters,
                        sa_ms2,
                        kn_eff_list,
                        sd_meters_0,
                        sa_ms2_0,
                        dy_DB,
                        kb,
                    ]

            return get_calcs_recursive(
                Vp_DB, check, 1, None, None, None, None, None, None, None, None
            )
        dy = dy + 0.00001

        return self.find_dy(dy)

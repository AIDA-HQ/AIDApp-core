from calcs import Values

values = Values()


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
        k1_eff_curve,
    ):
        print("Storey masses Matrix:\n", values.get_m_matrix(), "\n")
        print("Eigenvalues Matrix:\n", values.get_φ(), "\n")
        print("Modal pattern:\n", values.get_Mφ())
        print("\nφTMτ:", values.get_φTMτ())
        print("φTMφ:", values.get_φTMφ())
        # TODO print("Γ:", Γ)
        print("Vp_kn:", Vp_kN)
        print("de:", values.get_de(adrs_spectrum, k1_eff_curve))

        print("Vy(F):", Vy_F_ms2, "m/s^2")
        print("dp(F):", dp, "m")
        print("Vp(F):", VpF_ms2, "m/s^2")
        print("de:", de, "m")
        print("\nξn_eff:", self.get_ξn_eff(), "%")

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

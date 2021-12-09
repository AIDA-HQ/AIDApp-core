from calcs import Values

values = Values()


class Print:
    @staticmethod
    def print_brief(
        i,
        Vy_F_DB,
        Vp_F_DB,
        ξ_eff_F_DB,
        Vp_DB_prev_iteration,
        ξn_eff,
        Vp_DB,
        check,
        check_Vp_DB,
    ):
        """
        Print some brief information about the current iteration.
        """
        print("Iteraction #", i)
        print("Vp_DB:", Vp_DB)
        print("Vy_F_DB: " + str(Vy_F_DB) + " m/s^2")
        print("Vp_F_DB: " + str(Vp_F_DB) + " m/s^2")
        print("ξ_eff_F_DB: " + str(ξ_eff_F_DB) + " %")
        print("Vp_DB_prev_iteration: ", Vp_DB_prev_iteration)
        print("ξ" + str(i) + "_eff: " + str(ξn_eff))
        print("check: " + str(check) + " %")
        print("check_Vp_DB: " + str(check_Vp_DB) + " %")
        print("\n")

    @staticmethod
    def print_iteration_zero(ξFrame, ξn_eff, Vp_DB, check):
        """
        Print information about the iteration 0.
        """
        print("\n")
        print("Iteraction #", 1)
        print("Vp_DB:", Vp_DB)
        print("ξn_eff:", ξn_eff)
        print("ξFrame:", ξFrame)
        print("check: " + str(check) + " %")
        print("\n")

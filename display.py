from calcs import Values

values = Values()


class Print:
    def print_brief(
        self,
        i,
        Vy_F_DB,
        Vp_F_DB,
        ξ_eff_F_DB,
        Vp_DB_prev_iteraction,
        ξn_eff,
        Vp_DB,
        check,
        check_Vp_DB,
    ):
        """
        Print some brief information about the current iteration.
        """
        print("Iteraction #", i)
        print("Vy_F_DB: " + str(Vy_F_DB) + "m/s^2")
        print("Vp_F_DB: " + str(Vp_F_DB) + "m/s^2")
        print("ξ_eff_F_DB: " + str(ξ_eff_F_DB) + "%")
        print("Vp_DB_prev_iteraction: ", Vp_DB_prev_iteraction)
        print("ξ" + str(i) + "_eff: " + str(ξn_eff))
        print("Vp_DB:", Vp_DB)
        print("check: " + str(check) + "%")
        print("check_Vp_DB: " + str(check_Vp_DB) + "%")
        print("\n")

    def print_iteration_zero(self, ξFrame, ξn_eff, Vp_DB, check):
        """
        Print information about the iteration 0.
        """
        print("\n")
        print("Iteraction #", 1)
        print("ξn_eff:", ξn_eff)
        print("ξFrame:", ξFrame)
        print("Vp_DB:", Vp_DB)
        print("check: " + str(check) + "%")
        print("\n")

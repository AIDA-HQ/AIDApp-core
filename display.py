from calcs import Values

values = Values()


class Print:
    @staticmethod
    def print_brief(
        i,
        Vy_F_DB,
        Vp_F_DB,
        xi_eff_F_DB,
        Vp_DB_prev_iteration,
        xi_n_eff,
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
        print("xi_eff_F_DB: " + str(xi_eff_F_DB) + " %")
        print("Vp_DB_prev_iteration: ", Vp_DB_prev_iteration)
        print("xi" + str(i) + "_eff: " + str(xi_n_eff))
        print("check: " + str(check) + " %")
        print("check_Vp_DB: " + str(check_Vp_DB) + " %")
        print("\n")

    @staticmethod
    def print_iteration_zero(xiFrame, xi_n_eff, Vp_DB, check):
        """
        Print information about the iteration 0.
        """
        print("\n")
        print("Iteraction #", 1)
        print("Vp_DB:", Vp_DB)
        print("xi_n_eff:", xi_n_eff)
        print("xiFrame:", xiFrame)
        print("check: " + str(check) + " %")
        print("\n")

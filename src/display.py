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
        print(f"Iteraction #{i}")
        print(f"Vp_DB: {Vp_DB}")
        print(f"Vy_F_DB: {Vy_F_DB} m/s^2")
        print(f"Vp_F_DB: {Vp_F_DB} m/s^2")
        print(f"xi_eff_F_DB: {xi_eff_F_DB} %")
        print(f"Vp_DB_prev_iteration: {Vp_DB_prev_iteration}")
        print(f"xi{i} _eff: {xi_n_eff}")
        print(f"check: {check} %")
        print(f"check_Vp_DB: {check_Vp_DB} %")
        print("\n")

    @staticmethod
    def print_iteration_zero(xiFrame, xi_n_eff, Vp_DB, check):
        """
        Print information about the iteration 0.
        """
        print("\n")
        print("Iteraction #1")
        print(f"Vp_DB: {Vp_DB}")
        print(f"xi_n_eff: {xi_n_eff}")
        print(f"xiFrame: {xiFrame}")
        print(f"check: {check}  %")
        print("\n")

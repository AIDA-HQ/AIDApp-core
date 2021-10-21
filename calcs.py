import numpy as np
from scipy.stats import linregress


class Calculations:
    def get_Γ(self, storey_masses, eigenvalues):
        global m_tot
        global φ
        global Mφ
        global φTMτ
        global φTMφ
        global m_matrix
        global Γ

        m_matrix = np.diagflat(
            storey_masses
        )  # Storey masses displayed in a diagonal matrix
        m_tot = sum(storey_masses)  # Sum all storey masses together
        φ = np.array(eigenvalues)  # Eigenvalues displayed in a 1-coloumn matrix
        Mφ = np.matmul(m_matrix, φ)
        φTMτ = np.matmul(φ, storey_masses)
        φTMφ = np.matmul(φ, Mφ)
        Γ = φTMτ / φTMφ
        return Γ

    def get_m_matrix(self):
        return m_matrix

    def get_m_tot(self):
        return m_tot

    def get_φ(self):
        return φ

    def get_Mφ(self):
        return Mφ

    def get_φTMτ(self):
        return φTMτ

    def get_φTMφ(self):
        return φTMφ

    def get_K1(self, a, b):
        k1 = linregress(a, b)[0]  # kN
        return k1  # Slope

    def get_Vy_kN(self, K1, dy):
        Vy_kN = K1 * dy  # kN
        return Vy_kN

    def get_me(self):
        global me
        me = m_tot / Γ
        return me

    def get_Vy_F_ms2(self, Vy_kN):
        Vy_F_ms2 = Vy_kN / me  # [m/s^2]
        return Vy_F_ms2

    def get_de(self, ADRS_spectrum, K1_eff_curve):
        # X coords of K1eff intercepting ADRS spectrum
        intersection_ADRS_K1 = ADRS_spectrum.intersection(K1_eff_curve)
        de = float(intersection_ADRS_K1.x)  # [m]
        return de

    def get_ξ1eff(self, dp, ADRS_spectrum, K1_eff_curve):
        de = self.get_de(ADRS_spectrum, K1_eff_curve)
        ξ1eff = 10 * (de / dp) ** 2 - 10
        return ξ1eff

    def get_ξFrame(self, Kf, dp, dy, Vy_kN, Vp_ms2):
        dyF = dy  # [m]
        Vy_F_ms2 = self.get_Vy_F_ms2(Vy_kN)
        VpF_ms2 = Vp_ms2  # [m/s^2]

        ξFrame = (Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp)
        return ξFrame


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
        area_tot,
        a1,
        a2,
        area_diff,
    ):
        values = Calculations()
        print("Storey masses Matrix:\n", values.get_m_matrix(), "\n")
        print("Eigenvalues Matrix:\n", values.get_φ(), "\n")
        print("Modal pattern:\n", values.get_Mφ())
        print("\nφTMτ:", values.get_φTMτ())
        print("φTMφ:", values.get_φTMφ())
        print("Γ: ", Γ)
        print("Vp_kn:", Vp_kN)
        Kf = float(input("Enter the value of K(F): "))
        print("k(F): ", Kf)
        """
        print("Vy(F): ", Vy_F_ms2, "m/s^2")
        print("dp(F): ", dp, "m")
        print("Vp(F): ", VpF_ms2, "m/s^2")
        print("de: ", de, "m")
        print("\nξ1eff: ", ξ1eff, "%")
        """
        print("ξFrame: ", values.get_ξFrame(Kf, dp, dy, Vy_kN, Vp_ms2), "%")
        # print("Check:", check * 100, "%")
        print(
            "\nIntersection(s) between First line of bilinear and SDOF Pushover Curve:",
            intersection_bilinear1_psdof_coords,
        )
        print(
            "Intersection(s) between Second line of bilinear and SDOF Pushover Curve:",
            intersection_bilinear2_psdof_coords,
        )
        print("Intersection of the two lines of the bilinear:", intersection_dy_coords)
        print("Total Area under pushover curve:", area_tot)

        print("dy:", dy)
        print("A1 =", a1)
        print("A2 =", a2)
        print("A1-A2:", area_diff)
        print("%:", area_diff / a1)

import numpy as np


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

    def get_me(self):
        me = m_tot / Γ
        return me

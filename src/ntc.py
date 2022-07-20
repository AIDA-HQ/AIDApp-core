from numpy import arange, around, array, log, log10, pi


class Ntc:
    def __init__(
        self,
        limit_state,
        V_N,
        C_U,
        soil_class,
        topographic_category,
        ag_input,
        fo_input,
        tc_input,
        xi,  # damping coefficient
    ):
        self.limit_state = limit_state
        self.V_N = V_N
        self.soil_class = soil_class
        self.topographic_category = topographic_category
        self.ag_input = ag_input
        self.fo_input = fo_input
        self.tc_input = tc_input
        self.xi = xi
        match C_U:
            case "I":
                self.C_U = 0.7
            case "II":
                self.C_U = 1
            case "III":
                self.C_U = 1.5
            case "IV":
                self.C_U = 2

    def get_V_R(self):
        """Calculate the value of Vr of a building"""
        if (self.V_N * self.C_U) >= 35:
            self.V_R = self.V_N * self.C_U
            return self.V_R
        self.V_R = 35
        return self.V_R

    def get_T_R_SLO(self):
        if (-self.V_R) / log(1 - 0.81) <= 30:
            t_R_SLO = 30
        else:
            if (-self.V_R) / log(1 - 0.81) <= 2475:
                t_R_SLO = around((-self.V_R) / log(1 - 0.81), 0)
            else:
                t_R_SLO = 2475
        return t_R_SLO

    def get_T_R_SLD(self):
        if (-self.V_R) / log(1 - 0.63) <= 30:
            t_R_SLD = 30
        else:
            if (-self.V_R) / log(1 - 0.63) <= 2475:
                t_R_SLD = around((-self.V_R) / log(1 - 0.63), 0)
            else:
                t_R_SLD = 2475
        return t_R_SLD

    def get_T_R_SLV(self):
        if (-self.V_R) / log(1 - 0.10) <= 30:
            t_R_SLV = 30
        else:
            if (-self.V_R) / log(1 - 0.10) <= 2475:
                t_R_SLV = around((-self.V_R) / log(1 - 0.10), 0)
            else:
                t_R_SLV = 2475
        return t_R_SLV

    def get_T_R_SLC(self):
        if (-self.V_R) / log(1 - 0.05) <= 30:
            t_R_SLC = 30
        else:
            if (-self.V_R) / log(1 - 0.05) <= 2475:
                t_R_SLC = around((-self.V_R) / log(1 - 0.05), 0)
            else:
                t_R_SLC = 2475
        return t_R_SLC

    def get_return_times(self):
        self.get_V_R()

        match self.limit_state:
            case "SLO":
                self.t_R = self.get_T_R_SLO()
                return self.t_R
            case "SLD":
                self.t_R = self.get_T_R_SLD()
                return self.t_R
            case "SLV":
                self.t_R = self.get_T_R_SLV()
                return self.t_R
            case "SLC":
                self.t_R = self.get_T_R_SLC()
                return self.t_R

    def get_zonation_value_dict(self, v_tuple):
        """
        Returns a dictionary with the t_R [years] as keys
        and the seismic zonationparameters as values.
        """
        self.get_return_times()

        v_30, v_50, v_72, v_101, v_140, v_201, v_475, v_975, v_2475 = v_tuple

        tR_30 = 30
        tR_50 = 50
        tR_72 = 72
        tR_101 = 101
        tR_140 = 140
        tR_201 = 201
        tR_475 = 475
        tR_975 = 975
        tR_2475 = 2475
        t_R = 30
        zonation_value_dict = {30: v_30}

        while t_R < 50:
            v = 10 ** (
                log10(v_30)
                + (log10(v_50 / v_30)) * log10((t_R + 1) / tR_30) / log10(tR_50 / tR_30)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 50
        while t_R < 72:
            v = 10 ** (
                log10(v_50)
                + (log10(v_72 / v_50)) * log10((t_R + 1) / tR_50) / log10(tR_72 / tR_50)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 72
        while t_R < 101:
            v = 10 ** (
                log10(v_72)
                + (log10(v_101 / v_72))
                * log10((t_R + 1) / tR_72)
                / log10(tR_101 / tR_72)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 101
        while t_R < 140:
            v = 10 ** (
                log10(v_101)
                + (log10(v_140 / v_101))
                * log10((t_R + 1) / tR_101)
                / log10(tR_140 / tR_101)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 140
        while t_R < 201:
            v = 10 ** (
                log10(v_140)
                + (log10(v_201 / v_140))
                * log10((t_R + 1) / tR_140)
                / log10(tR_201 / tR_140)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 201
        while t_R < 475:
            v = 10 ** (
                log10(v_201)
                + (log10(v_475 / v_201))
                * log10((t_R + 1) / tR_201)
                / log10(tR_475 / tR_201)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 475
        while t_R < 975:
            v = 10 ** (
                log10(v_475)
                + (log10(v_975 / v_475))
                * log10((t_R + 1) / tR_475)
                / log10(tR_975 / tR_475)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)
        t_R = 975
        while t_R < 2475:
            v = 10 ** (
                log10(v_975)
                + (log10(v_2475 / v_975))
                * log10((t_R + 1) / tR_975)
                / log10(tR_2475 / tR_975)
            )
            t_R = t_R + 1
            key = t_R
            zonation_value_dict[key] = round(v, 15)

        return zonation_value_dict

    @staticmethod
    def get_zonation_value_array(zonation_value_dict):
        """Returns an array with the seismic zonation parameters as values."""
        zonation_array = []
        for key in zonation_value_dict:
            zonation_array.append(zonation_value_dict[key])
        return array(zonation_array)

    def get_basic_seismic_danger_value(self, zonation_value_dict):
        """Checks if t_R is a zonation_value_dict key and returns the corresponding value."""
        if self.t_R in zonation_value_dict:
            return zonation_value_dict[self.t_R]
        return None

    def get_values(self):

        ag_dict = self.get_zonation_value_dict(self.ag_input)
        self.ag_value = self.get_basic_seismic_danger_value(ag_dict)
        fo_dict = self.get_zonation_value_dict(self.fo_input)
        self.fo_value = self.get_basic_seismic_danger_value(fo_dict)
        tc_dict = self.get_zonation_value_dict(self.tc_input)
        self.tc_value = self.get_basic_seismic_danger_value(tc_dict)

    def get_ss_calc(self):
        """Returns the ss_calc value."""
        self.get_values()
        match self.soil_class:
            case "A":
                self.ss_calc = 1
                return self.ss_calc
            case "B":
                self.ss_calc = 1.4 - 0.4 * (self.fo_value * self.ag_value)
                return self.ss_calc
            case "C":
                self.ss_calc = 1.7 - 0.6 * (self.fo_value * self.ag_value)
                return self.ss_calc
            case "D":
                self.ss_calc = 2.5 - 1.5 * (self.fo_value * self.ag_value)
                return self.ss_calc
            case "E":
                self.ss_calc = 2 - 1.1 * (self.fo_value * self.ag_value)
                return self.ss_calc

    def get_ss_min(self):
        match self.soil_class:
            case "A":
                self.ss_min = 1
                return self.ss_min
            case "B":
                self.ss_min = 1
                return self.ss_min
            case "C":
                self.ss_min = 1
                return self.ss_min
            case "D":
                self.ss_min = 0.9
                return self.ss_min
            case "E":
                self.ss_min = 1
                return self.ss_min

    def get_ss_max(self):
        match self.soil_class:
            case "A":
                self.ss_max = 1
                return self.ss_max
            case "B":
                self.ss_max = 1.2
                return self.ss_max
            case "C":
                self.ss_max = 1.5
                return self.ss_max
            case "D":
                self.ss_max = 1.8
                return self.ss_max
            case "E":
                self.ss_max = 1.6
                return self.ss_max

    def get_ss(self):
        self.get_ss_calc()
        self.get_ss_min()
        self.get_ss_max()
        if self.ss_calc <= self.ss_min:
            self.ss = self.ss_min
        if self.ss_calc >= self.ss_max:
            self.ss = self.ss_max
        else:
            self.ss = self.ss_calc
        return self.ss

    def get_st(self):
        match self.topographic_category:
            case "T1":
                self.st = 1
                return self.st
            case "T2":
                self.st = 1.2
                return self.st
            case "T3":
                self.st = 1.2
                return self.st
            case "T4":
                self.st = 1.4
                return self.st

    def get_s(self):
        self.get_ss_min()
        self.get_ss_max()

        self.get_ss()
        self.get_st()
        self.s = self.ss * self.st
        return self.s

    def get_eta(self):
        self.eta = max([(10 / (5 + self.xi)) ** 0.5, 0.55])
        return self.eta

    def get_c_c(self):
        match self.soil_class:
            case "A":
                self.c_c = 1
                return self.c_c
            case "B":
                self.c_c = 1.1 * ((self.tc_value ** (-0.2)))
                return self.c_c
            case "C":
                self.c_c = 1.05 * ((self.tc_value ** (-0.33)))
                return self.c_c
            case "D":
                self.c_c = 1.25 * ((self.tc_value ** (-0.5)))
                return self.c_c
            case "E":
                self.c_c = 1.15 * ((self.tc_value ** (-0.4)))
                return self.c_c

    def get_t_c(self):
        """t_C is T_C* from the basic seismic danger table."""
        self.get_c_c()
        self.t_c = self.tc_value * self.c_c
        return self.t_c

    def get_t_b(self):
        self.get_t_c()
        self.t_b = self.t_c / 3
        return self.t_b

    def get_t_d(self):
        self.t_d = 4 * self.ag_value + 1.6
        return self.t_d

    def get_acceleration_curve_T(self):
        self.get_s()
        self.get_t_b()
        self.get_t_c()
        self.get_t_d()
        self.t_acceleration_coords = []
        arange_array = arange(0.00, 1, 0.05)
        # Calculate the ones until T_B line
        for value in arange_array:
            coord = value * self.t_b
            self.t_acceleration_coords.append(coord)

        # Calculate the ones until T_C line
        for value in arange_array:
            coord = self.t_b + (self.t_c - self.t_b) * value
            self.t_acceleration_coords.append(coord)

        # Calculate the ones until T_D line
        for value in arange_array:
            coord = self.t_c + (self.t_d - self.t_c) * value
            self.t_acceleration_coords.append(coord)

        # Calculate the ones until the end line
        for value in arange_array:
            coord = self.t_d + (4 - self.t_d) * value
            self.t_acceleration_coords.append(coord)
        self.t_acceleration_coords.append(float(4))

        return self.t_acceleration_coords

    def get_acceleration_curve_Se(self):
        t_acceleration_coords = self.get_acceleration_curve_T()
        self.get_eta()
        self.Se_coords = []

        # Calculate the ones until T_B line
        for element in t_acceleration_coords[:21]:
            coord = (
                self.ag_value
                * self.s
                * self.eta
                * self.fo_value
                * (
                    element / self.t_b
                    + (1 / (self.eta * self.fo_value)) * (1 - element / self.t_b)
                )
            )
            self.Se_coords.append(coord)

        # Calculate the ones until T_C line
        for _ in range(20):
            coord = self.ag_value * self.s * self.eta * self.fo_value
            self.Se_coords.append(coord)

        # Calculate the ones until T_D line
        for element in t_acceleration_coords[41:62]:
            coord = (
                self.ag_value * self.s * self.eta * self.fo_value * (self.t_c / element)
            )
            self.Se_coords.append(coord)

        # Calculate the ones until the end line
        for element in t_acceleration_coords[62:]:
            coord = (
                self.ag_value
                * self.s
                * self.eta
                * self.fo_value
                * (self.t_c * self.t_d / element**2)
            )
            self.Se_coords.append(coord)

        return array(self.Se_coords)

    def get_movement_curve_SDe(self):
        self.get_acceleration_curve_T()
        self.get_acceleration_curve_Se()
        self.SDe_coords_movement = []

        for s, g in zip(self.t_acceleration_coords, self.Se_coords):
            coord = g * 9.806 * (s / (2 * pi)) ** 2
            self.SDe_coords_movement.append(coord)
        return array(self.SDe_coords_movement)

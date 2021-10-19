from matplotlib import lines
import numpy as np
from numpy import trapz
from scipy.stats import linregress

import matplotlib.pyplot as plt
from shapely.geometry.linestring import LineString
from shapely.geometry import Polygon
from coord import Coords
from calcs import Calculations

coord = Coords()
values = Calculations()

# Store data from user input
number_storeys = int(input("Enter the number of storeys: "))
storey_masses = []
eigenvalues = []

i = 0
while i < number_storeys:
    i = i + 1
    storey_masses.append(float(input("Enter the mass of storey #" + str(i) + ": ")))
print("\n")
n = 0
while n < number_storeys:
    n = n + 1
    eigenvalues.append(float(input("Enter the eigenvalues #" + str(n) + ": ")))
print("\n")


Γ = values.get_Γ(storey_masses, eigenvalues)
me = values.get_me()  # [ton]
y_p_sdof = coord.y_p_sdof(Γ)
x_p_sdof = coord.x_p_sdof(Γ)

print("Storey masses Matrix:\n", values.get_m_matrix(), "\n")
print("Eigenvalues Matrix:\n", values.get_φ(), "\n")
print("Modal pattern:\n", values.get_Mφ())
print("\nφTMτ: ", values.get_φTMτ())
print("φTMφ: ", values.get_φTMφ())
print("Γ: ", Γ)


# 3rd x coordinate of bilinear curve
dp = float(input("\nEnter the value of d*p [m]: "))

Vp_kN = y_p_sdof[coord.find_nearest_coordinate_index(x_p_sdof, dp)]
print("Vp_kn:", Vp_kN)
Vp_ms2 = Vp_kN / me  # ms2

# TODO automatically calculate k1
# Slope of first 5 values of SDOF Pushover Curve
a = [x_p_sdof[2:10]]
b = [y_p_sdof[2:10]]
K1 = linregress(a, b)[0]  # kN

dy = float(input("\nEnter the selected value of dy [m]: "))
Vy_kN = K1 * dy  # kN

# X coordinates of the bilinear curve
x_bilinear = np.array([0, dy, dp])

# Y coords of the bilinear curve in [kN]
y_bilinear_kN = np.array([0, Vy_kN, Vp_kN])

# Y coords of the bilinear curve in [m/s^2]
y_bilinear_ms2 = np.array(
    [y_bilinear_kN[0] / me, y_bilinear_kN[1] / me, y_bilinear_kN[2] / me]
)


#
# Graphs
ADRS_meters_curve = plt.plot(
    coord.x_ADRS_meters, coord.y_ADRS_meters, label="ADRS meters curve"
)

K1_eff_curve = plt.plot(coord.x_K1_eff, coord.y_K1_eff, label="K1 eff curve")
# p_mdof_curve = plt.plot(coord.x_p_mdof, coord.y_p_mdof, label="MDOF Pushover Curve")
bilinear_ms2_curve = plt.plot(
    x_bilinear, y_bilinear_ms2, label="Bilinear curve in m/s^2"
)
p_sdof_curve = plt.plot(x_p_sdof, y_p_sdof, label="SDOF Pushover Curve")

ADRS_spectrum = LineString(np.column_stack((coord.x_ADRS_meters, coord.y_ADRS_meters)))
K1_eff_curve = LineString(np.column_stack((coord.x_K1_eff, coord.y_K1_eff)))
p_sdof = LineString(np.column_stack((x_p_sdof, y_p_sdof)))

intersection_ADRS_K1 = ADRS_spectrum.intersection(K1_eff_curve)

# TODO switch from kN bilinear to the ms2 one
# Straight line passing through 1st and 2nd point of bilinear curve
m_bilinear_line_1, q_bilinear_line_1 = np.polyfit(
    x=[x_bilinear[0], x_bilinear[1]], y=[y_bilinear_kN[0], y_bilinear_kN[1]], deg=1
)

x_bilinear_line_1 = coord.x_bilinear_line(x_p_sdof[0], x_p_sdof[-1])
y_bilinear_line_1 = m_bilinear_line_1 * x_bilinear_line_1 + q_bilinear_line_1
print("y bilinear 1:", m_bilinear_line_1, q_bilinear_line_1)
plt.plot(
    x_bilinear_line_1, y_bilinear_line_1, "-r", label="1st line of the bilinear curve"
)

bilinear_line_1 = LineString(np.column_stack((x_bilinear_line_1, y_bilinear_line_1)))

# Intersections

intersection_bilinear1_psdof = p_sdof.intersection(bilinear_line_1)
intersection_bilinear1_psdof_coords = coord.plot_intersections(
    intersection_bilinear1_psdof
)
intersection_bilinear1_psdof_coords

# Straight line passing through 2nd and 3rd point of the bilinear curve
m_bilinear_line_2, q_bilinear_line_2 = np.polyfit(
    x=[x_bilinear[1], x_bilinear[2]], y=[y_bilinear_kN[1], y_bilinear_kN[2]], deg=1
)

x_bilinear_line_2 = np.linspace(x_p_sdof[0], x_p_sdof[-1], 1000)
y_bilinear_line_2 = m_bilinear_line_2 * x_bilinear_line_2 + q_bilinear_line_2
print("y bilinear 2:", m_bilinear_line_2, q_bilinear_line_2)

plt.plot(
    x_bilinear_line_2, y_bilinear_line_2, "-r", label="2nd line of the bilinear curve"
)

bilinear_line_2 = LineString(np.column_stack((x_bilinear_line_2, y_bilinear_line_2)))


intersection_bilinear2_psdof = p_sdof.intersection(bilinear_line_2)
intersection_bilinear2_psdof_coords = coord.plot_intersections(
    intersection_bilinear2_psdof
)
intersection_bilinear2_psdof_coords

# Intersection of the two straight lines
intersection_dy = bilinear_line_1.intersection(bilinear_line_2)
intersection_dy_coords = coord.plot_intersections(intersection_dy)
intersection_dy_coords

print("\n")
print(
    "Intersection(s) between First line of bilinear and SDOF Pushover Curve:",
    intersection_bilinear1_psdof_coords,
)
print(
    "Intersection(s) between Second line of bilinear and SDOF Pushover Curve:",
    intersection_bilinear2_psdof_coords,
)
print("Intersection of the two lines of the bilinear:", intersection_dy_coords)

#####

# X coords of K1eff intercepting ADRS spectrum
de = float(intersection_ADRS_K1.x)  # [m]

dyF = dy  # [m]
Vy_F_ms2 = Vy_kN / me  # [m/s^2]
VpF_ms2 = Vp_ms2  # [m/s^2]

Kf = float(input("Enter the value of K(F): "))
ξ1eff = 10 * (de / dp) ** 2 - 10

ξFrame = (Kf * 63.7 * (Vy_F_ms2 * dp - VpF_ms2 * dyF)) / (VpF_ms2 * dp)
check = (np.abs(ξ1eff - ξFrame)) / ξFrame

print("\ndyF: ", dyF, "m")
print("k(F): ", Kf)
print("Vy(F): ", Vy_F_ms2, "m/s^2")
print("dp(F): ", dp, "m")
print("Vp(F): ", VpF_ms2, "m/s^2")
print("de: ", de, "m")

print("\nξ1eff: ", ξ1eff, "%")
print("ξFrame: ", ξFrame, "%")
print("Check:", check * 100, "%")

plt.legend()
plt.show()


# Calculate A1 and A2

difference_array_x_0 = np.absolute(x_p_sdof - intersection_bilinear1_psdof_coords[1][0])
# find the index of minimum element from the array
index_x_0 = difference_array_x_0.argmin()
print("Nearest element to the given values is : ", x_p_sdof[index_x_0])
print("Index of nearest value is : ", index_x_0)

difference_array_x_1 = np.absolute(x_p_sdof - intersection_bilinear2_psdof_coords[0][0])
# find the index of minimum element from the array
index_x_1 = difference_array_x_1.argmin()
print("Nearest element to the given values is : ", x_p_sdof[index_x_1])
print("Index of nearest value is : ", index_x_1)
list_fitting_x = [x_p_sdof[index_x_0 : index_x_1 + 1]]


difference_array_y_0 = np.absolute(y_p_sdof - intersection_bilinear1_psdof_coords[1][1])
# find the index of minimum element from the array
index_y_0 = difference_array_y_0.argmin()
print("Nearest element to the given values is : ", y_p_sdof[index_y_0])
print("Index of nearest value is : ", index_y_0)

difference_array_y_1 = np.absolute(y_p_sdof - intersection_bilinear2_psdof_coords[0][1])
# find the index of minimum element from the array
index_y_1 = difference_array_y_1.argmin()
print("Nearest element to the given values is : ", y_p_sdof[index_y_1])
print("Index of nearest value is : ", index_y_1)
list_fitting_y = [y_p_sdof[index_y_0 : index_y_1 + 1]]


difference_array_x_1_b = np.absolute(
    x_p_sdof - intersection_bilinear2_psdof_coords[1][0]
)
# find the index of minimum element from the array
index_x_1_b = difference_array_x_1_b.argmin()
print("Nearest element to the given values is : ", x_p_sdof[index_x_1])
print("Index of nearest value is : ", index_x_1)
list_fitting_x_b = [x_p_sdof[index_x_1 : index_x_1_b + 1]]

difference_array_y_1_b = np.absolute(
    y_p_sdof - intersection_bilinear2_psdof_coords[1][1]
)
# find the index of minimum element from the array
index_y_1_b = difference_array_y_1_b.argmin()
print("Nearest element to the given values is : ", y_p_sdof[index_y_1])
print("Index of nearest value is : ", index_y_1)
list_fitting_y_b = [y_p_sdof[index_y_1 : index_y_1_b + 1]]

# Compute the area using the composite trapezoidal rule.
y = np.array(
    [
        intersection_bilinear1_psdof_coords[1][1],
        Vy_kN,
        intersection_bilinear2_psdof_coords[0][1],
    ]
)
x = np.array(
    [
        intersection_bilinear1_psdof_coords[1][0],
        dy,
        intersection_bilinear2_psdof_coords[0][0],
    ]
)

z = np.array(
    [
        intersection_bilinear2_psdof_coords[0][1],
        intersection_bilinear2_psdof_coords[1][1],
    ]
)
k = np.array(
    [
        intersection_bilinear2_psdof_coords[0][0],
        intersection_bilinear2_psdof_coords[1][0],
    ]
)
area_tot = trapz(y_p_sdof, x_p_sdof)
area_1 = trapz(np.array(list_fitting_y), np.array(list_fitting_x))
area_2 = trapz(np.array(list_fitting_y_b), np.array(list_fitting_x_b))

print("Total Area:", area_tot)
print("Area under pushover:", area_1)
print("Area under bilinear:", trapz(y, x))
print("A1 =", np.absolute(area_1 - trapz(y, x)))
print("A2 =", np.absolute(area_2 - trapz(z, k)))

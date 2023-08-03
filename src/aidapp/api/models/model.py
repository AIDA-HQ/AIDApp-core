from pydantic import BaseModel
from typing import List


class InputValues(BaseModel):
    dp: float
    mu_DB: float
    k_DB: float
    kf: float
    storey_masses: List[float]
    eigenvalues: List[float]
    brace_number: List[int]
    zonation_0: List[float]
    zonation_1: List[float]
    zonation_2: List[float]
    pushover_x: List[float]
    pushover_y: List[float]
    span_length: float
    interfloor_height: float
    nominal_age: int
    functional_class: str
    topographic_factor: str
    soil_class: str
    limit_state: str
    damping_coeff: float


# class OutputValues(BaseModel):
#     TODO
#     kc_n_s_array : List[float]
#     Fc_n_s_array : List[float]
#     i : int
#     de_0 : float
#     de_n : float
#     dp : float

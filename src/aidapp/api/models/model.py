from pydantic import BaseModel
from typing import List


class InputValues(BaseModel):
    dp: float
    mu_DB: float
    k_DB: float
    Kf: float
    storey_masses: List[float]
    eigenvalues: List[float]
    brace_number: List[int]
    path_zonation: List[str]
    pushover_x: str
    pushover_y: str
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

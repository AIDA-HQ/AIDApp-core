from typing import List

from pydantic import BaseModel


class InputValues(BaseModel):
    """Input value model for the AIDAPP calculate endpoint."""

    dp: float
    mu_DB: float
    k_DB: float
    kf: float
    storey_masses: List[float]
    eigenvalues: List[float]
    zonation_ag: List[float]
    zonation_fo: List[float]
    zonation_tc: List[float]
    pushover_x: List[float]
    pushover_y: List[float]
    nominal_age: int
    functional_class: str
    topographic_factor: str
    soil_class: str
    limit_state: str
    damping_coeff: float


class OutputValues(BaseModel):
    """Output value model for the AIDAPP calculate endpoint."""

    i: int
    x_bilinear: List[float]
    y_bilinear_ms2: List[float]
    sd_meters: List[float]
    sa_ms2: List[float]
    kn_eff_list: List[float]
    y_bilinear_ms2_0: List[float]
    kn_eff_list_0: List[float]
    de_0: List[float]
    de_n: List[float]
    dp: float

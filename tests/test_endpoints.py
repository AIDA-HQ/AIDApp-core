import json

import pytest
from fastapi.testclient import TestClient

from aidapp.api import main
from aidapp.api.schemas.schema import InputValues

client = TestClient(main.app)


def test_calculate_endpoint_valid_input():
    """Test the /calculate/ endpoint with valid input."""
    with open("tests/test_payload.json") as f:
        payload = json.load(f)
    response = client.post("/calculate/", json=payload)
    assert response.status_code == 200

    assert response.json()["i"] == 5
    assert response.json()["de_0"] == [0.148465762254, 4.838711036209]
    assert response.json()["de_n"] == [0.092350797764, 7.807520454074]
    assert response.json()["dp"] == 0.044429959868


def test_calculate_endpoint_invalid_input():
    """Test the /calculate/ endpoint with invalid input."""
    with pytest.raises(ValueError):
        input_values = InputValues(
            dp=0.1,
            mu_DB=6,
            k_DB=1,
            kf=0.66,
            storey_masses=[
                239.6789,
                231.4220183,
            ],
            eigenvalues=[0.113530691, 0.326058618],
            brace_number=[2, 2],
            zonation_0=[0.1, "invalid"],
            zonation_1=[0.1, 0.2],
            zonation_2=[0.1, 0.2],
            pushover_x=[0, 0.0015, 0.003, 0.0045],
            pushover_y=[0, 55.59392236, 109.3670878, 163.8144485],
            span_length=6,
            interfloor_height=3,
            nominal_age=50,
            functional_class="I",
            topographic_factor="T1",
            soil_class="A",
            limit_state="SLV",
            damping_coeff=5,
        )
        client.post("/calculate/", json=input_values.model_dump_json())

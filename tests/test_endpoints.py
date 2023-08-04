import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from aidapp.api import main

client = TestClient(main.app)


def test_calculate():
    with open("tests/test_payload.json") as f:
        payload = json.load(f)
    response = client.post("/calculate/", json=payload)
    assert response.status_code == 200

    assert response.json()["kc_n_s_array"] == [
        896060.0409196536,
        461111.24652382464,
        342785.6925901348,
        331648.53775286616,
        324788.7688801968,
        253737.4026480032,
    ]
    assert response.json()["Fc_n_s_array"] == [
        852.868455309155,
        821.586663019117,
        734.840773590922,
        585.588377513482,
        382.303200328156,
        142.997493643942,
    ]
    assert response.json()["i"] == 5
    assert response.json()["de_0"] == [0.148465762254, 4.838711036209]
    assert response.json()["de_n"] == [0.092350797764, 7.807520454074]
    assert response.json()["dp"] == 0.044429959868

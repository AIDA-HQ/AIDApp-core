from fastapi import APIRouter
from ..models.model import InputValues
from aidapp.main import main

router = APIRouter()


@router.post("/calculate/")
async def calculate(input_values: InputValues):
    print("yeeeet")
    kc_n_s_array, Fc_n_s_array, i, _, _, _, _, _, _, _, de_0, de_n, dp = main(
        input_values
    )
    return {"message": f"{input_values}"}

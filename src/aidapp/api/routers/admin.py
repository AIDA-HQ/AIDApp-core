from fastapi import APIRouter

from aidapp.api.models.model import InputValues, OutputValues
from aidapp.main import main

router = APIRouter()


@router.post("/calculate/", response_model=OutputValues)
async def calculate(input_values: InputValues):
    try:
        aidapp_output = main(input_values)
    except Exception as e:
        return {"message": f"{e}"}
    return aidapp_output._asdict()

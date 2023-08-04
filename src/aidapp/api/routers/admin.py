from fastapi import APIRouter

from aidapp.main import main

from aidapp.api.models.model import InputValues, OutputValues

router = APIRouter()


@router.post("/calculate/", response_model=OutputValues)
async def calculate(input_values: InputValues):
    try:
        aidapp_output = main(input_values)
    except Exception as e:
        return {"message": f"{e}"}
    return aidapp_output._asdict()

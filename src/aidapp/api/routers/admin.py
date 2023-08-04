from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from aidapp.api.models.model import InputValues, OutputValues
from aidapp.main import main

router = APIRouter()


@router.post("/calculate/", response_model=OutputValues)
async def calculate(input_values: InputValues):
    """Endpoint to feed the inputs to the algorithm and return the output values."""
    try:
        aidapp_output = main(input_values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    return JSONResponse(content=aidapp_output._asdict(), status_code=200)

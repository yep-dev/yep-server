from fastapi import APIRouter

router = APIRouter()


@router.post("/actions/calibrate")
async def calibrate():
    return {}


@router.post("/actions/stop")
async def calibrate():
    return {}
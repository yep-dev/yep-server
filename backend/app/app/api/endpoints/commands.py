from app.streams import commands
from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter()


@router.post("/calibrate")
async def calibrate(request: Request):
    redis = request.app.extra["redis"]
    # todo: check if stopped
    redis.xadd(commands.command_all, {"type": commands.calibrate})


@router.post("/stop")
async def stop(request: Request):
    redis = request.app.extra["redis"]
    redis.xadd(commands.command_all, {"type": commands.stop})

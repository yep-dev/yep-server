import time

from fastapi import APIRouter
from starlette.requests import Request

from app.streams import commands

router = APIRouter()


@router.post("/calibrate")
async def calibrate(request: Request):
    redis = request.app.extra["redis"]
    # todo: check if stopped
    redis.xadd(commands.command_all, {"type": commands.calibrate, "time": time.time()})


@router.post("/stop")
async def stop(request: Request):
    redis = request.app.extra["redis"]
    redis.xadd(commands.command_all, {"type": commands.stop, "time": time.time()})

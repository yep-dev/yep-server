import time

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from streams import commands

router = APIRouter()


class RunData(BaseModel):
    type: str


@router.post("/run")
async def run(request: Request, data: RunData):
    redis = request.app.extra["redis"]
    redis.xadd(commands.command_all, {"type": data.type, "time": time.time()})

import json
import time

import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from app.crud.crud_settings import settings_crud
from app.streams import commands

router = APIRouter()


class WaveSpec(BaseModel):
    type: str
    duration: float


def sine(length):
    linespace = np.linspace(-np.pi, np.pi, int(length) + 1)
    return np.sin(linespace)


def square(length):
    # todo: implement wave smoothing based on max motor frequency to avoid overloading it here
    def process_point(point, points_number):
        if points_number / 4 <= point < points_number / 4 * 3:
            return 1
        return -1

    linespace = np.linspace(0, int(length), int(length), endpoint=True)
    return np.array([process_point(i, int(length)) for i in linespace])


def reverse_gradient(gradient, linespace):
    return (
        linespace[0]
        + 2
        * np.c_[
            np.r_[0, gradient[1:-1:2].cumsum()],
            gradient[::2].cumsum() - gradient[0] / 2,
        ].ravel()[: len(gradient)]
    )


async def build_wave(spec, tick_rate):
    types = {"sine": sine, "square": square}
    length = spec.duration * tick_rate
    original_positions = types.get(spec.type, lambda: None)(length)
    min_index = original_positions.argmin()
    positions = np.roll(original_positions[:-1], -min_index)
    return {
        "positions": positions.tolist()[:-1],
    }


@router.post("/get")
async def wave(request: Request, spec: WaveSpec):
    # todo: send flag if wave doesn't start at 0 to block running it
    settings = await settings_crud.get(request)
    data = await build_wave(spec, settings["wave_resolution"])
    return data


@router.post("/run")
async def wave(request: Request, spec: WaveSpec):
    # todo: ensure that each wave ran starts at 0 position
    settings = await settings_crud.get(request)
    data = await build_wave(spec, settings["wave_resolution"])

    redis = request.app.extra["redis"]
    redis.xadd(
        commands.command_all,
        {
            "type": commands.loop_wave,
            "time": time.time(),
            "data": json.dumps([(point + 1) / 2 for point in data["positions"]]),
        },
    )
    return {"status": "success"}

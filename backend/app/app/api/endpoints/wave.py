import json
import time

import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from app.streams import commands

router = APIRouter()

RESOLUTION = 20


class WaveSpec(BaseModel):
    type: str
    duration: float


def sine(duration):
    linespace = np.linspace(-np.pi, np.pi, int(RESOLUTION * duration) + 1)
    return np.sin(linespace)


def square(duration):
    # todo: implement wave smoothing based on max motor frequency to avoid overloading it here
    def process_point(point, points_number):
        if points_number / 4 <= point < points_number / 4 * 3:
            return 1
        return -1

    linespace = np.linspace(
        0, int(RESOLUTION * duration), int(RESOLUTION * duration), endpoint=True
    )
    return np.array([process_point(i, int(RESOLUTION * duration)) for i in linespace])


def reverse_gradient(gradient, linespace):
    return (
            linespace[0]
            + 2
            * np.c_[
                  np.r_[0, gradient[1:-1:2].cumsum()],
                  gradient[::2].cumsum() - gradient[0] / 2,
              ].ravel()[: len(gradient)]
    )


async def build_wave(spec):
    types = {"sine": sine, "square": square}
    original_positions = types.get(spec.type, lambda: None)(spec.duration)
    min_index = original_positions.argmin()
    original_positions = np.roll(original_positions[:-1], -min_index)
    movements = np.gradient(original_positions)
    # process movements here

    processed_positions = reverse_gradient(movements, original_positions)

    return {
        "originalPositions": original_positions.tolist()[:-1],
        "processedPositions": processed_positions.tolist()[:-1],
        "movements": movements.tolist()[:-1],
    }


@router.post("/get")
async def wave(request: Request, spec: WaveSpec):
    # todo: send flag if wave doesn't start at 0 to block running it
    data = await build_wave(spec)
    return data


@router.post("/run")
async def wave(request: Request, spec: WaveSpec):
    # todo: ensure that each wave ran starts at 0 position
    data = await build_wave(spec)

    redis = request.app.extra["redis"]
    redis.xadd(
        commands.command_all,
        {"type": commands.loop_wave, "time": time.time(),
         "data": json.dumps(data["movements"])},
    )
    return {"status": "success"}

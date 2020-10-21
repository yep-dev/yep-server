import json

from app.streams import commands
from fastapi import APIRouter
from pydantic import BaseModel

import numpy as np
from scipy import signal
from starlette.requests import Request

router = APIRouter()


class WaveSpec(BaseModel):
    type: str


def sine():
    linespace = np.linspace(-np.pi, np.pi, 51)
    return np.sin(linespace)


def square():
    linespace = np.linspace(0, 10, 51, endpoint=True)
    return signal.square(500 * linespace)


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
    original_positions = types.get(spec.type, lambda: None)()
    movements = np.gradient(original_positions)
    # process movements here

    processed_positions = reverse_gradient(movements, original_positions)

    return {
        "originalPositions": original_positions.tolist()[:-1],
        "processedPositions": processed_positions.tolist()[:-1],
        "movements": movements.tolist()[:-1],
    }


@router.post('/get')
async def wave(request: Request, spec: WaveSpec):
    data = await build_wave(spec)
    return data


@router.post("/run")
async def wave(request: Request, spec: WaveSpec):
    data = await build_wave(spec)

    redis = request.app.extra["redis"]
    redis.xadd(
        commands.command_all,
        {"type": commands.loop_wave, "data": json.dumps(data['movements'])},
    )
    return {'status': 'success'}

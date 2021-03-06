from typing import Any

import numpy as np
from fastapi import APIRouter
from pydantic import BaseModel
from scipy.interpolate import make_interp_spline

router = APIRouter()


class Data(BaseModel):
    points: Any
    resolution: int = 100

@router.post("/")
def post_settings_curve(
    *,
    data: Data,
) -> Any:
    data.points.append(0)
    x = [x * data.resolution / 10 for x in range(11)]
    xnew = np.linspace(0, data.resolution, data.resolution)
    spline = make_interp_spline(np.array(x), np.array(data.points), k=2)
    y_smooth = spline(xnew)
    return y_smooth.tolist()

from typing import Any

from fastapi import APIRouter
from scipy.interpolate import make_interp_spline

import numpy as np

router = APIRouter()

from pydantic import BaseModel


class Data(BaseModel):
    data: Any


@router.post("/")
def post_settings_curve(
    *,
    data: Data,
) -> Any:
    print(data)
    x = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    xnew = np.linspace(0, 1000, 1000)
    spline = make_interp_spline(np.array(x), np.array(data.data), k=2)
    y_smooth = spline(xnew)
    return y_smooth.tolist()

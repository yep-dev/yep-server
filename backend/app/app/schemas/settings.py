from typing import Optional

from pydantic import BaseModel


class ThrustSettingsEdit(BaseModel):
    name: Optional[str]
    microsteps_per_rev: Optional[int]
    wave_resolution: Optional[int]

    stroke_limit: Optional[int]
    max_stroke: Optional[int]
    padding_mm: Optional[int]
    max_steps: Optional[int]


class ThrustSettings(ThrustSettingsEdit):
    id: str
    stroke_limit: int
    max_stroke: int
    padding_mm: int

    # calibration
    max_steps: Optional[int]


class ThrustSettingsDisplay(ThrustSettings):
    steps_per_mm: Optional[float]

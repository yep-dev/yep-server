from typing import List, Optional

from pydantic import BaseModel


class ThrustSettingsEdit(BaseModel):
    name: Optional[str]
    active: Optional[bool]

    # Force response
    tick_stroke_limit: Optional[int]
    force_limit: Optional[int]
    stroke_force_chart: Optional[List[int]]

    # Stepper motor
    microsteps_per_rev: Optional[int]
    wave_resolution: Optional[int]  # todo: rename to tick_rate

    # Thrust
    stroke_limit: Optional[int]
    max_stroke: Optional[int]
    padding_mm: Optional[int]

    # Calibration
    max_steps: Optional[int]


class ThrustSettings(ThrustSettingsEdit):
    id: str
    stroke_limit: int
    max_stroke: int
    padding_mm: int
    stroke_force_chart: List[int]

    # calibration
    max_steps: Optional[int]


class ThrustSettingsDisplay(ThrustSettings):
    steps_per_mm: Optional[float]

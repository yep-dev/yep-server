from typing import Optional

from pydantic import BaseModel


class StepperSettings(BaseModel):
    name: str

    microsteps_per_rev: int
    wave_resolution: int


class MachineThrustSettingsEdit(StepperSettings):
    name: Optional[str]
    microsteps_per_rev: Optional[int]
    wave_resolution: Optional[int]

    stroke_length: Optional[int]
    stroke_limit: Optional[int]
    padding_steps: Optional[int]
    max_steps: Optional[int]


class MachineThrustSettingsDisplay(MachineThrustSettingsEdit):
    id: str
    stroke_length: int
    stroke_limit: int
    padding_steps: int
    max_steps: Optional[int]

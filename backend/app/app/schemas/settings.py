from typing import Optional

from pydantic import BaseModel


class StepperSettings(BaseModel):
    name: str

    microsteps_per_rev: int
    wave_resolution: int


class MachineThrustSettingsEdit(StepperSettings):
    stroke_length: int
    stroke_limit: int
    padding_steps: int


class MachineThrustSettingsDisplay(MachineThrustSettingsEdit):
    id: str
    max_steps: Optional[int]

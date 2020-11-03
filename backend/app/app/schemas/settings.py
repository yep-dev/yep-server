from typing import Optional

from pydantic import BaseModel


class StepperSettings(BaseModel):
    name: str

    microsteps_per_rev: int
    wave_resolution: int


class MachineThrustUiSettings(StepperSettings):
    stroke_length: int
    stroke_limit: int
    padding_steps: int

    max_steps: Optional[int]


class MachineThrustCalibrationSettings(BaseModel):
    max_steps: int


class MachineThrustSettings(MachineThrustUiSettings, MachineThrustCalibrationSettings):
    class Config:
        orm_mode = True

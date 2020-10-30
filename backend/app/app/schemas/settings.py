from typing import Optional

from pydantic import BaseModel


class StepperSettings(BaseModel):
    name: str

    microsteps_per_rev: int
    wave_resolution: int


class MachineThrustSettings(StepperSettings):
    stroke_length: int
    stroke_limit: int
    padding_steps: int

    max_steps: Optional[int]

    class Config:
        orm_mode = True

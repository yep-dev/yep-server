from sqlalchemy import Column, Integer, String

from app.db.base_class import Base

# class StepperSettings(Base):
#     pulses_per_rev = Column(Integer)
#     wave_resolution = Column(Integer)


class MachineThrustSettings(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    microsteps_per_rev = Column(Integer)
    wave_resolution = Column(Integer)

    stroke_length = Column(Integer)
    stroke_limit = Column(Integer)
    padding_steps = Column(Integer)

    max_steps = Column(Integer)

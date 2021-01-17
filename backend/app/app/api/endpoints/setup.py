from fastapi import APIRouter

from app.crud.crud_settings import settings_crud
from app.database.core import db_client

router = APIRouter()

INITIAL_SETTINGS = {
    "machine-thrust": {
        "name": "main",
        "microsteps_per_rev": 400,
        "wave_resolution": 20,
        "stroke_limit": 155,
        "max_stroke": 155,
        "padding_mm": 2,
        "max_steps": None,
        "active": True,
    }
}


@router.post("/initialize/")
async def initialize():
    await db_client.drop_database("data")
    await settings_crud.create("machine-thrust", INITIAL_SETTINGS["machine-thrust"])

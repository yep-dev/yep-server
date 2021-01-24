from fastapi import APIRouter
from starlette.requests import Request

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
        "padding_mm": 5,
        "tick_stroke_limit": 5,
        "stroke_force_chart": [50, 40, 30, 25, 23, 22, 20, 18, 15, 10],
        "max_steps": None,
        "active": True,
    }
}


@router.post("/initialize/")
async def initialize(request: Request):
    await db_client.drop_database("data")
    await settings_crud.create(
        request, "machine-thrust", INITIAL_SETTINGS["machine-thrust"]
    )

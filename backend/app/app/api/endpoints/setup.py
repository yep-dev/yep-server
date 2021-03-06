from fastapi import APIRouter
from starlette.requests import Request

from crud.crud_settings import settings_crud
from database.core import db_client

router = APIRouter()

INITIAL_SETTINGS = {
    "machine-thrust": {
        "name": "main",
        "active": True,
        
        "tick_stroke_limit": 10,
        "force_limit": 1000,
        "stroke_force_chart": [50, 40, 30, 25, 23, 22, 20, 18, 15, 10],
        
        "microsteps_per_rev": 400,
        "wave_resolution": 120,
        
        "stroke_limit": 155,
        "max_stroke": 155,
        "padding_mm": 5,
        
        "max_steps": None,
    }
}


@router.post("/initialize/")
async def initialize(request: Request):
    await db_client.drop_database("data")
    await settings_crud.create(
        request, "machine-thrust", INITIAL_SETTINGS["machine-thrust"]
    )

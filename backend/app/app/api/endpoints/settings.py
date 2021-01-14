import time

from fastapi import APIRouter
from starlette.requests import Request

from app import schemas
from app.crud.crud_settings import settings_crud
from app.streams import commands

router = APIRouter()


@router.get("/{model}/{id}", response_model=schemas.MachineThrustSettingsDisplay)
async def get_settings(model, id):
    item = await settings_crud.get(id)
    print(item)
    return {**item, "id": str(item["_id"])}


@router.get("/{model}/")
async def list_settings(model):
    return await settings_crud.list()


@router.post("/{model}/", response_model=schemas.MachineThrustSettingsDisplay)
async def create_settings(model: str, data: schemas.MachineThrustSettingsEdit):
    item = await settings_crud.create(model, data)
    return item


@router.put("/{model}/{id}")
async def update_settings(
    request: Request, model: str, id: str, data: schemas.MachineThrustSettingsEdit
):
    print(data)
    item = await settings_crud.update(model, id, data)
    if item:
        redis = request.app.extra["redis"]
        redis.xadd(
            commands.command_all,
            {"type": commands.update_settings, "time": time.time()},
        )
        return "updated"

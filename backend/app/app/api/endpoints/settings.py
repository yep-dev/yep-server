import time

from fastapi import APIRouter
from starlette.requests import Request

from crud.crud_settings import settings_crud
from schemas.settings import ThrustSettingsDisplay, ThrustSettingsEdit
from streams import commands

router = APIRouter()


@router.get("/{model}/{id}", response_model=ThrustSettingsDisplay)
async def get_settings(request: Request, model, id):
    item = await settings_crud.get(request, id)
    return item


@router.get("/{model}/")
async def list_settings(request: Request, model):
    return await settings_crud.list(request)


@router.post("/{model}/", response_model=ThrustSettingsDisplay)
async def create_settings(request: Request, model: str, data: ThrustSettingsEdit):
    item = await settings_crud.create(request, model, data)
    return item


@router.put("/{model}/{id}", response_model=ThrustSettingsDisplay)
async def update_settings(
    request: Request,
    model: str,
    id: str,
    data: ThrustSettingsEdit,
    machine: bool = False,
):
    print(data)
    item = await settings_crud.update(request, model, id, data)
    if item:
        if not machine:
            redis = request.app.extra["redis"]
            redis.xadd(
                commands.command_all,
                {"type": commands.update_settings, "time": time.time()},
            )
        return item

from fastapi import APIRouter

from app import schemas
from app.crud.crud_settings import settings_crud

router = APIRouter()

INITIAL_SETTINGS = {
    "machine-thrust": {
        "name": "main",
        "microsteps_per_rev": 400,
        "wave_resolution": 20,
        "stroke_length": 183,
        "stroke_limit": 200,
        "padding_steps": 60,
        "max_steps": None,
    }
}


@router.get("/{model}/{id}", response_model=schemas.MachineThrustSettingsDisplay)
async def get_settings(model, id):
    items = await settings_crud.get()
    return {**items[0], "id": str(items[0]["_id"])}


@router.post("/{model}/", response_model=schemas.MachineThrustSettingsDisplay)
async def create_settings(model: str, data: schemas.MachineThrustSettingsEdit):
    item = await settings_crud.create(model, data)
    return item


@router.put("/{model}/{id}")
async def update_item(model: str, id: str, data: schemas.MachineThrustSettingsEdit):
    item = await settings_crud.update(model, id, data)
    if item:
        return "updated"


# @router.delete("/")
# def reset_settings(*, db: Session = Depends(deps.get_db)) -> Any:
#     for model_name, data in INITIAL_SETTINGS.items():
#         model = MODELS_MAPPING[model_name]
#         db.query(model).delete()
#         db.commit()
#         crud.settings.create(db, model_name, data)
#         db.commit()
#

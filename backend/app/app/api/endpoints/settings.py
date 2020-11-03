from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.crud.crud_settings import MODELS_MAPPING
from app.db.initial_settings import INITIAL_SETTINGS

router = APIRouter()


@router.get("/{model}/{id}")
def read_items(*, db: Session = Depends(deps.get_db), model: str, id: int,) -> Any:
    items = crud.settings.get(db, model=model, id=id)
    return items


@router.post("/{model}/", response_model=schemas.MachineThrustSettings)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    model: str,
    data: schemas.MachineThrustSettings,
) -> Any:
    item = crud.settings.create(db, model, data)
    return item


@router.put("/{model}/{id}", response_model=schemas.MachineThrustSettings)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    model: str,
    id: int,
    data: Union[
        schemas.MachineThrustSettings, schemas.MachineThrustCalibrationSettings
    ],
) -> Any:
    item = crud.settings.get(db=db, model=model, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.settings.update(db=db, db_obj=item, data=data)
    return item


@router.delete("/")
def reset_settings(*, db: Session = Depends(deps.get_db)) -> Any:
    for model_name, data in INITIAL_SETTINGS.items():
        model = MODELS_MAPPING[model_name]
        db.query(model).delete()
        db.commit()
        crud.settings.create(db, model_name, data)
        db.commit()

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models.settings import MachineThrustSettings

MODELS_MAPPING = {"machine-thrust": MachineThrustSettings}


class CRUDSettings:
    def get(self, db: Session, model: str, id: int):
        model = MODELS_MAPPING[model]
        return db.query(model).filter(model.id == id).first()

    def create(self, db, model: str, data):
        model = MODELS_MAPPING[model]
        data = jsonable_encoder(data)
        db_obj = model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj, data):
        obj_data = jsonable_encoder(db_obj)

        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


settings = CRUDSettings()

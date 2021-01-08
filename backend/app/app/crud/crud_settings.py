from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.database.core import db_client

database = db_client.settings
settings = database.get_collection("settings_collection")
# MODELS_MAPPING = {"machine-thrust": MachineThrustSettings}


class CRUDSettings:
    async def get(self):
        settings_ = []
        async for setting in settings.find():
            settings_.append(setting)
        return settings_

    async def create(self, model, data):
        # model = MODELS_MAPPING[model]
        data = jsonable_encoder(data)
        await settings.insert_one(data)
        return data

    async def update(self, model, id: str, data):
        item = settings.find_one({"_id": ObjectId(id)})
        if item:
            data = jsonable_encoder(data)
            print(data)
            updated_item = await settings.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            print(updated_item.modified_count)
            if updated_item:
                return True
        return False


settings_crud = CRUDSettings()

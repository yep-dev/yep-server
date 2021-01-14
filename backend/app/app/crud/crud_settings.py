from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.database.core import db_client

database = db_client.data
settings = database.get_collection("settings")


# MODELS_MAPPING = {"machine-thrust": MachineThrustSettings}


class CRUDSettings:
    async def _get_item(self, id):
        if id == "default":
            item = await settings.find_one({"active": True})
        else:
            item = await settings.find_one({"_id": ObjectId(id)})
        return item

    async def get(self, id):
        return await self._get_item(id)

    async def list(self):
        x = await settings.to_list()
        return x

    async def create(self, model, data):
        # model = MODELS_MAPPING[model]
        data = jsonable_encoder(data)
        await settings.insert_one(data)
        return data

    async def update(self, model, id: str, data):
        item = await self._get_item(id)
        if item:
            data = jsonable_encoder(data)
            data = {k: v for k, v in data.items() if v is not None}
            updated_item = await settings.update_one(
                {"_id": item["_id"]}, {"$set": data}
            )
            if updated_item:
                return True
        return False


settings_crud = CRUDSettings()

from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.schemas.settings import ThrustSettings

# MODELS_MAPPING = {"machine-thrust": MachineThrustSettings}


class CRUDSettings:
    async def _get_item(self, settings, id):
        if id == "default":
            item = await settings.find_one({"active": True})
        else:
            item = await settings.find_one({"_id": ObjectId(id)})
        item = ThrustSettings(**item, id=str(item["_id"]))

        computed = {}
        if item.max_steps:
            computed["steps_per_mm"] = item.max_steps / item.max_stroke

        return {**jsonable_encoder(item), **computed}

    async def get(self, request, id):
        settings = request.app.extra["db"].data.get_collection("settings")
        return await self._get_item(settings, id)

    async def list(self, request):
        settings = request.app.extra["db"].data.get_collection("settings")
        x = await settings.to_list()
        return x

    async def create(self, request, model, data):
        settings = request.app.extra["db"].data.get_collection("settings")
        # model = MODELS_MAPPING[model]
        data = jsonable_encoder(data)
        await settings.insert_one(data)
        return data

    async def update(self, request, model, id: str, data):
        settings = request.app.extra["db"].data.get_collection("settings")
        item = await self._get_item(settings, id)
        if item:
            data = jsonable_encoder(data)
            data = {k: v for k, v in data.items() if v is not None}
            print(item)
            updated_item = await settings.update_one(
                {"_id": item["id"]}, {"$set": data}
            )
            return jsonable_encoder(updated_item.raw_result)


settings_crud = CRUDSettings()

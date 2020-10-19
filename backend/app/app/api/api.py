from fastapi import APIRouter

from app.api.endpoints import items, login, users, utils, commands, wave, stream

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(wave.router, prefix="/wave", tags=["wave"])
api_router.include_router(commands.router, prefix="/commands", tags=["commands"])
api_router.include_router(stream.router, prefix="/stream", tags=["stream"])

from fastapi import APIRouter

from app.api.endpoints import commands, curve, settings, setup, stream, wave

api_router = APIRouter()
api_router.include_router(wave.router, prefix="/wave", tags=["wave"])
api_router.include_router(commands.router, prefix="/commands", tags=["commands"])
api_router.include_router(stream.router, prefix="/stream", tags=["stream"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(curve.router, prefix="/curve", tags=["curve"])
api_router.include_router(setup.router, prefix="/setup", tags=["setup"])

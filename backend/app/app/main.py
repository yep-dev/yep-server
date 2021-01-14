import aioredis
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=True,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def handle_startup():
    try:
        redis = await aioredis.create_redis(settings.REDIS_URL)
        # logger.info(f"Connected to Redis")
        app.extra["redis"] = redis
    except ConnectionRefusedError:
        # logger.info(f"cannot connect to redis on {REDIS_HOST} {REDIS_PORT}")
        return

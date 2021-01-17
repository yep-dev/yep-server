import aioredis
import motor.motor_asyncio
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings

MONGO_DETAILS = "mongodb://192.168.99.101:27017"

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


@app.on_event("startup")
async def startup_event():
    db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    app.extra["db"] = db_client


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True, loop="asyncio")

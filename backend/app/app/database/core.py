import motor.motor_asyncio

MONGO_DETAILS = "mongodb://192.168.99.101:27017"

db_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

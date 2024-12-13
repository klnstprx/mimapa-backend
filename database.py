import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["mimapadb"]

markers_collection = db["markers"]
logs_collection = db["logs"]
visits_collection = db["visits"]

from motor.motor_asyncio import AsyncIOMotorClient


mongo_url = "mongodb://localhost:27017"
mongo_client = AsyncIOMotorClient(mongo_url)
DB = mongo_client['eventsync_db']
events_collection = DB["events"]



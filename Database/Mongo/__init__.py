from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import Config

def check():
    if not config.MONGO_DB_URI:
        return

def mongo_build():
    check()
    mongo = MongoClient(Config.MONGO_DB_URI)
    return db = mongo.EMB



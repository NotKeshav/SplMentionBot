import asyncio
import time

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client

import Config

loop = asyncio.get_event_loop()
boot = time.time()

mongo = MongoClient(Config.MONGO_DB_URI)
db = mongo.AFK


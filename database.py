# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["MovieBot"]

movies = db.movies
users = db.users
chats = db.chats

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #


async def add_movie(data):

    existing = await movies.find_one(
        {"file_id": data["file_id"]}
    )

    if not existing:
        await movies.insert_one(data)

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

async def add_user(user_id):

    await users.update_one(
        {"_id": user_id},
        {"$setOnInsert": {"_id": user_id}},
        upsert=True
    )

async def add_chat(chat_id):

    await chats.update_one(
        {"_id": chat_id},
        {"$setOnInsert": {"_id": chat_id}},
        upsert=True
    )
    
# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

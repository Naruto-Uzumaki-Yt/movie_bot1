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


async def add_user(user_id):

    user = await users.find_one(
        {"user_id": user_id}
    )

    if not user:
        await users.insert_one(
            {"user_id": user_id}
        )

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

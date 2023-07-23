from model import User, UserInDb
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("CLUSTER_PASSWORD")
client = motor.motor_asyncio.AsyncIOMotorClient(api_key)
database = client.UserList
collection = database.user


# User DB Calls Start
async def fetch_all_users():
    users = []
    cursor = collection.find({})
    async for document in cursor:
        users.append(User(**document))
    return users


async def create_user(user):
    document = user
    result = await collection.insert_one(document)
    return document


async def fetch_one_user(id):
    user = await collection.find_one({"_id": id})
    if user is not None:
        return user


async def fetch_one_user_by_username(username):
    user = await collection.find_one({"username": username})
    if user is not None:
        return UserInDb(**user)
    return None


async def update_user(id, user):
    update_result = await collection.update_one({"_id": id}, {"$set": user})
    if update_result.modified_count == 1:
        updated_user = await collection.find_one({"_id": id})
        if updated_user is not None:
            return updated_user
    existing_user = await collection.find_one({"_id": id})
    if existing_user is not None:
        return existing_user


async def remove_user(id):
    await collection.delete_one({"_id": id})
    return True


# User DB Calls End

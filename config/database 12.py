from motor.motor_asyncio import AsyncIOMotorClient  # PyMongo's async client
from urllib.parse import quote_plus

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
host = os.getenv("MONGO_HOST")

uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{host}/?retryWrites=true&w=majority&appName=CoordiName-CoordiName"

# Create a new client and connect to the server asynchronously


async def ping_mongodb():
    # Assuming 'client' is your AsyncIOMotorClient instance
    try:
        # The ping command is cheap and does not require auth (admin database)
        result = await client.admin.command('ping')
        print("Ping result:", result)
    except Exception as e:
        print("An error occurred while pinging MongoDB:", e)


async def connect_to_mongo():
    global client, db, collection_user, collection_apiKey
    client = AsyncIOMotorClient(uri)
    await ping_mongodb()
    db = client["CoordiName"]
    collection_user = db["users"]
    collection_apiKey = db["api_keys"]


async def close_mongodb():
    client.close()
    print("MongoDB connection closed")

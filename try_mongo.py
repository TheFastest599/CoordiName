from fastapi import FastAPI
from pymongo.mongo_client import MongoClient

from urllib.parse import quote_plus

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
host = os.getenv("MONGO_HOST")

uri = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{host}/?retryWrites=true&w=majority&appName=CoordiName-CoordiName"
print(uri)


# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

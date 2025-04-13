from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI, server_api=ServerApi("1"),)

def get_db():
    """Returns the MongoDB database instance."""
    try:
        # client.admin.command("ping")
        print("DATABASE CONNECTED SUCCESSFULLY")
        return client["Fastapi_Mongodb"]
    except ConnectionFailure:
        print("Database Connection Error")
        raise Exception("Database Connection Error")

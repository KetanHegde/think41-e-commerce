import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "ecommerce")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
conversations = db['conversations']

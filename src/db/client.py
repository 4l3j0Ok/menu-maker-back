from modules import config
from pymongo import MongoClient


client = MongoClient(
    host = config.MONGO_HOST,
    port = config.MONGO_PORT,
    username = config.MONGO_USER,
    password = config.MONGO_PASS
)

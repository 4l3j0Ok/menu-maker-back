import os


ROUTERS = [
    "users"
]

MONGO_HOST = "mongodb://db"
MONGO_PORT = 27017
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
import os

APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
ROUTERS = [
    {
        "module": "menus"
    },
    {
        "module": "sections",
        "parent": "menus"
    },
    {
        "module": "products",
        "parent": "menus/sections"
    }
]

LOG_PATH = "/var/log/app.log"
LOG_NAME = "uvicorn.error"

APP_TITLE = "Menu Maker Backend"
APP_DESCRIPTION = "API de Menu Maker."
APP_VERSION = "v1.0.0"

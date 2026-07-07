import os
from beanie import init_beanie
from urllib.parse import quote_plus
from pymongo import AsyncMongoClient

from app.models import Recipe


def get_mongo_uri() -> str:
    if mongo_uri := os.getenv("MONGO_DB_URI"):
        return mongo_uri

    username = os.getenv("MONGO_DB_USERNAME")
    password = os.getenv("MONGO_DB_PASSWORD")
    host = os.getenv("MONGO_DB_HOST", "localhost")
    port = os.getenv("MONGO_DB_PORT", "27017")

    if username and password:
        return (
            f"mongodb://{quote_plus(username)}:{quote_plus(password)}"
            f"@{host}:{port}/?authSource=admin"
        )

    return f"mongodb://{host}:{port}/"


async def init_database() -> None:
    client = AsyncMongoClient(get_mongo_uri(), serverSelectionTimeoutMS=5000)
    await init_beanie(
        database=client[os.getenv("MONGO_DB_NAME", "recipes")],
        document_models=[Recipe],
    )

import os
from random import randrange
from urllib.parse import quote_plus

import pymongo
from fastapi import APIRouter, HTTPException, Query
from pymongo.errors import PyMongoError

from app.schemas import RecipeCreate, RecipeListResponse, RecipeResponse


recipes_router = APIRouter()


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


client = pymongo.MongoClient(get_mongo_uri(), serverSelectionTimeoutMS=5000)
recipes_collection = client["recipes"]["recipesCollection"]


def generate_recipe_id() -> int:
    for _ in range(10):
        recipe_id = randrange(1, 1_000_001)
        if recipes_collection.count_documents({"id": recipe_id}, limit=1) == 0:
            return recipe_id

    raise HTTPException(status_code=503, detail="Could not allocate a recipe id")


@recipes_router.get("/")
async def get_recipes(
    limit: int = Query(default=8, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
) -> RecipeListResponse:
    try:
        cursor = recipes_collection.find({}, {"_id": 0}).skip(skip).limit(limit)
        recipes = [RecipeResponse(**doc) for doc in cursor]
        total = recipes_collection.count_documents({})
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return RecipeListResponse(recipes=recipes, total=total, limit=limit, skip=skip)


@recipes_router.post("/", status_code=201, response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate) -> RecipeResponse:
    recipe_dict = recipe.model_dump()
    try:
        recipe_dict["id"] = generate_recipe_id()
        recipes_collection.insert_one(recipe_dict)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return RecipeResponse(**recipe_dict)

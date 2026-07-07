import random
import pymongo
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class RecipeResponse(BaseModel):
    id: int
    name: str
    ingredients: list
    instructions: list
    prepTimeMinutes: int
    cookTimeMinutes: int
    servings: int
    difficulty: str
    cuisine: str
    caloriesPerServing: int
    image: str
    rating: float
    reviewCount: int


class RecipeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    ingredients: list
    instructions: list
    prepTimeMinutes: int = Field(ge=1)
    cookTimeMinutes: int = Field(ge=1)
    servings: int = Field(ge=1)
    difficulty: str = Field(..., min_length=1)
    cuisine: str = Field(..., min_length=1)
    caloriesPerServing: int = Field(ge=1)
    image: str = Field(..., min_length=1)
    rating: float = Field(ge=0)
    reviewCount: int = Field(ge=1)


app = FastAPI()
client = pymongo.MongoClient(
    f"mongodb://{'admin'}:{'password'}@localhost:27017/?authSource=admin"
)


@app.get("/")
async def get_recipes(
    limit: int = Query(default=8, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
) -> list:
    cursor = client["recipes"]["recipesCollection"].find().skip(skip).limit(limit)
    result = [RecipeResponse(**doc) for doc in cursor]
    result.append({"total": len(result), "limit": limit, "skip": skip})
    return result


@app.post("/", status_code=201)
def create_recipe(recipe: RecipeCreate):
    recipe_dict = recipe.model_dump()
    recipe_dict["id"] = random.randint(1, 100000)
    result = client["recipes"]["recipesCollection"].insert_one(recipe_dict)
    return {
        "message": "recipe created successfully",
        "inserted_id": str(result.inserted_id)
    }
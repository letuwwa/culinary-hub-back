from beanie import Document, Indexed
from pydantic import model_validator


class Recipe(Document):
    recipe_id: Indexed(int, unique=True, sparse=True) | None = None
    name: str
    ingredients: list[str]
    instructions: list[str]
    prepTimeMinutes: int
    cookTimeMinutes: int
    servings: int
    difficulty: str
    cuisine: str
    caloriesPerServing: int
    image: str
    rating: float
    reviewCount: int

    @model_validator(mode="before")
    @classmethod
    def populate_recipe_id(cls, data):
        if isinstance(data, dict) and "recipe_id" not in data:
            legacy_id = data.get("id")
            if isinstance(legacy_id, int):
                data = data.copy()
                data["recipe_id"] = legacy_id
                del data["id"]
        return data

    class Settings:
        name = "recipesCollection"

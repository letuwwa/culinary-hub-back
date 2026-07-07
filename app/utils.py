from random import randrange
from fastapi import HTTPException

from app.models import Recipe
from app.schemas import RecipeResponse


async def generate_recipe_id() -> int:
    for _ in range(10):
        recipe_id = randrange(1, 1_000_001)
        existing_recipe = await Recipe.find_one(
            {"$or": [{"recipe_id": recipe_id}, {"id": recipe_id}]}
        )
        if existing_recipe is None:
            return recipe_id

    raise HTTPException(status_code=503, detail="Could not allocate a recipe id")


async def find_recipe_by_public_id(recipe_id: int) -> Recipe | None:
    recipe = await Recipe.find_one(
        {"$or": [{"recipe_id": recipe_id}, {"id": recipe_id}]}
    )
    if recipe is not None:
        return recipe

    recipes_without_numeric_id = await Recipe.find({"recipe_id": None}).to_list()
    return next(
        (
            recipe
            for recipe in recipes_without_numeric_id
            if int(str(recipe.id)[-8:], 16) == recipe_id
        ),
        None,
    )


def to_recipe_response(recipe: Recipe) -> RecipeResponse:
    recipe_dict = recipe.model_dump()
    recipe_dict["id"] = recipe.recipe_id or int(str(recipe.id)[-8:], 16)
    return RecipeResponse.model_validate(recipe_dict)

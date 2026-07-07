from pymongo.errors import PyMongoError
from fastapi import APIRouter, HTTPException, Query

from app.models import Recipe
from app.schemas import RecipeCreate, RecipeListResponse, RecipeResponse
from app.utils import generate_recipe_id, find_recipe_by_public_id, to_recipe_response


recipes_router = APIRouter()


@recipes_router.get("/")
async def get_recipes(
    limit: int = Query(default=8, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
) -> RecipeListResponse:
    try:
        recipe_documents = await Recipe.find_all(skip=skip, limit=limit).to_list()
        recipes = [to_recipe_response(recipe) for recipe in recipe_documents]
        total = await Recipe.count()
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return RecipeListResponse(recipes=recipes, total=total, limit=limit, skip=skip)


@recipes_router.post("/", status_code=201, response_model=RecipeResponse)
async def create_recipe(recipe: RecipeCreate) -> RecipeResponse:
    recipe_dict = recipe.model_dump()
    try:
        recipe_dict["recipe_id"] = await generate_recipe_id()
        recipe_document = Recipe.model_validate(recipe_dict)
        await recipe_document.insert()
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return to_recipe_response(recipe_document)


@recipes_router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: int):
    recipe = await find_recipe_by_public_id(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    try:
        await recipe.delete()
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc


@recipes_router.put("/{recipe_id}", status_code=200, response_model=RecipeResponse)
async def update_recipe(recipe_id: int, payload: dict):
    recipe = await find_recipe_by_public_id(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    try:
        for key, value in payload.items():
            setattr(recipe, key, value)
        await recipe.save()
        return to_recipe_response(recipe)
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

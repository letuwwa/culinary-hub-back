from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
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


class RecipeResponse(RecipeBase):
    id: int


class RecipeListResponse(BaseModel):
    recipes: list[RecipeResponse]
    total: int
    limit: int
    skip: int


class RecipeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    ingredients: list[str] = Field(..., min_length=1)
    instructions: list[str] = Field(..., min_length=1)
    prepTimeMinutes: int = Field(ge=1)
    cookTimeMinutes: int = Field(ge=1)
    servings: int = Field(ge=1)
    difficulty: str = Field(..., min_length=1)
    cuisine: str = Field(..., min_length=1)
    caloriesPerServing: int = Field(ge=1)
    image: str = Field(..., min_length=1)
    rating: float = Field(ge=0, le=5)
    reviewCount: int = Field(ge=0)


class RecipeUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1)
    ingredients: list[str] | None = Field(default=None, min_length=1)
    instructions: list[str] | None = Field(default=None, min_length=1)
    prepTimeMinutes: int | None = Field(default=None, ge=1)
    cookTimeMinutes: int | None = Field(default=None, ge=1)
    servings: int | None = Field(default=None, ge=1)
    difficulty: str | None = Field(default=None, min_length=1)
    cuisine: str | None = Field(default=None, min_length=1)
    caloriesPerServing: int | None = Field(default=None, ge=1)
    image: str | None = Field(default=None, min_length=1)
    rating: float | None = Field(default=None, ge=0, le=5)
    reviewCount: int | None = Field(default=None, ge=0)

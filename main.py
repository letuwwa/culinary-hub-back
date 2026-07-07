import os

from fastapi import FastAPI
from dotenv import load_dotenv
from app.endpoints import recipes_router
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()
allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allowed_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(recipes_router, prefix="/recipes", tags=["Recipes"])


@app.get("/", status_code=200)
def root():
    return {"status": "ok"}

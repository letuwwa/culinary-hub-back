import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv
from app.endpoints import recipes_router
from app.database import init_database
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield


app = FastAPI(lifespan=lifespan)
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

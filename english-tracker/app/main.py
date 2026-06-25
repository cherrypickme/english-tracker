from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes import batches, topics
import app.models  # noqa: F401

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(topics.router)
app.include_router(batches.router)


@app.on_event("startup")
def create_tables():
    Path("data").mkdir(exist_ok=True)
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}

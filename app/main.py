from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "URL Shortener + Analytics API")

app.include_router(router)
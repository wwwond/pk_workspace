from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.main import search_router,itinerary_router
import models
from database import Base, engine

# models.get_related_models()

# Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(search_router)
app.include_router(itinerary_router)
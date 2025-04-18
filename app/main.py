from fastapi import FastAPI
from app.api import players
from app.core.config import settings
from app.database import engine
import app.models.player as models


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)


app.include_router(
    players.router,
    prefix=f"{settings.API_V1_STR}/players",
    tags=["players"]
)

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}
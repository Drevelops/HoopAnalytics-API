from fastapi import FastAPI
from app.api import players, auth
from app.core.config import settings
from app.database import engine
from app.models import player, user
from app.api import auth
from app.database import Base

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)


app.include_router(
    players.router,
    prefix=f"{settings.API_V1_STR}/players",
    tags=["players"]
)

app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"]
)

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}
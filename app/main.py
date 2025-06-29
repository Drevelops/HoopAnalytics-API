from fastapi import FastAPI
from app.api import players, auth, teams
from app.core.config import settings
from app.database import engine
from app.models import player, user
from app.api import auth
from app.database import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://localhost:3000",  
        "https://hoop-analytics-api.vercel.app/",   
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(
    teams.router,
    prefix = f"{settings.API_V1_STR}/teams",
    tags=["teams"]
)

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}
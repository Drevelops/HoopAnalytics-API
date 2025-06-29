from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import players, auth, teams
from app.core.config import settings
from app.database import engine
from app.models import player, user
from app.database import Base
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    print("🚀 Starting up NBA Analytics API...")
    
    # Import all models to register them
    from app.models.player import Players, PlayerStats
    from app.models.team import Teams
    from app.models.user import User
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    yield  

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan  
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://localhost:3000",  
        "https://hoop-analytics-api.vercel.app", 
        "https://*.vercel.app", 
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
    prefix=f"{settings.API_V1_STR}/teams",
    tags=["teams"]
)

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}

@app.get('/health')
def health_check():
    return {"status": "healthy", "message": "NBA Analytics API is running"}
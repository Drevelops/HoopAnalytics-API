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
    prefix="/api/v1/players",
    tags=["players"]
)

app.include_router(
    teams.router,
    prefix="/api/v1/teams",
    tags=["teams"]
)

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"]
)

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}

@app.get('/health')
def health_check():
    return {"status": "healthy", "message": "NBA Analytics API is running"}

@app.post('/admin/seed-database')
async def seed_database():
    """Populate database with NBA data - USE ONLY ONCE!"""
    try:
        # comprehensive seed function
        from scripts.seed_data import populate_nba_data 
        populate_nba_data()
        return {
            "message": "✅ Database seeded successfully!", 
            "data": "30 NBA teams, 50+ players, 30+ player stats"
        }
    except Exception as e:
        return {"error": f"❌ Seeding failed: {str(e)}"}
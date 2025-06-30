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
    

@app.get('/admin/debug-routes')
async def debug_routes():
    """Debug what routes are registered"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": getattr(route, 'name', 'unknown')
            })
    
    return {"routes": routes}

@app.get('/api/v1/test-teams')
async def test_teams():
    """Simple test to get teams without schemas"""
    try:
        from app.database import Session
        from app.models.team import Teams
        
        db = Session()
        teams = db.query(Teams).limit(5).all()
        
        result = []
        for team in teams:
            result.append({
                "id": team.id,
                "name": team.team_name,
                "city": team.city
            })
        
        db.close()
        return {"teams": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.schemas import Team,TeamCreate,TeamUpdate
from app.services import team_service
from app.database import get_db

router = APIRouter()

@router.get('/', response_model=List[Team])
def get_teams(team_name: str = None,conference: str = None, division: str = None, db: Session = Depends(get_db)):
    return team_service.get_teams(db,team_name,conference,division)
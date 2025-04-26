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

@router.get('/{team_id}', response_model=Team)
def get_teams_by_id(team_id: int, db: Session = Depends(get_db)):
    return team_service.get_team_by_id(db,team_id)

@router.post('/create_team',response_model=Team)
def create_team(team:TeamCreate,db:Session = Depends(get_db)):
    return team_service.create_team(db,team)

@router.put('/update_team/{team_id}',response_model=Team)
def update_team(team_id: int ,team:TeamUpdate, db:Session = Depends(get_db)):
    return team_service.update_team(team_id,team,db)

@router.delete('/delete_team/{team_id}', response_model = Team)
def delete_player(team_id:int,db:Session = Depends(get_db)):
    return team_service.delete_team(db,team_id)
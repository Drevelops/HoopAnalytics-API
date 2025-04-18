from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.schemas import Player, PlayerCreate, PlayerUpdate
from app.services import player_service
from app.database import get_db

router = APIRouter()

@router.get('/', response_model=List[Player])
def get_players(position: str = None, name: str = None, team: str = None, db: Session = Depends(get_db)):
    return player_service.get_players(db, position, name, team)

@router.get('/{player_id}', response_model=Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    return player_service.get_player_by_id(db, player_id)

@router.post('/create_player', response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return player_service.create_player(db, player)

@router.put("/update_player/{player_id}", response_model=Player)
def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db)):
    return player_service.update_player(db, player_id, player)

@router.delete("/delete_player/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player_service.delete_player(db, player_id)
    return {"message": "Player deleted successfully"}
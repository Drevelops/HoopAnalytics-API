from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.schemas import Player, PlayerCreate, PlayerUpdate , PlayerStats,PlayerStatsCreate,PlayerStatsUpdate
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

@router.get('/stats', response_model=List[PlayerStats])
def get_stats(player_id: int = None, season: str = None, db: Session = Depends(get_db)):
    return player_service.get_stats(db, player_id, season)

@router.get('/stats/{stats_id}', response_model=PlayerStats)
def get_stat_by_id(stats_id: int, db: Session = Depends(get_db)):
    return player_service.get_stats_by_id(db, stats_id)

@router.get('/{player_id}/stats', response_model=List[PlayerStats])
def get_player_stats(player_id: int, season: str = None, db: Session = Depends(get_db)):
    return player_service.get_player_stats(db, player_id, season)

@router.post('/{player_id}/stats', response_model=PlayerStats)
def create_player_stats(player_id: int, stats: PlayerStatsCreate, db: Session = Depends(get_db)):
    return player_service.create_player_stats(db, player_id, stats)

@router.put('/stats/{stats_id}', response_model=PlayerStats)
def update_stats(stats_id: int, stats: PlayerStatsUpdate, db: Session = Depends(get_db)):
    return player_service.update_stats(db, stats_id, stats)

@router.delete('/stats/{stats_id}')
def delete_stats(stats_id: int, db: Session = Depends(get_db)):
    player_service.delete_stats(db, stats_id)
    return {"message": "Stats deleted successfully"}
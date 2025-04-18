from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.player import Players
from app.models.schemas import PlayerCreate, PlayerUpdate

def get_players(
    db: Session, 
    position: Optional[str] = None, 
    name: Optional[str] = None, 
    team: Optional[str] = None
) -> List[Players]:
    """Get players with optional filtering"""
    query = db.query(Players)
    
    if position:
        query = query.filter(Players.position.ilike(f"{position}"))
    
    if name:
        query = query.filter(Players.name.ilike(f"%{name}%"))
    
    if team:
        query = query.filter(Players.team_name.ilike(f"%{team}%"))
    
    players = query.all()
    
    if not players and (position or name or team):
        raise HTTPException(status_code=404, detail="No players found matching the criteria")
        
    return players

def get_player_by_id(db: Session, player_id: int) -> Players:
    """Get a player by ID"""
    player = db.query(Players).filter(Players.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")
    return player

def create_player(db: Session, player: PlayerCreate) -> Players:
    """Create a new player"""
    player_data = player.model_dump(exclude_unset=True)
    db_player = Players(**player_data)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def update_player(db: Session, player_id: int, player: PlayerUpdate) -> Players:
    """Update an existing player"""
    db_player = get_player_by_id(db, player_id)
    
    # Update player attributes
    for key, value in player.model_dump().items():
        setattr(db_player, key, value)
    
    db.commit()
    db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int) -> None:
    """Delete a player"""
    db_player = get_player_by_id(db, player_id)
    db.delete(db_player)
    db.commit()
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.player import Players, PlayerStats
from app.models.schemas import PlayerCreate, PlayerUpdate, PlayerStatsCreate, PlayerStatsUpdate

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

def get_stats(
    db: Session,
    player_id: Optional[int] = None,
    season: Optional[str] = None
) -> List[PlayerStats]:
    """Get all stats with optional filtering"""
    query = db.query(PlayerStats)
    
    if player_id:
        query = query.filter(PlayerStats.player_id == player_id)
    
    if season:
        query = query.filter(PlayerStats.season == season)
    
    stats = query.all()
    
    if not stats and (player_id or season):
        raise HTTPException(status_code=404, detail="No stats found matching the criteria")
        
    return stats

def get_stats_by_id(db: Session, stats_id: int) -> PlayerStats:
    """Get stats by ID"""
    stats = db.query(PlayerStats).filter(PlayerStats.id == stats_id).first()
    if not stats:
        raise HTTPException(status_code=404, detail=f"Stats with id {stats_id} not found")
    return stats

def get_player_stats(
    db: Session,
    player_id: int,
    season: Optional[str] = None
) -> List[PlayerStats]:
    """Get all stats for a specific player"""
    get_player_by_id(db, player_id)
    
    query = db.query(PlayerStats).filter(PlayerStats.player_id == player_id)
    
    if season:
        query = query.filter(PlayerStats.season == season)
    
    stats = query.all()
    
    if not stats:
        raise HTTPException(
            status_code=404, 
            detail=f"No stats found for player with id {player_id}" + 
                  (f" in season {season}" if season else "")
        )
        
    return stats

def create_player_stats(
    db: Session,
    player_id: int,
    stats: PlayerStatsCreate
) -> PlayerStats:
    """Create stats for a player"""
    get_player_by_id(db, player_id)
    
    if hasattr(stats, 'season') and stats.season:
        existing_stats = db.query(PlayerStats).filter(
            PlayerStats.player_id == player_id,
            PlayerStats.season == stats.season
        ).first()
        
        if existing_stats:
            raise HTTPException(
                status_code=400,
                detail=f"Stats for player {player_id} in season {stats.season} already exist"
            )
    
    stats_data = stats.model_dump(exclude_unset=True)
    stats_data['player_id'] = player_id
    
    db_stats = PlayerStats(**stats_data)
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats

def update_stats(
    db: Session,
    stats_id: int,
    stats: PlayerStatsUpdate
) -> PlayerStats:
    """Update stats"""
    db_stats = get_stats_by_id(db, stats_id)
    
    # Update stats attributes
    update_data = stats.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_stats, key, value)
    
    db.commit()
    db.refresh(db_stats)
    return db_stats

def delete_stats(db: Session, stats_id: int) -> None:
    """Delete stats"""
    db_stats = get_stats_by_id(db, stats_id)
    db.delete(db_stats)
    db.commit()
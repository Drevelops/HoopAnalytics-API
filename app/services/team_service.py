from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.team import Teams
from app.models.schemas import TeamCreate, TeamUpdate

def get_teams(
        db: Session,
        team_name: Optional[str] = None,
        conference: Optional[str] = None,
        division: Optional[str] = None
) -> List[Teams]:
    """Get teams with optional filtering"""
    query = db.query(Teams)

    if team_name:
        query = query.filter(Teams.team_name.ilike(f"%{team_name}%"))

    if conference:
        query = query.filter(Teams.conference.ilike(f"%{conference}%"))
    
    if division:
        query = query.filter(Teams.division.ilike(f"%{division}%"))

    teams = query.all()

    if not teams and (team_name or conference or division):
        raise HTTPException(status_code=404, detail="No teams found matching the criteria")

def get_team_by_id(db: Session, team_id: int) -> Teams:
    """Get a team by ID"""
    team = db.query(Teams).filter(Teams.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail=f"team with id {team_id} not found")
    return team

def create_team(db: Session, team: TeamCreate) -> Teams:
    """Create a new player"""
    team_data = team.model_dump(exclude_unset=True)
    db_team = Teams(**team_data)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team: TeamUpdate) -> Teams:
    """Update an existing player"""
    db_team = get_team_by_id(db, team_id)
    
    # Update team attributes
    for key, value in team.model_dump().items():
        setattr(db_team, key, value)
    
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db:Session,team_id:int):
    '''Delete Team'''
    db_teams = get_team_by_id(db,team_id)
    db.delete(db_teams)
    db.commit()
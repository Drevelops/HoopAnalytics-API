from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import models
from database import engine


app = FastAPI(title="HoopAnalytics API",
              version="0.3")

models.Base.metadata.create_all(bind=engine)

class PlayerModel(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3)
    position: str = Field(min_length=1)
    height: str = Field(pattern=r"^[4-8]'(\d{1,2}\")?$")
    weight: int = Field(gt=130, lt=350)
    team_id: int =  Field(gt=0, lt=31)
    team_name: str = Field(min_length=3)
    age: int  = Field(ge=18, le=50)
    college: str 
    country: str = Field(min_length=2)
    ppg: float = Field(ge=0.0)
    apg: float = Field(ge=0.0)
    rpg: float = Field(ge=0.0)
    spg: float = Field(ge=0.0)
    bpg: float = Field(ge=0.0)
    fg_pct: float = Field(ge=0.0, le=1.0)
    ft_pct: float = Field(ge=0.0, le=1.0)
    threept_pct: float = Field(ge=0.0, le=1.0)

players = [
    {
        "id": 1,
        "name": "LeBron James",
        "position": "SF",
        "height": "6'9\"",
        "weight": 250,
        "team_id": 13,
        "team_name": "Los Angeles Lakers",
        "age": 40,
        "college": "None",
        "country": "USA",
        "ppg": 25.3,
        "apg": 8.1,
        "rpg": 7.4,
        "spg": 1.3,
        "bpg": 0.6,
        "fg_pct": 0.533,
        "ft_pct": 0.756,
        "threept_pct": 0.364
    },
    {
        "id": 2,
        "name": "Stephen Curry",
        "position": "PG",
        "height": "6'2\"",
        "weight": 185,
        "team_id": 9,
        "team_name": "Golden State Warriors",
        "age": 37,
        "college": "Davidson",
        "country": "USA",
        "ppg": 26.8,
        "apg": 5.1,
        "rpg": 4.7,
        "spg": 1.2,
        "bpg": 0.2,
        "fg_pct": 0.460,
        "ft_pct": 0.915,
        "threept_pct": 0.424
    },
    {
        "id": 3,
        "name": "Giannis Antetokounmpo",
        "position": "PF",
        "height": "6'11\"",
        "weight": 242,
        "team_id": 15,
        "team_name": "Milwaukee Bucks",
        "age": 30,
        "college": "None",
        "country": "Greece",
        "ppg": 29.7,
        "apg": 6.4,
        "rpg": 11.2,
        "spg": 1.2,
        "bpg": 1.1,
        "fg_pct": 0.576,
        "ft_pct": 0.692,
        "threept_pct": 0.302
    },
    {
        "id": 4,
        "name": "Nikola Jokic",
        "position": "C",
        "height": "6'11\"",
        "weight": 284,
        "team_id": 7,
        "team_name": "Denver Nuggets",
        "age": 30,
        "college": "None",
        "country": "Serbia",
        "ppg": 26.7,
        "apg": 9.2,
        "rpg": 12.1,
        "spg": 1.4,
        "bpg": 0.9,
        "fg_pct": 0.582,
        "ft_pct": 0.825,
        "threept_pct": 0.376
    },
    {
        "id": 5,
        "name": "Luka Doncic",
        "position": "PG",
        "height": "6'7\"",
        "weight": 230,
        "team_id": 13,
        "team_name": "Los Angeles Lakers",
        "age": 26,
        "college": "None",
        "country": "Slovenia",
        "ppg": 32.5,
        "apg": 9.8,
        "rpg": 9.2,
        "spg": 1.4,
        "bpg": 0.5,
        "fg_pct": 0.481,
        "ft_pct": 0.778,
        "threept_pct": 0.367
    }
]


@app.get('/players')
def get_players(position : str = None, name: str = None, team: str = None):
    filtered_players = players 

    if position:
        filtered_players = [player for player in filtered_players
                          if player.get('position').lower() == position.lower()]
    
    if name:
        filtered_players = [player for player in filtered_players
                            if name.lower() in player.get('name').lower()]
    
    if team:
        filtered_players = [player for player in filtered_players
                            if team.lower() in player.get('team_name').lower()]
    
    if not filtered_players and (position or name or team):
        raise HTTPException(status_code=404, detail="No players found matching the criteria")

    return filtered_players

@app.get('/players/{player_id}')
def get_player(player_id: int):
    for player in players:
        if player.get('id') == player_id:
            return player
    raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")

@app.post('/players/create_player')
def create_player(new_player: PlayerModel):
    player_data = new_player.model_dump()
    player_data['id'] = get_next_id()
    players.append(player_data)
    return {"message": "Player created successfully"}

@app.put("/players/update_player/{player_id}")
def update_player(player_id: int, updated_player:PlayerModel):
    for i, player in enumerate(players):
        if player.get('id') == player_id:
            players[i] = updated_player.model_dump()
            return {"message": "Player updated successfully", "player": updated_player}
    raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")

@app.delete("/players/delete_player/{player_id}")
def delete_player(player_id: int):
    for i in range(len(players)):
        if players[i].get('id') == player_id:
            players.pop(i)
            return {"message": "Player deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")
    
def get_next_id():
    if not players:
        return 1
    return max([player.get('id', 0) for player in players]) + 1

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}
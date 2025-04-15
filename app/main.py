from fastapi import FastAPI, HTTPException, Body


app = FastAPI(title="HoopAnalytics API",
              version="0.3")

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
        "country": "USA"
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
        "country": "USA"
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
        "country": "Greece"
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
        "country": "Serbia"
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
        "country": "Slovenia"
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
def create_player(new_player=Body()):
    players.append(new_player)
    return {"message": "Player created successfully"}

@app.put("/players/update_player/{player_id}")
def update_player(player_id: int, updated_player=Body()):
    for i, player in enumerate(players):
        if player.get('id') == player_id:
            players[i] = updated_player
            return {"message": "Player updated successfully", "player": updated_player}
    raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")

@app.delete("/players/delete_player/{player_id}")
def delete_player(player_id: int):
    for i in range(len(players)):
        if players[i].get('id') == player_id:
            players.pop(i)
            return {"message": "Player deleted successfully"}
        raise HTTPException(status_code=404, detail=f"Player with id {player_id} not found")

@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}
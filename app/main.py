from fastapi import FastAPI

app = FastAPI()

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
        "team_id": 6,
        "team_name": "Dallas Mavericks",
        "age": 26,
        "college": "None",
        "country": "Slovenia"
    }
]


@app.get('/players')
def get_players():
    return players

@app.get('/players/{player_id}')
def get_player(player_id: int):
    for player in players:
        if player.get('id') == player_id:
            return player
        
@app.get('/')
def root():
    return {"message": "Welcome to HoopAnalytics API"}
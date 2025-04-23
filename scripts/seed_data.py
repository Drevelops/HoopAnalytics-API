import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Session
from app.models.player import Players, PlayerStats

initial_stats = [
    {"id": 1,
     "player_id": 1,
     "season": "2024-25",
    "ppg": 25.3,
    "apg": 8.1,
    "rpg": 7.4,
    "spg": 1.3,
    "bpg": 0.6,
    "fg_pct": 0.533,
    "ft_pct": 0.756,
    "threept_pct": 0.364},

     {"id": 2,
           "player_id": 2,
     "season": "2024-25",
        "ppg": 26.8,
        "apg": 5.1,
        "rpg": 4.7,
        "spg": 1.2,
        "bpg": 0.2,
        "fg_pct": 0.460,
        "ft_pct": 0.915,
        "threept_pct": 0.424},

        {"id": 3,
              "player_id": 3,
     "season": "2024-25",
        "ppg": 29.7,
        "apg": 6.4,
        "rpg": 11.2,
        "spg": 1.2,
        "bpg": 1.1,
        "fg_pct": 0.576,
        "ft_pct": 0.692,
        "threept_pct": 0.302},

        {"id": 4,
              "player_id": 4,
     "season": "2024-25",
"ppg": 26.7,
        "apg": 9.2,
        "rpg": 12.1,
        "spg": 1.4,
        "bpg": 0.9,
        "fg_pct": 0.582,
        "ft_pct": 0.825,
        "threept_pct": 0.376},

        {"id": 5,
              "player_id": 5,
     "season": "2024-25",
        "ppg": 32.5,
        "apg": 9.8,
        "rpg": 9.2,
        "spg": 1.4,
        "bpg": 0.5,
        "fg_pct": 0.481,
        "ft_pct": 0.778,
        "threept_pct": 0.367}]
# Initial player data
initial_players = [
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

    }
]

def seed_database():
    db = Session()
    try:
        # Check if we already have data
        existing_players = db.query(Players).count()
        existing_stats = db.query(PlayerStats).count()
        if existing_players > 0:
            print("Database already contains data. Skipping seed operation.")
            return
        
        if existing_stats > 0:
            print("Database already contains data. Skipping seed operation.")
            return
        # Add players
        for player_data in initial_players:
            player = Players(**player_data)
            db.add(player)
        #Add stats
        for stats_data in initial_stats:
            stat = PlayerStats(**stats_data)
            db.add(stat)
        db.commit()
        print(f"Added {len(initial_players)} players to the database.")
        print(f"Added {len(initial_stats)} players stats to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Session
from app.models.player import Players, PlayerStats
from app.models.team import Teams

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

nba_teams = [
    {
        "team_name": "Boston Celtics",
        "team_abbreviation": "BOS",
        "city": "Boston",
        "conference": "Eastern",
        "division": "Atlantic",
        "arena_name": "TD Garden",
        "head_coach": "Joe Mazzulla",
        "founded_year": 1946,
        "team_colors": ["Green", "White", "Black", "Gold"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
        "website_url": "https://www.nba.com/celtics/",
        "current_season_wins": 64,
        "current_season_losses": 18,
        "playoff_appearances": 60,
        "championship_titles": 18
    },
    {
        "team_name": "Los Angeles Lakers",
        "team_abbreviation": "LAL",
        "city": "Los Angeles",
        "conference": "Western",
        "division": "Pacific", 
        "arena_name": "Crypto.com Arena",
        "head_coach": "JJ Redick",
        "founded_year": 1947,
        "team_colors": ["Purple", "Gold"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg",
        "website_url": "https://www.nba.com/lakers/",
        "current_season_wins": 47,
        "current_season_losses": 35,
        "playoff_appearances": 63,
        "championship_titles": 17
    },
    {
        "team_name": "Golden State Warriors",
        "team_abbreviation": "GSW",
        "city": "San Francisco",
        "conference": "Western",
        "division": "Pacific",
        "arena_name": "Chase Center",
        "head_coach": "Steve Kerr",
        "founded_year": 1946,
        "team_colors": ["Royal Blue", "Golden Yellow"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg",
        "website_url": "https://www.nba.com/warriors/",
        "current_season_wins": 46,
        "current_season_losses": 36,
        "playoff_appearances": 41,
        "championship_titles": 7
    },
    {
        "team_name": "Miami Heat",
        "team_abbreviation": "MIA",
        "city": "Miami",
        "conference": "Eastern",
        "division": "Southeast",
        "arena_name": "Kaseya Center",
        "head_coach": "Erik Spoelstra",
        "founded_year": 1988,
        "team_colors": ["Red", "Black", "Yellow"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg",
        "website_url": "https://www.nba.com/heat/",
        "current_season_wins": 46,
        "current_season_losses": 36,
        "playoff_appearances": 24,
        "championship_titles": 3
    },
    {
        "team_name": "Milwaukee Bucks",
        "team_abbreviation": "MIL",
        "city": "Milwaukee",
        "conference": "Eastern",
        "division": "Central",
        "arena_name": "Fiserv Forum",
        "head_coach": "Doc Rivers",
        "founded_year": 1968,
        "team_colors": ["Green", "Cream", "Blue"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg",
        "website_url": "https://www.nba.com/bucks/",
        "current_season_wins": 49,
        "current_season_losses": 33,
        "playoff_appearances": 36,
        "championship_titles": 2
    },
    {
        "team_name": "New York Knicks",
        "team_abbreviation": "NYK",
        "city": "New York",
        "conference": "Eastern",
        "division": "Atlantic",
        "arena_name": "Madison Square Garden",
        "head_coach": "Tom Thibodeau",
        "founded_year": 1946,
        "team_colors": ["Blue", "Orange", "Silver", "Black"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg",
        "website_url": "https://www.nba.com/knicks/",
        "current_season_wins": 50,
        "current_season_losses": 32,
        "playoff_appearances": 43,
        "championship_titles": 2
    },
    {
        "team_name": "Denver Nuggets",
        "team_abbreviation": "DEN",
        "city": "Denver",
        "conference": "Western",
        "division": "Northwest",
        "arena_name": "Ball Arena",
        "head_coach": "Michael Malone",
        "founded_year": 1967,
        "team_colors": ["Navy Blue", "Gold", "Red"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg",
        "website_url": "https://www.nba.com/nuggets/",
        "current_season_wins": 57,
        "current_season_losses": 25,
        "playoff_appearances": 31,
        "championship_titles": 1
    },
    {
        "team_name": "Philadelphia 76ers",
        "team_abbreviation": "PHI",
        "city": "Philadelphia",
        "conference": "Eastern",
        "division": "Atlantic",
        "arena_name": "Wells Fargo Center",
        "head_coach": "Nick Nurse",
        "founded_year": 1946,
        "team_colors": ["Blue", "Red", "White", "Grey"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg",
        "website_url": "https://www.nba.com/sixers/",
        "current_season_wins": 47,
        "current_season_losses": 35,
        "playoff_appearances": 52,
        "championship_titles": 3
    },
    {
        "team_name": "Phoenix Suns",
        "team_abbreviation": "PHX",
        "city": "Phoenix",
        "conference": "Western",
        "division": "Pacific",
        "arena_name": "Footprint Center",
        "head_coach": "Mike Budenholzer",
        "founded_year": 1968,
        "team_colors": ["Purple", "Orange", "Black", "Gray"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg",
        "website_url": "https://www.nba.com/suns/",
        "current_season_wins": 49,
        "current_season_losses": 33,
        "playoff_appearances": 32,
        "championship_titles": 0
    },
    {
        "team_name": "Dallas Mavericks",
        "team_abbreviation": "DAL",
        "city": "Dallas",
        "conference": "Western",
        "division": "Southwest",
        "arena_name": "American Airlines Center",
        "head_coach": "Jason Kidd",
        "founded_year": 1980,
        "team_colors": ["Royal Blue", "Navy Blue", "Silver", "Black"],
        "logo_url": "https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg",
        "website_url": "https://www.nba.com/mavericks/",
        "current_season_wins": 50,
        "current_season_losses": 32,
        "playoff_appearances": 24,
        "championship_titles": 1
    }
]

def seed_database():
    db = Session()
    try:
        # Check if we already have data
        existing_players = db.query(Players).count()
        existing_stats = db.query(PlayerStats).count()
        existing_teams = db.query(Teams)
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
        #add teams
        for team_data in nba_teams:
            team = Teams(**team_data)
            db.add(team)

        db.commit()
        print(f"Added {len(initial_players)} players to the database.")
        print(f"Added {len(initial_stats)} players stats to the database.")
        print(f"Added {len(nba_teams)} teams to the database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
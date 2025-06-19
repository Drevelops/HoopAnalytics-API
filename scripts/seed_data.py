import sys
import os
import time
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Session
from app.models.player import Players, PlayerStats
from app.models.team import Teams
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import commonteamroster, playercareerstats, commonplayerinfo

def get_all_nba_teams():
    """Get all 30 NBA teams with complete data"""
    teams_data = []
    nba_teams = teams.get_teams()
    
    # Team conference/division mapping
    team_divisions = {
        'ATL': ('Eastern', 'Southeast'), 'BOS': ('Eastern', 'Atlantic'), 'BKN': ('Eastern', 'Atlantic'),
        'CHA': ('Eastern', 'Southeast'), 'CHI': ('Eastern', 'Central'), 'CLE': ('Eastern', 'Central'),
        'DAL': ('Western', 'Southwest'), 'DEN': ('Western', 'Northwest'), 'DET': ('Eastern', 'Central'),
        'GSW': ('Western', 'Pacific'), 'HOU': ('Western', 'Southwest'), 'IND': ('Eastern', 'Central'),
        'LAC': ('Western', 'Pacific'), 'LAL': ('Western', 'Pacific'), 'MEM': ('Western', 'Southwest'),
        'MIA': ('Eastern', 'Southeast'), 'MIL': ('Eastern', 'Central'), 'MIN': ('Western', 'Northwest'),
        'NOP': ('Western', 'Southwest'), 'NYK': ('Eastern', 'Atlantic'), 'OKC': ('Western', 'Northwest'),
        'ORL': ('Eastern', 'Southeast'), 'PHI': ('Eastern', 'Atlantic'), 'PHX': ('Western', 'Pacific'),
        'POR': ('Western', 'Northwest'), 'SAC': ('Western', 'Pacific'), 'SAS': ('Western', 'Southwest'),
        'TOR': ('Eastern', 'Atlantic'), 'UTA': ('Western', 'Northwest'), 'WAS': ('Eastern', 'Southeast')
    }
    
    # Team additional info
    team_info = {
        'ATL': {'arena': 'State Farm Arena', 'founded': 1968, 'coach': 'Quin Snyder'},
        'BOS': {'arena': 'TD Garden', 'founded': 1946, 'coach': 'Joe Mazzulla'},
        'BKN': {'arena': 'Barclays Center', 'founded': 1976, 'coach': 'Jordi Fernandez'},
        'CHA': {'arena': 'Spectrum Center', 'founded': 1988, 'coach': 'Charles Lee'},
        'CHI': {'arena': 'United Center', 'founded': 1966, 'coach': 'Billy Donovan'},
        'CLE': {'arena': 'Rocket Mortgage FieldHouse', 'founded': 1970, 'coach': 'Kenny Atkinson'},
        'DAL': {'arena': 'American Airlines Center', 'founded': 1980, 'coach': 'Jason Kidd'},
        'DEN': {'arena': 'Ball Arena', 'founded': 1976, 'coach': 'Michael Malone'},
        'DET': {'arena': 'Little Caesars Arena', 'founded': 1941, 'coach': 'J.B. Bickerstaff'},
        'GSW': {'arena': 'Chase Center', 'founded': 1946, 'coach': 'Steve Kerr'},
        'HOU': {'arena': 'Toyota Center', 'founded': 1971, 'coach': 'Ime Udoka'},
        'IND': {'arena': 'Gainbridge Fieldhouse', 'founded': 1967, 'coach': 'Rick Carlisle'},
        'LAC': {'arena': 'Crypto.com Arena', 'founded': 1970, 'coach': 'Tyronn Lue'},
        'LAL': {'arena': 'Crypto.com Arena', 'founded': 1947, 'coach': 'JJ Redick'},
        'MEM': {'arena': 'FedExForum', 'founded': 1995, 'coach': 'Taylor Jenkins'},
        'MIA': {'arena': 'Kaseya Center', 'founded': 1988, 'coach': 'Erik Spoelstra'},
        'MIL': {'arena': 'Fiserv Forum', 'founded': 1968, 'coach': 'Doc Rivers'},
        'MIN': {'arena': 'Target Center', 'founded': 1989, 'coach': 'Chris Finch'},
        'NOP': {'arena': 'Smoothie King Center', 'founded': 2002, 'coach': 'Willie Green'},
        'NYK': {'arena': 'Madison Square Garden', 'founded': 1946, 'coach': 'Tom Thibodeau'},
        'OKC': {'arena': 'Paycom Center', 'founded': 1967, 'coach': 'Mark Daigneault'},
        'ORL': {'arena': 'Kia Center', 'founded': 1989, 'coach': 'Jamahl Mosley'},
        'PHI': {'arena': 'Wells Fargo Center', 'founded': 1946, 'coach': 'Nick Nurse'},
        'PHX': {'arena': 'Footprint Center', 'founded': 1968, 'coach': 'Mike Budenholzer'},
        'POR': {'arena': 'Moda Center', 'founded': 1970, 'coach': 'Chauncey Billups'},
        'SAC': {'arena': 'Golden 1 Center', 'founded': 1945, 'coach': 'Mike Brown'},
        'SAS': {'arena': 'Frost Bank Center', 'founded': 1967, 'coach': 'Gregg Popovich'},
        'TOR': {'arena': 'Scotiabank Arena', 'founded': 1995, 'coach': 'Darko Rajaković'},
        'UTA': {'arena': 'Delta Center', 'founded': 1974, 'coach': 'Will Hardy'},
        'WAS': {'arena': 'Capital One Arena', 'founded': 1961, 'coach': 'Brian Keefe'}
    }
    
    for team in nba_teams:
        abbrev = team['abbreviation']
        conference, division = team_divisions.get(abbrev, ('Eastern', 'Atlantic'))
        info = team_info.get(abbrev, {'arena': f"{team['city']} Arena", 'founded': 1970, 'coach': 'TBD'})
        
        team_data = {
            'id': team['id'],
            'team_name': team['full_name'],
            'team_abbreviation': abbrev,
            'city': team['city'],
            'conference': conference,
            'division': division,
            'arena_name': info['arena'],
            'head_coach': info['coach'],
            'founded_year': info['founded'],
            'team_colors': ['#000000', '#FFFFFF'],  # Default colors
            'logo_url': f"https://cdn.nba.com/logos/nba/{team['id']}/global/L/logo.svg",
            'website_url': f"https://www.nba.com/{abbrev.lower()}/",
            'current_season_wins': 0,  # Will be updated with real data later
            'current_season_losses': 0,
            'playoff_appearances': 0,
            'championship_titles': 0
        }
        teams_data.append(team_data)
    
    return teams_data

def standardize_position(position: str) -> str:
    """Standardize position formats"""
    if not position:
        return 'G'
    
    position = position.upper().strip()
    
    # Map common variations
    position_map = {
        'GUARD': 'G',
        'POINT GUARD': 'PG',
        'SHOOTING GUARD': 'SG',
        'FORWARD': 'F',
        'SMALL FORWARD': 'SF',
        'POWER FORWARD': 'PF',
        'CENTER': 'C',
        'FORWARD-GUARD': 'G-F',
        'GUARD-FORWARD': 'G-F',
        'FORWARD-CENTER': 'F-C',
        'CENTER-FORWARD': 'F-C'
    }
    
    return position_map.get(position, position[:2] if len(position) > 2 else position)

def parse_height(height_str: str) -> str:
    """Convert height to standard format"""
    if not height_str:
        return "6'6\""
    
    height_str = str(height_str).strip()
    
    # Handle formats like "6-11" or "6'11"
    if '-' in height_str:
        parts = height_str.split('-')
        if len(parts) == 2:
            feet, inches = parts[0].strip(), parts[1].strip()
            return f"{feet}'{inches}\""
    
    # Handle formats like "6'11\""
    if "'" in height_str and '"' in height_str:
        return height_str
    
    # Default fallback
    return "6'6\""

def get_current_players():
    """Get current NBA players from multiple teams"""
    players_data = []
    teams = teams.get_teams()
    
    # Get players from top teams to ensure we get stars
    priority_teams = ['LAL', 'GSW', 'BOS', 'MIL', 'DEN', 'PHX', 'MIA', 'NYK', 'DAL', 'PHI']
    
    for team in teams:
        if team['abbreviation'] in priority_teams:
            print(f"Getting players from {team['full_name']}...")
            
            try:
                # Get team roster
                roster = commonteamroster.CommonTeamRoster(team_id=team['id'])
                roster_df = roster.get_data_frames()[0]
                
                for _, player_row in roster_df.iterrows():
                    player_id = player_row['PLAYER_ID']
                    
                    # Skip if we already have this player
                    if any(p['id'] == player_id for p in players_data):
                        continue
                    
                    try:
                        # Get detailed player info
                        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                        info_df = player_info.get_data_frames()[0]
                        
                        if not info_df.empty:
                            player_data_row = info_df.iloc[0]
                            
                            player_data = {
                                'id': int(player_id),
                                'name': str(player_row['PLAYER']),
                                'position': standardize_position(player_row.get('POSITION', 'G')),
                                'height': parse_height(player_data_row.get('HEIGHT', '6-6')),
                                'weight': int(player_data_row.get('WEIGHT', 200)) if player_data_row.get('WEIGHT') else 200,
                                'team_id': int(team['id']),
                                'team_name': team['full_name'],
                                'age': int(player_row.get('AGE', 25)) if player_row.get('AGE') else 25,
                                'college': str(player_data_row.get('SCHOOL', 'Unknown')),
                                'country': str(player_data_row.get('COUNTRY', 'USA'))
                            }
                            
                            players_data.append(player_data)
                            print(f"  ✅ Added {player_data['name']}")
                            
                            # Limit to avoid too much data for demo
                            if len(players_data) >= 50:
                                break
                                
                    except Exception as e:
                        print(f"  ❌ Error getting info for {player_row['PLAYER']}: {e}")
                        continue
                
                # Rate limiting
                time.sleep(2)
                
                if len(players_data) >= 50:
                    break
                    
            except Exception as e:
                print(f"❌ Error getting roster for {team['full_name']}: {e}")
                continue
    
    return players_data

def get_player_season_stats(player_id: int) -> Optional[dict]:
    """Get current season stats for a player"""
    try:
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        season_totals_df = career_stats.get_data_frames()[0]
        
        if not season_totals_df.empty:
            # Get most recent season
            latest_season = season_totals_df.iloc[-1]
            games_played = max(int(latest_season['GP']), 1)
            
            return {
                'player_id': int(player_id),
                'season': '2024-25',
                'ppg': float(round(float(latest_season['PTS']) / games_played, 1)),
                'apg': float(round(float(latest_season['AST']) / games_played, 1)),
                'rpg': float(round(float(latest_season['REB']) / games_played, 1)),
                'spg': float(round(float(latest_season['STL']) / games_played, 1)),
                'bpg': float(round(float(latest_season['BLK']) / games_played, 1)),
                'fg_pct': float(round(float(latest_season['FG_PCT']), 3)) if latest_season['FG_PCT'] else 0.0,
                'ft_pct': float(round(float(latest_season['FT_PCT']), 3)) if latest_season['FT_PCT'] else 0.0,
                'threept_pct': float(round(float(latest_season['FG3_PCT']), 3)) if latest_season['FG3_PCT'] else 0.0
            }
    except Exception as e:
        print(f"Error getting stats for player {player_id}: {e}")
        return None

def populate_nba_data():
    """Populate database with comprehensive NBA data"""
    db = Session()
    
    try:
        # Check if data already exists
        if db.query(Teams).count() > 0:
            print("Database already contains data. Clear it first if you want to repopulate.")
            return
        
        print("🏀 Starting comprehensive NBA data population...")
        
        # 1. Populate all 30 teams
        print("\n📋 Step 1: Adding all NBA teams...")
        teams_data = get_all_nba_teams()
        
        for team_data in teams_data:
            team = Teams(**team_data)
            db.add(team)
        
        db.commit()
        print(f"✅ Added {len(teams_data)} NBA teams")
        
        # 2. Populate current players
        print("\n👥 Step 2: Adding current NBA players...")
        players_data = get_current_players()
        
        for player_data in players_data:
            player = Players(**player_data)
            db.add(player)
        
        db.commit()
        print(f"✅ Added {len(players_data)} NBA players")
        
        # 3. Populate player stats
        print("\n📊 Step 3: Adding player statistics...")
        stats_added = 0
        
        for player_data in players_data[:30]:  # Limit to first 30 to avoid rate limits
            print(f"Getting stats for {player_data['name']}...")
            
            stats_data = get_player_season_stats(player_data['id'])
            if stats_data:
                stat = PlayerStats(**stats_data)
                db.add(stat)
                stats_added += 1
                
                if stats_added % 5 == 0:
                    db.commit()
                    print(f"  📈 Added stats for {stats_added} players...")
            
            # Rate limiting
            time.sleep(1)
        
        db.commit()
        print(f"✅ Added stats for {stats_added} players")
        
        print("\n🎉 NBA data population complete!")
        print(f"📊 Final counts:")
        print(f"  Teams: {db.query(Teams).count()}")
        print(f"  Players: {db.query(Players).count()}")
        print(f"  Player Stats: {db.query(PlayerStats).count()}")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_nba_data()
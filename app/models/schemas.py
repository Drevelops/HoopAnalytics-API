from typing import Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List

class PlayerBase(BaseModel):
    name: str = Field(min_length=3)
    position: str = Field(min_length=1)
    height: str = Field(pattern=r"^[4-8]'(\d{1,2}\")?$")
    weight: int = Field(gt=130, lt=350)
    team_id: int = Field(gt=0, lt=31)
    team_name: str = Field(min_length=3)
    age: int = Field(ge=18, le=50)
    college: str
    country: str = Field(min_length=2)

class PlayerCreate(PlayerBase):
    id: Optional[int] = None
    pass

class PlayerUpdate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}

class PlayerStatsBase(BaseModel):
    player_id: int = Field(gt=0)
    season: str = Field(min_length=4)
    ppg: float = Field(ge=0.0)
    apg: float = Field(ge=0.0)
    rpg: float = Field(ge=0.0)
    spg: float = Field(ge=0.0)
    bpg: float = Field(ge=0.0)
    fg_pct: float = Field(ge=0.0, le=1.0)
    ft_pct: float = Field(ge=0.0, le=1.0)
    threept_pct: float = Field(ge=0.0, le=1.0)

class PlayerStatsCreate(PlayerStatsBase):
    id: Optional[int] = None
    pass

class PlayerStatsUpdate(PlayerStatsBase):
    pass

class PlayerStats(PlayerStatsBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}

class TeamBase(BaseModel):
    id: int = Field(gt=0, lt=31)
    team_name: str = Field(min_length=3)
    team_abbreviation: str = Field(max_length=3)
    city: str = Field(min_length=3)
    conference: str = Field(min_length=3)
    division: str = Field(min_length=3)
    arena_name: str = Field(min_length=3)
    head_coach: str = Field(min_length=3)
    founded_year: int = Field(gt=1923, le=2030)
    team_colors: List[str]
    logo_url: HttpUrl = Field(description="URL to the team's Logo image")
    website_url:  HttpUrl = Field(description="The official website URL of the team",)
    current_season_wins: int = Field(ge=0, le=82)
    current_season_losses: int = Field(ge=0, le=82)
    playoff_appearances: int = Field(ge=0, le=100)
    championship_titles: int = Field(ge=0, le=50)

class TeamCreate(TeamBase):
    id: Optional[int] = None
    pass

class TeamUpdate(TeamBase):
    pass
class Team(TeamBase):
    id:int

    class Config:
        model_config = {"from_attributes": True}
        
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
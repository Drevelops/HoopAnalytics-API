from typing import Optional
from pydantic import BaseModel, Field, EmailStr

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
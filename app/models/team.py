from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

class Teams(Base):
    __tablename__ = 'teams'

    id = Column(BigInteger, primary_key=True, index=True)
    team_name = Column(String)
    team_abbreviation = Column(String)
    city = Column(String)
    conference = Column(String)
    division = Column(String)
    arena_name = Column(String)
    head_coach = Column(String)
    founded_year = Column(Integer)
    team_colors = Column(ARRAY(String), nullable=True)
    logo_url= Column(String)
    website_url= Column(String)
    current_season_wins  = Column(Integer)
    current_season_losses  = Column(Integer)
    playoff_appearances = Column(Integer)
    championship_titles  = Column(Integer)

    


from database import Base
from sqlalchemy import Column, Integer, String, Float

class Players(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    position = Column(String)
    height= Column(String)
    weight = Column(Integer)
    team_id = Column(Integer)
    team_name = Column(String)
    age = Column(Integer)
    college = Column(String)
    country = Column(String)
    ppg = Column(Float)
    apg = Column(Float)
    rpg = Column(Float)
    spg = Column(Float)
    bpg = Column(Float)
    fg_pct = Column(Float)
    ft_pct = Column(Float)
    threept_pct = Column(Float)
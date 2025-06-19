from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

class Players(Base):
    __tablename__ = 'players'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    position = Column(String)
    height= Column(String)
    weight = Column(Integer)
    team_id = Column(Integer)
    team_name = Column(String)
    age = Column(Integer)
    college = Column(String)
    country = Column(String)

    stats = relationship("PlayerStats", back_populates="player")

class PlayerStats(Base):
    __tablename__ = 'player_stats'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    player_id = Column(BigInteger,ForeignKey('players.id'))
    season =  Column(String)

    ppg = Column(Float)
    apg = Column(Float)
    rpg = Column(Float)
    spg = Column(Float)
    bpg = Column(Float)
    fg_pct = Column(Float)
    ft_pct = Column(Float)
    threept_pct = Column(Float)

    player = relationship("Players", back_populates="stats")
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column

Base = declarative_base()

class Hero(Base):

    __tablename__ = "heroes"

    hero = Column(String, primary_key=True)
    faction = Column(String)

    def __init__(self, hero, faction):
        self.hero = hero
        self.faction = faction
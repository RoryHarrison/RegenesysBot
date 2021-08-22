from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer

Base = declarative_base()

class Roster(Base):

    __tablename__ = "rosters"

    id = Column(Integer, primary_key=True)
    user = Column(String)
    hero = Column(String)
    asc = Column(String)
    si = Column(String)
    fi = Column(String)
    en = Column(String)

    def __init__(self, user, hero, asc, si, fi, en):
        self.user = user
        self.hero = hero
        self.asc = asc
        self.si = si
        self.fi = fi
        self.en = en
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer

Base = declarative_base()

class AEWish(Base):

    __tablename__ = "aewish"

    id = Column(Integer, primary_key=True)
    hero = Column(String)
    asc = Column(String)
    si = Column(String)
    fi = Column(String)
    en = Column(String)

    def __init__(self, hero, asc, si, fi, en):
        self.hero = hero
        self.asc = asc
        self.si = si
        self.fi = fi
        self.en = en
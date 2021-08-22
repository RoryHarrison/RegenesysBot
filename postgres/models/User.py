from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    ign = Column(String)

    def __init__(self, id, ign):
        self.id = id
        self.ign = ign
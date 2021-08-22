from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

_db= "postgresql"+os.environ['DATABASE_URL'][8:]

_engine = create_engine(_db)
session = sessionmaker(bind=_engine)()
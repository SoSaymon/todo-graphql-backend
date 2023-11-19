from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.env import getenv

DB_URL = getenv("DB_URL")

engine = create_engine(DB_URL)
conn = engine.connect()
Session = sessionmaker(bind=engine)

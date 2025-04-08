from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite database stored in a local file
DB_URL = "sqlite:///jobs.db"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

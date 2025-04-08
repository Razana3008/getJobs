from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    company = Column(String)
    position = Column(String)
    place = Column(String)
    time_posted = Column(String)
    more_info = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

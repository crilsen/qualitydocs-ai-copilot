"""SQLite engine + session. Path-safe for local and Docker."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Base

db_url = settings.database_url
if db_url.startswith("sqlite"):
    os.makedirs(os.path.dirname(db_url.split("sqlite:///")[-1]) or ".", exist_ok=True)

engine = create_engine(db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

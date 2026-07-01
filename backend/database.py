"""Database setup with SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # test connection health before each use — auto-reconnects on stale SSL
    pool_recycle=280,     # recycle connections every 280s (Neon idles out after ~300s)
    pool_timeout=10,      # give up waiting for a pool slot after 10s
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variables
# Using SQLite as default for local development without Docker
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./floristeria.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        # SQLite specific settings
        connect_args={"check_same_thread": False},  # Required for SQLite
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )
else:
    # Use MySQL settings for production
    engine = create_engine(
        DATABASE_URL,
        # Add pool settings for production use
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
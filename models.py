import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------------------------------------------------------------------
# Database URL handling – supports PostgreSQL (psycopg) and SQLite fallback
# ---------------------------------------------------------------------------
_db_url = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))
if _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg://")

# Add SSL mode for remote PostgreSQL instances (but not for local SQLite)
if not _db_url.startswith("sqlite"):
    if "localhost" not in _db_url and "127.0.0.1" not in _db_url:
        # Preserve existing query params
        if "?" in _db_url:
            if "sslmode=" not in _db_url:
                _db_url += "&sslmode=require"
        else:
            _db_url += "?sslmode=require"

# Engine creation – synchronous (no asyncpg)
engine = create_engine(
    _db_url,
    connect_args={"sslmode": "require"} if not _db_url.startswith("sqlite") else {"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


class Bookmark(Base):
    __tablename__ = "ln_bookmarks"  # prefixed to avoid collisions

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    tags = Column(JSON, nullable=False, default=list)  # list of strings
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

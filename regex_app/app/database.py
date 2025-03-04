"""
Database configuration and session management
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Get database URL from environment or use SQLite by default
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./regex_generator.db")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create session factory
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass

async def create_db_and_tables():
    """Create database tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Dependency for getting database session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
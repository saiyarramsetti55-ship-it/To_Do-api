from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Create SQLAlchemy engine using the database connection URL from .env
engine = create_engine(settings.DATABASE_URL)

# Configure session factory for local sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()

# FastAPI dependency to yield database sessions and ensure they are closed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

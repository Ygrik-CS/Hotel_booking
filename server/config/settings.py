"""Configuration settings for the application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./hotel_booking.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "Hotel Booking System"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

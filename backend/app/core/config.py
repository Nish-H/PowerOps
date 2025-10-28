"""
Configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "ScriptMyIdeas"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Back4app Configuration
    BACK4APP_APPLICATION_ID: str = ""
    BACK4APP_REST_API_KEY: str = ""
    BACK4APP_JAVASCRIPT_KEY: str = ""
    BACK4APP_SERVER_URL: str = "https://parseapi.back4app.com"

    # API Configuration
    API_V1_PREFIX: str = "/api"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]

    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [
        ".py", ".js", ".sh", ".ps1", ".rb", ".go",
        ".java", ".cpp", ".c", ".rs", ".ts", ".html",
        ".css", ".json", ".yaml", ".yml", ".xml"
    ]

    # Script Storage
    SCRIPTS_STORAGE_PATH: str = "./scripts"
    ARTIFACTS_STORAGE_PATH: str = "./artifacts"

    # Versioning
    DEFAULT_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()

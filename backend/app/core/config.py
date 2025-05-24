from typing import List, Any
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Audiobook AI"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str = "us-east-1"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 
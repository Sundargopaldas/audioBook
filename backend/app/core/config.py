from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Caminho para o arquivo .env na pasta backend (um nível acima de core)
# __file__ é o caminho para config.py (backend/app/core/config.py)
# os.path.dirname(__file__) é backend/app/core
# os.path.join(os.path.dirname(__file__), '..', '..', '.env') aponta para backend/.env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "Audiobook AI"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000", "http://localhost:8080", "http://localhost:8001"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AWS
    AWS_ACCESS_KEY_ID: str = "test-key"
    AWS_SECRET_ACCESS_KEY: str = "test-secret"
    AWS_BUCKET_NAME: str = "test-bucket"
    AWS_REGION: str = "us-east-1"
    
    # Google Cloud TTS
    GOOGLE_APPLICATION_CREDENTIALS: str = "google-tts-key.json" # Caminho relativo à raiz do projeto

    class Config:
        # case_sensitive foi removido pois .env já lida com isso
        # env_file = ".env" # Removido, pois estamos carregando explicitamente com dotenv
        pass

settings = Settings()
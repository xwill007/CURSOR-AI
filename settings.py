from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Configuración de la aplicación
    """
    # Configuración general
    APP_NAME: str = "FastAPI Simple"
    APP_DESCRIPTION: str = "Una API simple construida con FastAPI"
    APP_VERSION: str = "0.1.0"
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia de configuración para usar en la aplicación
settings = Settings()

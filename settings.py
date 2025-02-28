from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application settings configuration class.
    
    This class manages all configuration parameters for the application,
    including app metadata, server settings, and CORS configuration.
    """
    # Application configuration
    APP_NAME: str = "Mi API con FastAPI"
    APP_DESCRIPTION: str = "Una API de ejemplo creada con FastAPI"
    APP_VERSION: str = "0.1.0"
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8888
    RELOAD: bool = True
    
    # CORS configuration
    CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        """
        Configuration for the Settings class.
        
        Specifies environment file location and case sensitivity settings.
        """
        env_file = ".env"
        case_sensitive = True

# Create a configuration instance
settings = Settings()

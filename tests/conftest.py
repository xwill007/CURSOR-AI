import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def env_setup():
    """
    Automatically sets up the environment variables for testing.
    This fixture runs automatically before each test.
    """
    load_dotenv()
    # Ensure we have test API keys
    os.environ["GENIUS_API_KEY"] = "test_genius_api_key"
    os.environ["GENIUS_ACCESS_TOKEN"] = "test_genius_access_token"

@pytest.fixture
def test_app():
    """
    Creates a test instance of the FastAPI application.
    
    Returns:
        FastAPI: A configured test instance of the FastAPI application.
    """
    from main import app
    return app 
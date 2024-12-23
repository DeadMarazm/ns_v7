import os
from dotenv import load_dotenv

load_dotenv()


class APIConfig:
    """Конфигурация API."""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set.")
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # OAuth2 settings
    OAUTH2_TOKEN_URL = "/api/v1/auth/token"

    # Database settings (PostgreSQL)
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable must be set.")

    # Debug
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

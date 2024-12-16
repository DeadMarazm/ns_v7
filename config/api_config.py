import os


class APIConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")  # Замените на более безопасный ключ
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # OAuth2 settings
    OAUTH2_TOKEN_URL = "/api/v1/auth/token"

    # Debug
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

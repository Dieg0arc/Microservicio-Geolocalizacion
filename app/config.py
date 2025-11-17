import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "dev")
    DB_URL: str = os.getenv("DB_URL", "")
    API_NAME: str = os.getenv("API_NAME", "easy-parking-geo")
    API_VERSION: str = os.getenv("API_VERSION", "v1")

settings = Settings()

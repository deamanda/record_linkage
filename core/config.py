import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from fastapi_pagination.utils import disable_installed_extensions_check

load_dotenv()

# FastAPI Additional settings
disable_installed_extensions_check()


# Env settings
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
SECRET = os.environ.get("SECRET")


# Base settings
class Settings(BaseSettings):
    api_prefix: str = "/api"
    db_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db_echo: bool = False
    secret: str = f"{SECRET}"


# logger settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="py_log.log",
)
logger = logging.getLogger("Prosept_logs")


settings = Settings()

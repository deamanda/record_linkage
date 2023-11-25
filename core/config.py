from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@host:port/name"


settings = Settings()

settings.db_url

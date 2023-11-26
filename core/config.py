from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"
    db_url: str = "postgresql+asyncpg://user:password@host:port/name"
    db_echo: bool = False


settings = Settings()

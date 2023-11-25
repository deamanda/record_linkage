from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/api_v1"
    db_url: str = (
        "postgresql+asyncpg://{name}:{password}@localhost:5432/{name}"
    )
    db_echo: bool = False


settings = Settings()

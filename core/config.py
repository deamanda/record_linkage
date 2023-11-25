from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = "postgresql+asyncpg://rashid:12061998@localhost:5432/rashid"
    db_echo: bool = False


settings = Settings()

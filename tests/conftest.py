import asyncio
import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
import core.config as conf
from core.config import Settings

TEST_DB = "postgresql+asyncpg://postgres:postgres@localhost:5432/tests"

conf.settings = Settings(db_url=TEST_DB)

from main import app

@pytest.fixture(autouse=True, scope="session")
def run_migrations() -> None:
    from alembic.config import Config
    from alembic import command

    alembic_text_cfg = Config()
    alembic_text_cfg.set_main_option('script_location', 'alembic')
    alembic_text_cfg.set_main_option('sqlalchemy.url', TEST_DB)
    command.upgrade(alembic_text_cfg, 'head')
    yield
    command.downgrade(alembic_text_cfg, 'base')


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app): 
        async with httpx.AsyncClient(
            app=app, base_url='http://test/api/v1/') as test_client:
            yield test_client

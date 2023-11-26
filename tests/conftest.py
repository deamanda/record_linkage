import asyncio
import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from main import app


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

import asyncio
import httpx
import pytest
import pytest_asyncio
import core.config as conf
from core.config import Settings, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME_TEST
from models import Dealer, DealerPrice, Product, User
from models.match import ProductsMapped
from datetime import datetime
from .utils import data_to_model
from fastapi_users.password import PasswordHelper


TEST_DB = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}"
conf.settings = Settings(db_url=TEST_DB)


@pytest.fixture(autouse=True)
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
    """Make the loop session scope to use session async fixtures."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop


@pytest_asyncio.fixture(scope='session', autouse=True)
async def test_client():
    from main import app
    from core.auth import current_user
    user = User(
        email='dummy_user@example.com',
        hashed_password='dummy',
        is_active=True,
        is_verified=True,
        is_superuser=False,
    )
    app.dependency_overrides[current_user] = lambda: user
    async with httpx.AsyncClient(
         app=app, base_url='http://test/api/') as test_client:
        yield test_client


@pytest_asyncio.fixture
async def test_product():
    product = {
         'article': '1',
         'ean_13': 1234567891011,
         'name': 'dye',
         'cost': 1.11,
         'recommended_price': 100,
         'category_id': 1,
         'ozon_name': 'dye ozon',
         'name_1c': 'dye 1c',
         'wb_name': 'dye wb',
         'ozon_article': '1_ozon',
         'wb_article': '1_wb',
         'ym_article': '1_ym',
         'wb_article_td': '1_wb_td',
        }
    return await data_to_model(Product, product)


@pytest_asyncio.fixture
async def test_dealer():
    dealer = {
         'id': 1,
         'name': 'Dealer d',
         }
    return await data_to_model(Dealer, dealer)


@pytest_asyncio.fixture
async def test_dealer_price():
    dealer_price = {
        'id': 1,
        'product_key': '1',
        'price': 100.2,
        'product_url': 'https://example.com/',
        'product_name': 'green dye',
        'date': datetime.now(),
        'dealer_id': 1,
        }
    return await data_to_model(DealerPrice, dealer_price)

@pytest_asyncio.fixture
async def test_user():
    test_password='aaa'
    user_data = {
        'email': 'user@example.com',
        'username': 'user',
        'hashed_password': PasswordHelper().hash(password=test_password),
        'is_active': True,
        'is_verified': True,
        'is_superuser': False,
        }
    return await data_to_model(User, user_data)

@pytest_asyncio.fixture
async def test_products_mapped(test_product, test_dealer_price):
    data = {
        'position': 1,
        'dealerprice_id': 1,
        'product_id': 1,
        'id': 1,
    }
    return await data_to_model(ProductsMapped, data)


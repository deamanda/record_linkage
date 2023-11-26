import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_get_products_ok(test_client):
    response = await test_client.get('products/')

    assert response.status_code == status.HTTP_200_OK


async def test_get_dealers_price_ok(test_client):
    response = await test_client.get('dealers/price/')

    assert response.status_code == status.HTTP_200_OK

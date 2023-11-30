import pytest
from fastapi import status
from pathlib import Path


pytestmark = pytest.mark.asyncio


async def test_post_products(test_client):
    path = Path(Path.cwd(), 'tests/test_files', 'products.csv')
    with open(path, 'rb') as f:
        file = {'file': f}
        response = await test_client.post('products/import-csv/', files=file)
        assert response.status_code == status.HTTP_200_OK


async def test_get_products(test_client):
    response = await test_client.get('products')

    assert response.status_code == status.HTTP_200_OK


async def test_get_dealers_price(test_client):
    response = await test_client.get('dealers/price/')

    assert response.status_code == status.HTTP_200_OK

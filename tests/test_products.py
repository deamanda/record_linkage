import pytest
from fastapi import status
from pathlib import Path




async def test_post_products(test_client):
    path = Path(Path.cwd(), 'tests/test_files', 'products.csv')
    with open(path, 'rb') as f:
        file = {'file': f}
        response = await test_client.post('v1/products/import-csv/', files=file)
        assert response.status_code == status.HTTP_200_OK


async def test_get_products(test_client, test_product):
    response = await test_client.get('v1/products')
    assert response.status_code == status.HTTP_200_OK


async def test_get_product(test_client, test_product):
    response = await test_client.get('v1/products/1/')
    assert response.status_code == status.HTTP_200_OK

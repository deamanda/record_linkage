import pytest
from fastapi import status
from pathlib import Path


pytestmark = pytest.mark.asyncio(scope="module")


async def test_get_dealers(test_client, test_dealer):
    response = await test_client.get('v1/dealers')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['items'][0] == test_dealer


async def test_get_dealers_price(test_client, test_dealer, test_dealer_price):
    response = await test_client.get('v1/dealers/price')
    assert response.status_code == status.HTTP_200_OK


async def test_get_dealers_price_id(
        test_client, test_dealer, test_dealer_price):
    response = await test_client.get('/v1/dealers/price/1/')
    assert response.status_code == status.HTTP_200_OK


async def test_post_dealers_prices(test_client, test_dealer):
    path = Path(Path.cwd(), 'tests/test_files', 'dealerprice.csv')
    with open(path, 'rb') as f:
        file = {'file': f}
        response = await test_client.post(
            'v1/dealers/import-csv/dealerprices', files=file)
        assert response.status_code == status.HTTP_200_OK


async def test_post_dealers(test_client):
    path = Path(Path.cwd(), 'tests/test_files', 'dealer.csv')
    with open(path, 'rb') as f:
        file = {'file': f}
        response = await test_client.post(
            'v1/dealers/import-csv/dealers', files=file)
        assert response.status_code == status.HTTP_200_OK

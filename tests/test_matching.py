import pytest
from fastapi import status
from pathlib import Path


pytestmark = pytest.mark.asyncio


async def test_match_dealer_price(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('/matching/1/')
    assert response.status_code == status.HTTP_200_OK


async def test_match_dealer_price_all(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('/matching/all')
    assert response.status_code == status.HTTP_200_OK


async def test_match_user_me(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('/matching/user/me')
    assert response.status_code == status.HTTP_200_OK


async def test_match_user(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('/matching/user/1')
    assert response.status_code == status.HTTP_200_OK


async def test_match_dealer(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('/matching/dealer/1')
    assert response.status_code == status.HTTP_200_OK


async def test_match_accept(test_client, test_product, test_dealer, test_dealer_price):
    data = {
        'key': 1,
        'product_id': 1
        }
    response = await test_client.post('/matching/accepted', json=data)
    assert response.status_code == status.HTTP_200_OK

async def test_match_not_accept(test_client, test_product, test_dealer, test_dealer_price):
    data = {
        'key': 1,
        'product_id': 1
        }
    response = await test_client.post('/matching/not-accepted', json=data)
    assert response.status_code == status.HTTP_200_OK


async def test_match_not_accept_later(test_client, test_product, test_dealer, test_dealer_price):
    data = {
        'key': 1,
        'product_id': 1
        }
    response = await test_client.post('/matching/accepted-later', json=data)
    assert response.status_code == status.HTTP_200_OK
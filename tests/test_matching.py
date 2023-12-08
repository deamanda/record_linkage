import pytest
from fastapi import status


pytestmark = pytest.mark.asyncio


async def test_match_dealer_price(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('v1/matching/1/')
    assert response.status_code == status.HTTP_200_OK


async def test_match_dealer_price_all(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('v1/matching/all')
    assert response.status_code == status.HTTP_200_OK


async def test_match_user_me(test_client, test_product, test_dealer, test_dealer_price, test_user):
    email = test_user['email']
    headers= {'content-type': 'application/x-www-form-urlencoded'}
    response = await test_client.post('auth/jwt/login', data={'username': email, 'password': 'aaa'}, headers=headers)
    value = response.cookies['Prosept']
    cookies = {'Prosept': value}
    response = await test_client.get('v1/matching/user/me', cookies=cookies)
    assert response.status_code == status.HTTP_200_OK


async def test_match_user(test_client, test_product, test_dealer, test_dealer_price, test_user):
    response = await test_client.get('v1/matching/user/1')
    assert response.status_code == status.HTTP_200_OK


async def test_match_dealer(test_client, test_product, test_dealer, test_dealer_price):
    response = await test_client.get('v1/matching/dealer/1')
    assert response.status_code == status.HTTP_200_OK


async def test_match_accept(test_client, test_product, test_dealer, test_dealer_price, test_user, test_products_mapped):
    data = {
        'key': '1',
        'product_id': '1'
        }
    email = test_user['email']
    headers= {'content-type': 'application/x-www-form-urlencoded'}
    response = await test_client.post('auth/jwt/login', data={'username': email, 'password': 'aaa'}, headers=headers)
    value = response.cookies['Prosept']
    cookies = {'Prosept': value}
    response = await test_client.post('v1/matching/accepted', json=data, cookies=cookies)
    assert response.status_code == status.HTTP_200_OK

async def test_match_not_accept(test_client, test_product, test_dealer, test_dealer_price, test_user):
    data = {
        'key': '1',
        'product_id': 1
        }
    email = test_user['email']
    headers= {'content-type': 'application/x-www-form-urlencoded'}
    response = await test_client.post('auth/jwt/login', data={'username': email, 'password': 'aaa'}, headers=headers)
    value = response.cookies['Prosept']
    cookies = {'Prosept': value}
    response = await test_client.post('v1/matching/not-accepted', json=data, cookies=cookies)
    assert response.status_code == status.HTTP_200_OK



async def test_match_not_accept_later(test_client, test_product, test_dealer, test_dealer_price, test_user):
    data = {
        'key': '1',
        'product_id': 1
        }
    email = test_user['email']
    headers= {'content-type': 'application/x-www-form-urlencoded'}
    response = await test_client.post('auth/jwt/login', data={'username': email, 'password': 'aaa'}, headers=headers)
    value = response.cookies['Prosept']
    cookies = {'Prosept': value}    
    response = await test_client.post('v1/matching/accepted-later', json=data, cookies=cookies)
    assert response.status_code == status.HTTP_200_OK
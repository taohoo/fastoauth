from time import sleep

import pytest
from fastapi import HTTPException

from fastoauth import OAuth2


def test_create_access_token():
    access_token = OAuth2.create_access_token({'user_id': 1, 'user_name': 'foo', 'tenant_id': 23})
    print(f'access_token: {access_token}')


def test_get_current_user():
    # 注意，测试用的SECRET_KEY，请勿用于生产环境
    OAuth2.SECRET_KEY = 'c1cc1a59d0d64ea04c4d62bc738dee398cd78348d18ef57b66ebad5b88e39d66'
    OAuth2.EXPIRE_SECONDS = 60 * 60 * 24 * 365
    # one_year_token = OAuth2.create_access_token({'user_id': 1, 'user_name': 'foo', 'tenant_id': 23})
    # print(f'一年有效期的token: {one_year_token}')
    one_year_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX25hbWUiOiJmb28iLCJ0ZW5hbnRfaWQiOjIzLCJleHAiOjE3NDM5NjE0NTh9.muCjjUvUBtTn418C8plTlZF2eWOQrOLLMLroSDSktR0'
    # 得到之前加密的字典数据
    print(OAuth2.get_token_user(one_year_token))


def test_refresh_token():
    # 注意，测试用的SECRET_KEY，请勿用于生产环境
    OAuth2.SECRET_KEY = 'c1cc1a59d0d64ea04c4d62bc738dee398cd78348d18ef57b66ebad5b88e39d66'
    OAuth2.EXPIRE_SECONDS = 60 * 60 * 24 * 2
    # access_token = OAuth2.create_access_token({'user_id': 1, 'user_name': 'foo', 'tenant_id': 23})
    # print(f'access_token: {access_token}')
    # 之前运行出来的一年有效期的refresh_token
    refresh_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX25hbWUiOiJmb28iLCJ0ZW5hbnRfaWQiOjIzLCJleHAiOjE3NDM5NjE0NTgsIl9yZWZyZXNoIjp0cnVlfQ.aDR-Pfw_m4clsBCt0KBQMZkml-790Jrg-t7eA0ZQkpQ'
    print(OAuth2.refresh_token(refresh_token))


def test_redis():
    # 需要先启动redis
    OAuth2.REDIS_URL = 'redis://localhost:6379/oauth2'
    indata = {'user_id': 1, 'user_name': 'aaaa', 'tenant_id': 23}
    access_token = OAuth2.create_access_token(indata)
    print(f'access_token: {access_token}')
    outdata = OAuth2.get_token_user(access_token.access_token)
    print(outdata)
    assert indata['user_id'] == outdata['user_id']
    # 模拟refresh
    refreshed_token = OAuth2.refresh_token(access_token.refresh_token)
    print(f'refreshed token: {refreshed_token}')
    # 模拟logout，测试access_token是否删除
    with pytest.raises(HTTPException) as ex:
        OAuth2.remove_token(access_token.access_token)
        OAuth2.get_token_user(access_token.access_token)  # 异常
    assert ex.value.status_code == 401
    assert ex.value.detail == 'Could not validate credentials'
    # 模拟logout，测试refresh_token是否删除
    with pytest.raises(HTTPException) as ex:
        OAuth2.remove_token(refreshed_token.access_token)
        OAuth2.refresh_token(refreshed_token.refresh_token)  # 异常
    assert ex.value.status_code == 401
    assert ex.value.detail == 'Could not validate credentials'
    print(f'token removed')


def test_redis_timeout():
    # 需要先启动redis
    OAuth2.REDIS_URL = 'redis://localhost:6379/oauth2'
    OAuth2.EXPIRE_SECONDS = 5
    indata = {'user_id': 1, 'user_name': 'aaaa', 'tenant_id': 23}
    access_token = OAuth2.create_access_token(indata)
    print(f'access_token: {access_token}')
    sleep(OAuth2.EXPIRE_SECONDS + 1)
    with pytest.raises(HTTPException) as ex:
        OAuth2.get_token_user(access_token.access_token)        # 异常
    assert ex.value.status_code == 401
    assert ex.value.detail == 'Could not validate credentials'
    print(f'token expired: {access_token}')


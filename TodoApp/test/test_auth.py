import os
from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException, status

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    
    non_existent_user = authenticate_user('wrong_username', 'testpassword', db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    user_role = 'admin'
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, user_role, expires_delta)
    
    response = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])

    assert response['sub'] == username
    assert response['id'] == user_id
    assert response['role'] == user_role


@pytest.mark.asyncio
async def test_get_user():
    username = 'testuser'
    user_id = 1
    user_role = 'admin'
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, user_role, expires_delta)

    user = await get_current_user(token)
    assert user['username'] == username
    assert user['id'] == user_id
    assert user['user_role'] == user_role

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token = jwt.encode(encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate user"


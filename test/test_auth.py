import pytest
from jose import jwt
from datetime import timedelta
from .utils import *
from fastapi import status
from fastapi.exceptions import HTTPException
from routers.auth import authenticate_user, get_db, SECRET_KEY, ALGORITHM, create_access_token, get_current_user

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):

    db = TestingSessionLocal()

    user = authenticate_user(test_user.username, 'testpassword', db)
    assert user is not None
    assert user.username == test_user.username

    non_existent_user = authenticate_user('non_existent_user', 'testpassword', db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(minutes=20)
    token = create_access_token(username, user_id, role, expires_delta)
    assert token is not None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("username") == username
    assert payload.get("id") == user_id
    assert payload.get("role") == role

# for await operations in pytest package named pytest-asyncio is used (needs to be installed)
@pytest.mark.asyncio
async def test_get_current_user():
    token = create_access_token('testuser', 1, 'user', timedelta(minutes=20))
    user = await get_current_user(token)
    assert user is not None
    assert user.get("username") == 'testuser'
    assert user.get("id") == 1
    assert user.get("role") == 'user'


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    to_encode = {'role': 'user'}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"
    


from .utils import *
from fastapi import status
from routers.users import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_user(test_user):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == "testuser@test.com"
    assert response.json()['first_name'] == 'Test'
    assert response.json()['last_name'] == 'User'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == "1234567890"


def test_user_change_password_success(test_user):
    response = client.put('/users/change-password', json={
        'current_password': 'testpassword',
        'new_password': 'newpassword'
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put('/users/change-password', json={
        'current_password': 'wrongpassword',
        'new_password': 'newpassword'
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'detail': 'Authentication Failed'
    }

def test_user_change_phone_number_success(test_user):
    response = client.put('/users/change-phone-number', json={
        'current_phone_number': '1234567890',
        'new_phone_number': '0987654321'
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_user_change_phone_number_invalid_current_phone_number(test_user):
    response = client.put('/users/change-phone-number', json={
        'current_phone_number': 'wrongphonenumber',
        'new_phone_number': '0987654321'
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        'detail': 'Authentication Failed'
    }

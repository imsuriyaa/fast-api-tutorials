from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user(test_user):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == 'suris@deloitte.com'
    assert response.json()['username'] == 'suriyaa_13'
    assert response.json()['first_name'] == 'Suriyaa'
    assert response.json()['last_name'] == 'S'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '6379440750'

def test_change_password_success(test_user):
    response = client.put('/users/change_password', json={
        'password': 'testpassword',
        'new_password': 'newpassword'
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put('/users/change_password', json={
        'password': 'wrongtestpassword',
        'new_password': 'newpassword'
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}
    
def test_change_phone_number_success(test_user):
    response = client.put('/users/phone_number', json={
        'phone_number': '9999999999'
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_change_phone_number_(test_user):
    response = client.put('/users/phone_number', json={
        'phone_number': '9999999999'
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

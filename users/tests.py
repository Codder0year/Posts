import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient


# Фикстура для создания пользователя
@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        email="testuser@example.com",
        password="password",
        first_name="Test",
        last_name="User",
        username="testuser@example.com"
    )
    return user


# Фикстура для клиента API
@pytest.fixture
def api_client():
    return APIClient()


# Фикстура для аутентифицированного клиента
@pytest.fixture
def authenticated_client(api_client, user):
    login_url = '/users/login/'
    login_data = {
        "email": user.email,
        "password": "password"
    }
    response = api_client.post(login_url, login_data)
    assert response.status_code == status.HTTP_200_OK

    # Получаем токен из ответа
    token = response.data.get("access")
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


# Тест для регистрации нового пользователя
@pytest.mark.django_db
def test_create_user(api_client):
    url = '/users/register/'
    data = {
        "email": "newuser@example.com",
        "password": "P4$$w0rd",
        "first_name": "New",
        "last_name": "User",
        "phone": "1122334455",
        "role": "user",
        "username": "newuser@example.com"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == data["email"]


# Тест для входа пользователя
@pytest.mark.django_db
def test_login_user(api_client, user):
    url = '/users/login/'
    data = {
        "email": user.email,
        "password": "password"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data  # Проверка на наличие токена


# Тест для запроса на сброс пароля
@pytest.mark.django_db
def test_password_reset(api_client, user):
    url = '/users/reset_password/'
    data = {"email": user.email}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK


# Тест для подтверждения сброса пароля
@pytest.mark.django_db
def test_password_reset_confirm(api_client, user):
    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    url = f'/users/reset_password_confirm/{uidb64}/{token}/'
    data = {'new_password': 'newP4$$w0rd'}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK


# Тест для обновления данных пользователя с использованием токена
@pytest.mark.django_db
def test_update_user(authenticated_client, user):
    url = f'/users/{user.pk}/'
    updated_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    response = authenticated_client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == "Updated"

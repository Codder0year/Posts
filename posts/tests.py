import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Ad, Review
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='testuser@example.com',
        password='testpassword123'
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email='anotheruser@example.com',
        password='testpassword456'
    )


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def ad_data(user):
    return {
        'title': 'Test Ad',
        'description': 'Description of the ad',
    }


@pytest.fixture
def ad(user):
    return Ad.objects.create(
        title="Test Ad",
        description="Description of the ad",
        author=user
    )

@pytest.fixture
def review_data(ad, user):
    return {
        'ad': ad,
        'author': user,
        'text': "Great ad!"
    }

# Тесты для объявления (Ad)

@pytest.mark.django_db
def test_ad_list(authenticated_client):
    url = reverse('posts:ad-list')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data  # проверка, что в ответе есть данные


@pytest.mark.django_db
def test_create_ad(authenticated_client, ad_data):
    url = reverse('posts:ad-create')
    response = authenticated_client.post(url, ad_data, format='json')
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == ad_data['title']
    assert response.data['description'] == ad_data['description']


@pytest.mark.django_db
def test_ad_retrieve(authenticated_client, user, ad_data):
    ad = Ad.objects.create(author=user, **ad_data)
    url = reverse('posts:ad-retrieve', args=[ad.pk])
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == ad_data['title']


@pytest.mark.django_db
def test_create_review(authenticated_client, review_data):
    url = reverse('posts:review-create')  # Убедитесь, что URL правильный
    review_data = {
        'ad': review_data['ad'].id,  # Передаем ID объявления, а не объект
        'text': review_data['text'],
    }
    response = authenticated_client.post(url, review_data, format='json')
    assert response.status_code == 201  # Ожидаем, что отзыв будет успешно создан
    assert response.data['text'] == review_data['text']  # Проверяем, что текст отзыва правильный


@pytest.mark.django_db
def test_update_review(authenticated_client, review_data):
    # Создаем отзыв для обновления
    review = Review.objects.create(**review_data)
    url = reverse('posts:review-update', args=[review.pk])

    # Обновляем отзыв
    updated_data = {
        'text': 'Updated comment',
        'ad': review.ad.id  # Обязательно передаем поле ad
    }
    response = authenticated_client.put(url, updated_data, format='json')

    # Печать ошибок сериализатора, если они есть
    if response.status_code == 400:
        print(f"Serializer errors: {response.data}")

    # Проверка, что код ответа 200
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response data: {response.data}"

    # Проверка, что текст был обновлен
    assert response.data['text'] == updated_data['text']

    # Проверка, что в базе данных отзыв действительно обновился
    review.refresh_from_db()
    assert review.text == updated_data['text']


@pytest.mark.django_db
def test_review_list(authenticated_client):
    url = reverse('posts:review-list')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data


@pytest.mark.django_db
def test_update_review(authenticated_client, review_data):
    # Создаем отзыв для обновления
    review = Review.objects.create(**review_data)
    url = reverse('posts:review-update', args=[review.pk])

    # Обновляем отзыв
    updated_data = {
        'text': 'Updated comment',
        'ad': review.ad.id
    }
    response = authenticated_client.put(url, updated_data, format='json')

    # Вывод ошибок сериализатора, если они есть
    if response.status_code == 400:
        print(f"Serializer errors: {response.data}")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}. Response data: {response.data}"

    # Проверка, что текст был обновлен
    assert response.data['text'] == updated_data['text']

    review.refresh_from_db()
    assert review.text == updated_data['text']


@pytest.mark.django_db
def test_delete_review(authenticated_client, review_data):
    review = Review.objects.create(**review_data)
    url = reverse('posts:review-delete', args=[review.pk])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.filter(pk=review.pk).count() == 0


@pytest.mark.django_db
def test_review_permission(user, ad_data, review_data):
    # Создаём объявление с указанием автора
    ad_data['author'] = user  # Указываем автора объявления
    ad = Ad.objects.create(**ad_data)

    # Создаём отзыв
    review_data['ad'] = ad
    review_data['author'] = user  # Указываем автора отзыва
    review = Review.objects.create(**review_data)

    # Тестируем
    assert review.author == user
    assert review.ad == ad

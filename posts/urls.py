from django.urls import path

from .apps import PostsConfig
from .views import (
    AdListAPIView, AdCreateAPIView, AdRetrieveAPIView, AdUpdateAPIView, AdDestroyAPIView,
    ReviewCreateAPIView, ReviewListAPIView, ReviewUpdateAPIView, ReviewDestroyAPIView
)

app_name = PostsConfig.name

urlpatterns = [
    path('ads/', AdListAPIView.as_view(), name='ad-list'),
    path('ads/create/', AdCreateAPIView.as_view(), name='ad-create'),
    path('ads/<int:pk>/', AdRetrieveAPIView.as_view(), name='ad-retrieve'),
    path('ads/<int:pk>/update/', AdUpdateAPIView.as_view(), name='ad-update'),
    path('ads/<int:pk>/delete/', AdDestroyAPIView.as_view(), name='ad-delete'),

    path('reviews/create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/update/', ReviewUpdateAPIView.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete/', ReviewDestroyAPIView.as_view(), name='review-delete'),
]

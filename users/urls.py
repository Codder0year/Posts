from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .apps import UsersConfig
from .views import UserCreateView, UserDetailView, ChangePasswordView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset_password_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

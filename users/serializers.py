from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения и обновления информации о пользователе."""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'image']
        read_only_fields = ['id', 'email', 'role']


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации нового пользователя."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data.get('phone')
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Сериалайзер для смены пароля."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

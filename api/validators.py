from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError


User = get_user_model()


def username_validation(value):
    """Проверка наличия в базе пользователя с данным именем (email)."""
    if User.objects.filter(username=value).exists():
        raise ValidationError(
            f'Пользователь с email <{value}> не найден.')
    return value

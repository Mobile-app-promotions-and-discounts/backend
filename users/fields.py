from django.contrib.auth.password_validation import (
    password_validators_help_texts,
    get_password_validators,
)
from django.conf import settings
from django.forms import CharField


class UserPasswordField(CharField):
    """Поле ввода пароля пользователя."""
    required = True
    help_text = password_validators_help_texts()
    validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)

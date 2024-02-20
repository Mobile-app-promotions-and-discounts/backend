from django.contrib.auth.password_validation import (
    get_default_password_validators, password_validators_help_text_html)
from django.forms import CharField, Form


class CustomPasswordForm(Form):
    """Форма для ввода нового пароля при сбросе пароля."""
    new_password = CharField(
        label='Введите пароль:',
        required=True,
        min_length=8,
        max_length=128,
        help_text=password_validators_help_text_html(),
        validators=[validator.validate for validator in get_default_password_validators()],
    )

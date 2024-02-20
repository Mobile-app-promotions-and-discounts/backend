from django.forms import Form, CharField
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
    get_default_password_validators,
)


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
    uid = CharField(label='UID')
    token = CharField(label='Token')

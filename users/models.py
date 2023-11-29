from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ('phone', 'role', 'foto', 'first_name', 'last_name')
    EMAIL_FIELD = 'username'
    ROLE = [
        ('m', 'marketer'),
        ('s', 'shopper'),
    ]
    username = models.EmailField(
        unique=True,
        verbose_name='email',
    )
    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    role = models.CharField(
        max_length=1,
        choices=ROLE,
        default='s',
        verbose_name='Роль пользователя приложения',
    )
    foto = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True,
        verbose_name='Фото пользователя',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username

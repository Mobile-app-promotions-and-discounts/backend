from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ('phone', 'role', 'photo', 'first_name', 'last_name', 'gender', 'date_of_birth')
    EMAIL_FIELD = 'username'

    class RoleType(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Покупатель'
        SELLER = 'SELLER', 'Продавец'

    class GenderType(models.TextChoices):
        MAN = 'MAN', 'Мужчина'
        WOMAN = 'WOMAN', 'Женщина'

    username = models.EmailField(
        unique=True,
        verbose_name='email',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    role = models.CharField(
        max_length=8,
        choices=RoleType.choices,
        default=RoleType.CUSTOMER,
        verbose_name='Роль пользователя приложения',
    )
    photo = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True,
        verbose_name='Фото пользователя',
    )
    gender = models.CharField(
        max_length=5,
        choices=GenderType.choices,
        blank=True,
        null=True,
        verbose_name='Пол',
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='День рождения',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username

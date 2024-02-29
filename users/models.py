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


class ResetPasswordPin(models.Model):
    """PIN для сброса пароля пользователя."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='reset_pins',
        verbose_name='Пользователь',
        unique=True,
    )
    pin = models.CharField(
        verbose_name='PIN для сброса пароля',
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания PIN'
    )

    class Meta:
        verbose_name = 'PIN для сброса пароля'
        verbose_name_plural = 'PIN для сброса пароля'
        ordering = ['user']

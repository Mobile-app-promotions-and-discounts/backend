from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE = [
        ("m", "marketer"),
        ("s", "shopper"),
    ]
    username = models.EmailField(
        unique=True,
        verbose_name="email",
    )
    phone = models.CharField(max_length=12, verbose_name="Телефон")
    role = models.CharField(
        max_length=1,
        choices=ROLE,
        default="s",
        verbose_name="Роль пользователя приложения",
    )
    # foto = models.ImageField(
    #     upload_to="users/",
    #     verbose_name="Фото пользователя",
    # )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


# Здесь будут пользователи

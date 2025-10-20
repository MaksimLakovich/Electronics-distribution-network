from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import AppUserManager


class AppUser(AbstractUser):
    """Модель представляет пользователя на платформе (авторизация по email)."""

    username = None  # type: ignore
    email = models.EmailField(
        unique=True,
        verbose_name="Почта (username):",
        help_text="Введите email",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # Указываю кастомный менеджер для пользователя без поля username.
    objects = AppUserManager()  # type: ignore

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

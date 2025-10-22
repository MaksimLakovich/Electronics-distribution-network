from django.db import models

from network.services import (calculate_level, validate_level,
                              validate_no_cycles_in_level)
from products.models import Product, TimeStampedModel


class AddressNode(TimeStampedModel):
    """Модель адреса для звеньев сети."""

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Страна:",
        help_text="Укажите страну",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город:",
        help_text="Укажите город",
    )
    street = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Улица:",
        help_text="Укажите улицу",
    )
    house_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Дом:",
        help_text="Укажите номер дома",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        parts = [self.country, self.city, self.street, self.house_number]
        return ", ".join(filter(None, parts)) or "Адрес не указан"

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ["country", "city", "street", "house_number"]


class NetworkNode(TimeStampedModel):
    """Модель представляет звено торговой сети на платформе (наследуется от TimeStampedModel)."""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Название звена сети:",
        help_text="Укажите название звена сети",
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email:",
        help_text="Укажите email контактного лица/офиса",
    )
    address = models.ForeignKey(
        to=AddressNode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="node",
        verbose_name="Адрес:",
        help_text="Укажите адрес",
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="network_nodes",
        verbose_name="Продукт:",
        help_text="Укажите продукт",
    )
    level = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Уровень иерархии:",
        editable=False,  # запрет на ручное редактирование
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
        verbose_name="Поставщик:",
        help_text="Укажите поставщика (предыдущий по иерархии объект сети)",
    )
    debt_to_supplier = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком:",
        help_text="Укажите задолженность перед поставщиком",
    )

    def clean(self):
        """Проверка level иерархии перед сохранением через админку (делегируется сервису)."""
        validate_level(self.parent)

    def save(self, *args, **kwargs):
        """Автоматический расчет level в структуре сети (делегируется сервису)."""
        # Проверяем циклы - validate_no_cycles_in_level выбрасывает ValidationError при проблеме
        validate_no_cycles_in_level(self, self.parent)
        # Проверка уровня, что не больше 2 (0, 1, 2)
        self.clean()
        # Присваиваем level
        self.level = calculate_level(self.parent)
        super().save(*args, **kwargs)

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return self.name

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["name"]

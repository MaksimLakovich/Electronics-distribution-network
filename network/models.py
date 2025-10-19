from django.db import models

from products.models import Product, TimeStampedModel


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
    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="network_nodes",
        verbose_name="Продукт:",
        help_text="Укажите продукт",
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

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return self.name

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["name"]

from django.core.exceptions import ValidationError
from django.db import models

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
        """Проверка уровня иерархии перед сохранением через админку."""
        if self.parent and self.parent.level >= 2:
            raise ValidationError(f"Нельзя создавать звенья в сети выше третьего уровня (0, 1, 2). "
                                  f"Текущий уровень родителя: {self.parent.level}")

    def save(self, *args, **kwargs):
        """Автоматический расчет уровня в структуре сети."""
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        # Сначала запускаю clean(), чтобы админка корректно обработала ошибки при наличии, а потом уже сохраняю
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return self.name

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["name"]

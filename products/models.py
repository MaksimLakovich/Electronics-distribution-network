from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактная базовая модель для дальнейшего создания created_at и updated_at во всех моделях приложения."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания:",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления:",
    )

    class Meta:
        abstract = True


class Product(TimeStampedModel):
    """Модель представляет продукт на платформе (наследуется от TimeStampedModel)."""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Название продукта:",
        help_text="Укажите название продукта",
    )
    model = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Модель продукта:",
        help_text="Укажите модель продукта",
    )
    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата выхода продукта на рынок:",
        help_text="Укажите дату выхода продукта на рынок",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание продукта:",
        help_text="Укажите описание продукта",
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Серийный номер продукта:",
        help_text="Укажите серийный номер продукта",
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Факт наличия продукта:",
        help_text="Зафиксируйте факт наличия продукта",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        verbose_name="Цена продукта (usd):",
        help_text="Укажите цену продукта (usd)",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.name} ({self.model or '—'})"  # Защита, если вдруг model=None у нас в БД

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "-release_date"]  # "-release_date" - чтобы новые продукты по дате были выше

from datetime import date

from rest_framework import serializers


class ReleaseDateValidator:
    """Класс-валидатор для проверки, что дата выхода продукта на рынок не в будущем."""

    def __call__(self, release_date):
        """Метод __call__() делает экземпляр класса вызываемым, как функцию.
        Используется в DRF как валидатор поля сериализатора."""
        if release_date > date.today():
            raise serializers.ValidationError("Дата выхода продукта на рынок не может быть в будущем.")

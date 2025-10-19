from django.core.exceptions import ValidationError


class NetworkLevelValidator:
    """Класс-валидатор для проверки положения в иерархии. Вычисление уровня и запрет создания объекта с level > 2:
        - если parent еще не задан, то будет устанавливаться level = 0;
        - если parent задан, то level + 1, но не больше 2."""

    def __call__(self, parent):
        """Метод __call__() делает экземпляр класса вызываемым, как функцию.
        Используется в DRF как валидатор поля сериализатора."""
        if parent and parent.level >= 2:
            raise ValidationError(
                f"Нельзя создавать звенья в сети выше третьего уровня в иерархии (0, 1, 2). "
                f"Текущий уровень родителя: {parent.level}"
            )

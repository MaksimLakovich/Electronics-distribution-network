from typing import TYPE_CHECKING, Optional

from django.core.exceptions import ValidationError

from network.constants import MAX_LEVEL

if TYPE_CHECKING:
    from .models import NetworkNode


def calculate_level(parent: Optional["NetworkNode"]) -> int:
    """1) Вычисляет уровень для нового/обновляемого звена в структуре сети на основе parent.
    2) Не мутирует parent."""
    if parent:
        # Берем текущий уровень звена и прибавляем 1 - при этом не изменяем сам parent, что важно так как
        # parent - это существующий объект в БД и его нельзя изменять при вычислении уровня дочернего узла
        return int(parent.level) + 1
    else:
        return 0


def validate_level(parent: Optional["NetworkNode"]) -> None:
    """1) Проверяет, что уровень звена не превысит MAX_LEVEL, который задается в константе (network/constants.py).
    2) Выбрасывает django.core.exceptions.ValidationError при нарушении."""
    if parent and parent.level >= MAX_LEVEL:
        raise ValidationError(
            f"Нельзя создавать звенья выше третьего уровня (0..{MAX_LEVEL}). "
            f"Текущий уровень родителя: {parent.level}"
        )


def validate_no_cycles_in_level(instance: Optional["NetworkNode"], parent: Optional["NetworkNode"]) -> None:
    """1) Защищает от циклических ссылок: например, parent не может быть самим instance (нельзя ссылаться
    самому на себя) и не может быть потомком instance.
    2) instance может быть None при создании - тогда проверяем только parent != None."""
    if parent is None or instance is None:
        return

    # Проверка, что parent не может быть самим собой
    if parent.pk == instance.pk:
        raise ValidationError("Звено сети не может быть родителем для самого себя.")

    # Проверка, что parent не находится в поддереве instance, т.е. чтоб не случилось такого
    # кейса "A → B → C → (B)" ведь тут B изначально имел level=1, а значит его позволило бы
    # установить в структуре снова и была бы замкнутая петля - бесконечный цикл.
    current = parent
    while current:
        if current.pk == instance.pk:
            raise ValidationError("Нельзя назначить потомка в качестве родителя (образуется цикл).")
        current = current.parent

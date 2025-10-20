from rest_framework.permissions import BasePermission

from users.constants import EMPLOYEE_GROUP_NAME


class IsActiveEmployee(BasePermission):
    """Проверяет, что пользователь является действующим сотрудником."""

    def has_permission(self, request, view):
        """Возвращает True, если пользователь активен и состоит в группе "EMPLOYEE_GROUP_NAME".
        Используется во views для ограничения доступа к операциям CRUD для продуктов/торговой сети."""
        user = request.user

        # Булево выражение (в виде логической цепочки). Оно возвращает True, только если все условия истинны
        return (
            user
            and user.is_authenticated
            and user.is_active
            and user.groups.filter(name=EMPLOYEE_GROUP_NAME).exists()
        )

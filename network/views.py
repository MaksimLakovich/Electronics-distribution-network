from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from network.models import NetworkNode
from network.serializers import NetworkNodeSerializer
from users.permissions import IsActiveEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для управления звеньями торговой сети на платформе (CRUD)."""

    permission_classes = [IsActiveEmployee]
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer

    filter_backends = (DjangoFilterBackend,)  # Бэкенд для обработки фильтра
    filterset_fields = ("country",)  # Набор полей для фильтрации

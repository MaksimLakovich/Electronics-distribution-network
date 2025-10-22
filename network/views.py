from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets

from network.filters import NetworkNodeFilter
from network.models import AddressNode, NetworkNode
from network.serializers import AddressNodeSerializer, NetworkNodeSerializer
from users.permissions import IsActiveEmployee


class AddressNodeListCreateAPIView(generics.ListCreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для создания адреса и получения всех существующих адресов."""

    permission_classes = [IsActiveEmployee]
    queryset = AddressNode.objects.all()
    serializer_class = AddressNodeSerializer

    filter_backends = (DjangoFilterBackend,)  # Бэкенд для обработки фильтра
    filterset_fields = ("country", "city", "street")  # Набор полей для фильтрации


class AddressNodeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения, обновления и удаления адреса."""

    permission_classes = [IsActiveEmployee]
    queryset = AddressNode.objects.all()
    serializer_class = AddressNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """ViewSet-класс для управления звеньями торговой сети на платформе (CRUD)."""

    permission_classes = [IsActiveEmployee]
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer

    filter_backends = (DjangoFilterBackend,)  # Бэкенд для обработки фильтра
    # Для удобной фильтрации по стране в звеньях создаю alias в модуле network/filters.py для использования
    # удобного параметра ?country= (например, "{{protocol}}{{base_url_api}}/network-node/?country=Корея"),
    # вместо ?address__country=
    filterset_class = NetworkNodeFilter

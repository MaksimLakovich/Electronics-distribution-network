from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import NetworkNode


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели NetworkNode. Описывает, какие поля из NetworkNode будут участвовать в сериализации/десериализации."""

    product = ProductSerializer(read_only=True)

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ["debt_to_supplier"]  # запрет обновления через API

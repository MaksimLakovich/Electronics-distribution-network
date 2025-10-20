from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import AddressNode, NetworkNode
from .validators import NetworkLevelValidator


class AddressNodeSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели AddressNode. Описывает, какие поля из AddressNode будут участвовать в сериализации/десериализации."""

    class Meta:
        model = AddressNode
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели NetworkNode. Описывает, какие поля из NetworkNode будут участвовать в сериализации/десериализации."""

    product = ProductSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        required=False,
        allow_null=True,
        validators=[NetworkLevelValidator()]
    )
    address = serializers.PrimaryKeyRelatedField(
        queryset=AddressNode.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    # Чтобы при GET-запросе возвращался не только ID, а полная информация об адресе
    address_info = AddressNodeSerializer(source="address", read_only=True)

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ["debt_to_supplier"]  # запрет обновления через API

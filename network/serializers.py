from rest_framework import serializers

from products.models import Product
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

    address = serializers.PrimaryKeyRelatedField(
        queryset=AddressNode.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    parent = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        required=False,
        allow_null=True,
        validators=[NetworkLevelValidator()]
    )

    # Чтоб в GET-запросе возвращались не только ID, а полная инфо об адресе (obj Address) и продукте (obj Product)
    address_info = AddressNodeSerializer(source="address", read_only=True)
    product_info = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ["debt_to_supplier"]  # запрет обновления через API

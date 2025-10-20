from rest_framework import serializers

from products.models import Product
from products.validators import ReleaseDateValidator


class ProductSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Product. Описывает то, какие поля модели Product будут участвовать в сериализации/десериализации."""

    release_date = serializers.DateField(
        validators=[ReleaseDateValidator()],
        required=False,
        allow_null=True
    )

    class Meta:
        model = Product
        fields = "__all__"

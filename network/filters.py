import django_filters

from network.models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    """Кастомный FilterSet (фильтр) для модели NetworkNode."""

    # Создаю alias для удобного параметра ?country= в фильтре адреса
    # (например, "{{protocol}}{{base_url_api}}/network-node/?country=Корея"), вместо ?address__country=
    country = django_filters.CharFilter(field_name="address__country", lookup_expr="icontains", label="Страна")

    class Meta:
        model = NetworkNode
        fields = ["country"]  # Теперь можно просто country писать в фильте, а не address__country

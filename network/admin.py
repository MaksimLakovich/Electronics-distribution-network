from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network.models import NetworkNode, AddressNode


@admin.register(AddressNode)
class AddressNodeAdmin(admin.ModelAdmin):
    """Настройка отображения модели AddressNode в админке."""

    list_display = ("id", "country", "city", "street", "house_number", "updated_at")
    search_fields = ("country", "city", "street")
    ordering = ("country", "city")
    readonly_fields = ("created_at", "updated_at")  # чтобы в админке их случайно не изменили


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Настройка отображения модели NetworkNode в админке."""

    # ШАГ 1: Реализация функции для кликабельных ссылок на ForeignKey в админке
    def product_link(self, obj):
        """Создает кликабельную ссылку на связанный продукт."""
        if obj.product:
            url = reverse("admin:products_product_change", args=[obj.product.id])
            return format_html("<a href=\'{url}\'>{name}</a>", url=url, name=obj.product.name)
        return "-"

    product_link.short_description = "Продукт"  # type: ignore
    product_link.admin_order_field = "product"  # type: ignore

    def parent_link(self, obj):
        """Создает кликабельную ссылку на поставщика."""
        if obj.parent:
            url = reverse("admin:network_networknode_change", args=[obj.parent.id])
            return format_html("<a href=\'{url}\'>{name}</a>", url=url, name=obj.parent.name)
        return "-"

    parent_link.short_description = "Поставщик"  # type: ignore
    parent_link.admin_order_field = "parent"  # type: ignore

    def address_link(self, obj):
        """Создает кликабельную ссылку на адрес."""
        if obj.address:
            url = reverse("admin:network_addressnode_change", args=[obj.address.id])
            return format_html("<a href=\'{url}\'>{name}</a>", url=url, name=obj.address)
        return "-"

    address_link.short_description = "Адрес"  # type: ignore
    address_link.admin_order_field = "address"  # type: ignore

    # ШАГ 2: Реализация Admin action для очищения задолженности перед поставщиком у выбранных объектов
    @admin.action(description="Обнулить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt_to_supplier=0)
        self.message_user(
            request,
            f"Задолженность обнулена у {updated_count} выбранных объектов."
        )

    # ШАГ 3: Базовая настройка полей админки
    list_display = (
        "id", "name", "level", "address_link", "product_link", "parent_link", "debt_to_supplier", "updated_at",
    )
    list_filter = ("address__city",)
    search_fields = ("name", "address__city", "product__name",)
    ordering = ("name",)
    readonly_fields = ("level", "created_at", "updated_at")  # чтобы в админке их случайно не изменили
    actions = ["clear_debt"]  # Подключаю Admin action

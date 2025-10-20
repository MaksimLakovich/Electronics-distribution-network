from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения модели Product в админке."""

    list_display = ("id", "name", "model", "release_date", "description", "is_available", "created_at", "updated_at")
    list_filter = ("name", "model", "release_date", "is_available")
    search_fields = ("name", "model", "description", "serial_number")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")  # чтобы в админке их случайно не изменили
    list_editable = ("is_available",)  # чтоб поле было доступно для изменения прямо из списка без захода в продукт

from django.urls import path

from .apps import ProductsConfig
from .views import ProductViewSet

app_name = ProductsConfig.name

urlpatterns = [
    path("product/", ProductViewSet.as_view({"post": "create"}), name="create_product"),
    path("product/<int:pk>/update/", ProductViewSet.as_view({"patch": "partial_update"}), name="update_product"),
    path("product/<int:pk>/delete/", ProductViewSet.as_view({"delete": "destroy"}), name="delete_product"),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import NetworkConfig
from .views import (AddressNodeListCreateAPIView,
                    AddressNodeRetrieveUpdateDestroyAPIView,
                    NetworkNodeViewSet)

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r"network-node", NetworkNodeViewSet, basename="network-node")

urlpatterns = [
    path("", include(router.urls)),
    path("address/", AddressNodeListCreateAPIView.as_view(), name="address-create-list"),
    path(
        "address/<int:pk>/",
        AddressNodeRetrieveUpdateDestroyAPIView.as_view(),
        name="address-retrieve-update-destroy"
    ),
]

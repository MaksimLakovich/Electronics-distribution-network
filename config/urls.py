from typing import cast

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLResolver, include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation for Electronics distribution network",
        contact=openapi.Contact(email="maks_lakovich@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # namespace="users" - это заданное пространство имен, которое есть в users/urls.py с помощью UsersConfig.name
    path("api/", include("users.urls", namespace="users")),
    path("api/", include("products.urls", namespace="products")),
    path("api/", include("network.urls", namespace="network")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += cast(
        list[URLResolver], static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

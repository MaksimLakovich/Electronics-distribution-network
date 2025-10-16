from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .apps import UsersConfig
from .views import AppUserTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path("token/", AppUserTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

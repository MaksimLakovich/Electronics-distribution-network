from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import AppUserTokenObtainPairSerializer


class AppUserTokenObtainPairView(TokenObtainPairView):
    """Класс-контроллер на основе TokenObtainPairView для авторизации по email."""

    serializer_class = AppUserTokenObtainPairSerializer

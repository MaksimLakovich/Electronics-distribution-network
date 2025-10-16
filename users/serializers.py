from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import AppUser


class AppUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный класс-сериализатор токена наследующийся от TokenObtainPairSerializer, позволяющий вход по email."""

    # ВАЖНО! Необходимо указать, что username_field - это будет email.
    # До это мы указывали в модели это "USERNAME_FIELD = "email"" но это настройка Django, например, в админке,
    # логике логина, командах createsuperuser и т.п. Но это не влияет на процессы DRF. Логика сериализатора от
    # DRF Simple JWT НЕ смотрит на USERNAME_FIELD модели автоматически. Поэтому чтобы Simple JWT понял, что логин
    # должен быть по email, а не по username, нужно явно указать это в сериализаторе в username_field
    username_field = AppUser.EMAIL_FIELD

    def validate(self, attrs):
        """Валидация данных при получении токена: проверка существования пользователя и корректности пароля."""
        # ШАГ 1: Получаю email и password из тела запроса
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:  # ШАГ 2: проверяю все ли данные есть
            try:  # ШАГ 3: Ищу пользователя с таким email
                user = AppUser.objects.get(email=email)
            except AppUser.DoesNotExist:
                raise AuthenticationFailed("Пользователь с таким email не найден.")

            if not user.check_password(password):  # ШАГ 4: Проверяю пароль
                raise AuthenticationFailed("Неверный пароль.")

        else:
            raise AuthenticationFailed("Необходимо указать email и пароль.")

        # ШАГ 5: Если все ок, то формирую словарь, чтобы передать в родительский "validate()"
        data = super().validate(
            {
                self.username_field: user.email,  # Ключ "email", значение - email пользователя
                "password": password,
            }
        )
        # ШАГ 6: Добавляю еще данные в ответ (опционально, это полезно для будущего функционала)
        data["email"] = user.email
        data["user_id"] = user.id

        return data

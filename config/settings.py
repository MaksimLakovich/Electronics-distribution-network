import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = True if os.getenv('DEBUG') == 'True' else False

# ALLOWED_HOSTS в Django - это список доменов/IP, с которых разрешено обращаться к приложению.
# 1) Если поставить ['*'], то Django будет принимать запросы с любого домена/IP. Это удобно на этапе тестового
# деплоя (ВМ, Nginx), когда ещё нет точного домена.
# 2) Но в боевой среде так оставлять не рекомендуется - лучше явно указать:
# ALLOWED_HOSTS = ["mydomain.com", "www.mydomain.com", "123.45.67.89"]
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # обязательно, иначе UI не поднимется

    # DRF (Django REST framework) - это библиотека, которая работает со стандартными моделями Django для создания
    # API-сервера для проекта.
    'rest_framework',

    # Для использования расширенной фильтрации с помощью пакета django-filter, после его установки
    'django_filters',

    # API-документация
    'drf_yasg',

    # CORS
    'corsheaders',

    # Приложения проекта
    'users',
    'products',
    'network',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', default='5432'),
    }
}

# База данных для тестов при разворачивании приложения (чтоб не разворачивать сразу postgresql достаточно в начале
# для тестов развернуть sqlite
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.AppUser'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Настройки для CORS и CSRF
# Разрешаем только конкретные origin’ы (более безопасно)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # это типичный адрес фронтенда во время разработки. Чтобы фронт мог в разработке
    # стучаться в наш Django API, нужно разрешить CORS с этого адреса. Если у нас нет фронтенда или он пока
    # не разрабатывается, то http://localhost:3000 - это просто заготовка для будущих разработчиков.
    'https://habits-frontend.example.com',  # продакшн фронтенд
]

# Для работы CSRF с кросс-доменными запросами (POST, PUT, DELETE)
# 1) ЧТО ЭТО?
# Если используется нестандартный порт (например, http://127.0.0.1:8081/admin/ вместо http://127.0.0.1:8000/admin/),
# то Django будет не доверять адресу http://127.0.0.1:8081/admin/, так как источник будет не совпадать с
# доверенным доменом из ALLOWED_HOSTS или CSRF_TRUSTED_ORIGINS и выдаст 403 CSRF verification failed.
# Чтоб исключить ошибку нужно добавить параметр CSRF_TRUSTED_ORIGINS в settings.py и указывать в нем список
# доверенных доменов с портами
# 2) ДОП ПОЯСНЕНИЕ:
# Django проверяет конфигурацию, и в CSRF_TRUSTED_ORIGINS должен быть СПИСОК и без пустых некорректных
# данных, поэтому если не хардкодить тут и выносить в .ENV , то нужно писать код для создания списка без пустых
# значений в конце.
CSRF_TRUSTED_ORIGINS = [
    origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin
]

# Запрещаем доступ для всех подряд (оставляем только из списка выше)
CORS_ALLOW_ALL_ORIGINS = False

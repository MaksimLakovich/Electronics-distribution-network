# Electronics distribution network

# Онлайн-платформа торговой сети электроники

---

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.x-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
![Languages](https://img.shields.io/github/languages/top/MaksimLakovich/Electronics-distribution-network)

![CI](https://img.shields.io/github/actions/workflow/status/MaksimLakovich/Electronics-distribution-network/deploy.yml)
![Build Status](https://img.shields.io/github/actions/workflow/status/MaksimLakovich/Electronics-distribution-network/ci.yml)
![Last commit](https://img.shields.io/github/last-commit/MaksimLakovich/Electronics-distribution-network)
![Open Pull Requests](https://img.shields.io/github/issues-pr/MaksimLakovich/Electronics-distribution-network)
![Stars](https://img.shields.io/github/stars/MaksimLakovich/Electronics-distribution-network)

---

[1. О проекте](#title1)  
[2. Технологии](#title2)   
[3. Структура репозитория](#title3)   
[4. API и функционал](#title4)  
[5. Переменные окружения](#title5)  
[6. Быстрый старт](#title6)  
[7. Документация](#title7)  
[8. Roadmap](#title8)  
[9. Автор](#title9)  

---

## <a id="title1"> 📌 О проекте </a>
*Electronics Distribution Network* - web-платформа для управления иерархией поставщиков и продаж электроники с API и админ-панелью в онлайн-платформе "Торговая сети электроники".  

В приложении реализовано:

1) Модель сети по продаже электроники (иерархическая структура из трех уровней).  
Каждое звено сети ссылается только на одного поставщика оборудования (не обязательно предыдущего по иерархии).
   - завод;
   - розничная сеть;
   - индивидуальный предприниматель.  

2) Вывод в админ-панели созданных объектов.

3) Создан CRUD для модели поставщика.

4) Настроены права доступа к API (только активные сотрудники имеют доступ к API).

---

## <a id="title2"> ⚙️ Технологии </a>
- ***Backend***: Python, Django, Django REST Framework
- ***База данных***: PostgreSQL
- ***Кэширование***: Redis
- ***Инфраструктура***: Docker, Docker Compose, CI/CD через GitHub Actions
- ***Качество кода***: PEP8, pre-commit hooks (flake8, black, mypy), тесты

---

## <a id="title3"> 📂 Структура репозитория </a>
```bash
.
├── .venv                       # Виртуальное окружение poetry
├── config/                     # Django проект и приложения, настройки
├── docs/                       # Дополнительная документация по деталям приложений и проекта в целом
│    ├── app_users_info.md
│    └── ...
├── users/                      # Приложение проекта ("Пользователи")
│    ├── admin.py
│    ├── managers.py                   # create_user(), create_superuser()
│    ├── models.py                     # AppUser(AbstractUser)
│    ├── serializers.py                # AppUserTokenObtainPairSerializer(TokenObtainPairSerializer)
│    ├── views.py                      # AppUserTokenObtainPairView(TokenObtainPairView)
│    ├── urls.py                       # "token/", "token/refresh/"
│    └── ...                           # 
├── products/                   # Приложение проекта ("Продукты")
│    ├── admin.py
│    ├── models.py
│    ├── ...                           # 
│    └── ...                           #
├── network/                    # Приложение проекта ("Торговая сеть")
│    ├── admin.py
│    ├── models.py
│    ├── ...                           # 
│    └── ...                           #
├── .env.example
├── .flake8
├── .gitignore
├── mypy.ini
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## <a id="title4"> 📊 API и функционал </a>

1. Функционал сотрудников на онлайн-платформе:
   - Используется кастомная модель пользователя `AppUser(AbstractUser)`.
   - Авторизация по email.
   - Сотрудники могут работать с функционалом онлайн-платформы:
     - с использованием админ-панели (http://base_url/admin/).
     - с использованием API-интерфейса.


2. Про API-интерфейс (работа через API с использованием Django REST Framework):
   - `API для авторизации сотрудников (users)`: Для API-интерфейса используется ***JSON Web Token*** поэтому необходимо выполнить авторизацию и получить access-токен для работы с API:
   Эндпоинты:
     - http://base_url/api/token/
   - `API для работы с продуктами (products)`: Сотрудники онлайн-платформы *"Торговая сеть электроники"* могут управлять базой ***Продуктов*** (создавать, редактировать, удалять).  
   Эндпоинты:
     - http://base_url/api/product/.../
     - http://base_url/api/product/.../
     - http://base_url/api/product/.../
     - http://base_url/api/product/.../
   - `API для работы с сетью (network)`: Сотрудники онлайн-платформы *"Торговая сеть электроники"* могут управлять структурой ***Торговой сети*** (создавать, редактировать, удалять).  
   Эндпоинты:
     - http://base_url/api/network/.../
     - http://base_url/api/network/.../
     - http://base_url/api/network/.../
     - http://base_url/api/network/.../


3. Документация API (Swagger/ReDoc) будет доступна по адресу:
   - Swagger UI: http://base_url/swagger/
   - Redoc: http://base_url/redoc/

---

## <a id="title5"> 🔑 Переменные окружения </a>

Все конфигурации проекта хранятся в файле `.env`.  
Пример файла доступен в репозитории как `.env.example`.

1. Скопируйте `.env.example` в `.env`:
   ```commandline
   cp .env.example .env
   ```
2. Укажите значения для переменных:

| Переменная | Описание                   | Пример                |
| ------- |----------------------------|-----------------------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django      | `django-insecure-...` |
| `DEBUG` | Режим отладки (True/False) | `True`                |
| `DATABASE_NAME`      | Назване БД в PostgreSQL    | `<some_bd_name>`      |
| `DATABASE_PASSWORD` | Пароль к БД в PostgreSQL   | `<some_bd_password>`  |
| `DATABASE_USER` | Имя пользователя в БД |                       |
| `DATABASE_HOST`           | Хост БД                    |                       |
| `DATABASE_PORT`           | Порт БД                    |                       |

---

## <a id="title6"> 🚀 Быстрый старт (локально) </a>
1. Клонировать репозиторий
    ```commandline
    git clone https://github.com/MaksimLakovich/Electronics-distribution-network.git
    cd Electronics-distribution-network
    ```

2. Установить зависимости:
    ```commandline
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. Настроить переменные окружения:
    ```commandline
    cp .env.example .env
    ```

4. Затем откройте .env и укажите значения для:
    ```commandline
    DJANGO_SECRET_KEY
    DEBUG
    DATABASE_NAME
    DATABASE_USER
    DATABASE_PASSWORD
    DATABASE_HOST
    DATABASE_PORT
    ```

5. Применить миграции и создать суперпользователя:
    ```commandline
    python manage.py migrate
    python manage.py createsuperuser
    ```

6. Запустить локально сервер:
    ```commandline
    python manage.py runserver
    ```

После этого сервис будет доступен локально по адресу: http://127.0.0.1:8000/

---

## <a id="title7"> 📖 Документация </a>

Подробное описание алгоритмов, архитектуры и процесса запуска находится в папке `docs/`.  

Приложение `users`:
- [Users (app_users_info.md)](docs/app_users_info.md): описание модели, админки, кастомной команды для создания новых пользователей, сериализатора, вьюх и путей.

Приложение `products`:
- [Products (app_products_info.md)](docs/app_products_info.md): описание моделей, админок, API, ...

Приложение `network`:
- [Network (app_network_info.md)](docs/app_network_info.md): описание моделей, админок, API, ...

---

## <a id="title8"> 🛣 Roadmap </a>

#### MVP (minimum viable product):
- [x] Приложение users (модели, админки, вью, маршруты)
- [x] AppUserAdmin корректно настроен (удобно создавать пользователей через админку).
- [x] Для работы с API-интерфейсом реализованы JWT endpoints: /token/, /token/refresh/.
- [x] REST_FRAMEWORK настроен с JWTAuthentication.
- [x] README содержит инструкции по созданию сотрудников и использованию токенов.
- [ ] Приложение products (модели, админки, вью, маршруты)
- [ ] Приложение network (модели, админки, вью, маршруты)
- [ ] Документация (оформить инструкцию по запуску сервиса и взаимодействию с проектом в README файле)
- [ ] Подготовлены тесты на аутентификацию и permission(написание базовых тестов для проверки API)

#### Будущие доработки (развитие системы):
- [ ] CI/CD для продакшн-сервера

---

## <a id="title9"> 👨‍💻 Автор </a>
 
**Автор**: Максим Лакович  
GitHub: [MaksimLakovich](https://github.com/MaksimLakovich)  
LinkedIn: [Maksim Lakovich](https://t.me/maksim_lakovich)  
Telegram: [@maksim_lakovich](https://t.me/maksim_lakovich)

---
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
│    └── app_products_info.md
├── users/                      # Приложение проекта ("Пользователи")
│    ├── models.py                     # AppUser(AbstractUser)
│    ├── admin.py                      # AppUserAdmin(UserAdmin)
│    ├── managers.py                   # create_user(), create_superuser()
│    ├── constants.py                  # для хранения различных констант приложения (EMPLOYEE_GROUP_NAME)
│    ├── permissions.py                # IsActiveEmployee(BasePermission)
│    ├── serializers.py                # AppUserTokenObtainPairSerializer(TokenObtainPairSerializer)
│    ├── views.py                      # AppUserTokenObtainPairView(TokenObtainPairView)
│    └── urls.py                       # "token/", "token/refresh/"
├── products/                   # Приложение проекта ("Продукты")
│    ├── models.py                     # TimeStampedModel(models.Model), Product(TimeStampedModel)
│    ├── admin.py                      # ProductAdmin(admin.ModelAdmin)
│    ├── validators.py                 # ReleaseDateValidator
│    ├── serializers.py                # ProductSerializer(serializers.ModelSerializer)
│    ├── views.py                      # ProductViewSet(viewsets.ViewSet) с методами create(), partial_update() и destroy()
│    └── urls.py                       # "product/", "product/<int:pk>/update/", "product/<int:pk>/delete/"
├── network/                    # Приложение проекта ("Торговая сеть")
│    ├── models.py                     # AddressNode(TimeStampedModel), NetworkNode(TimeStampedModel)
│    ├── admin.py                      # AddressNodeAdmin(admin.ModelAdmin), NetworkNodeAdmin(admin.ModelAdmin)
│    ├── constants.py                  # для хранения различных констант приложения (MAX_LEVEL)
│    ├── services.py                   # для сервисных функций по проверке LEVEL и PARENT: calculate_level(), validate_level(), validate_no_cycles_in_level()
│    ├── validators.py                 # NetworkLevelValidator
│    ├── serializers.py                # AddressNodeSerializer(serializers.ModelSerializer), NetworkNodeSerializer(serializers.ModelSerializer)
│    ├── filters.py                    # NetworkNodeFilter(django_filters.FilterSet)
│    ├── views.py                      # Полный CRUD для адресов и звеньев: NetworkNodeViewSet(viewsets.ModelViewSet), AddressNodeListCreateAPIView(generics.ListCreateAPIView) и AddressNodeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView)
│    └── urls.py
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

1. Пользователи (users):
   - Используется кастомная модель пользователя `AppUser(AbstractUser)`.
   - Авторизация по email.
   - JWT-аутентификация (/api/token/, /api/token/refresh/).
   - Сотрудники могут работать с функционалом онлайн-платформы:
     - с использованием админ-панели (http://base_url/admin/).
     - с использованием API-интерфейса.


2. Права доступа:
   - К API продуктов имеют доступ только активные сотрудники, состоящие в группе ***Employees***.
   - Эта группа создается автоматически при миграции ***users/migrations/0002_create_employee_group.py***.
   - Добавление пользователей в группу через админ-панель.


3. Продукты (products):
   - Модель `Product(TimeStampedModel)` с полями: name, model, release_date, description, serial_number, is_available, price
   - Админ-панель с фильтрами и поиском.
   - API-интерфейс (CRUD: create, partial_update, destroy).


4. Торговая сеть (network):
   - Иерархическая структура поставщиков и продавцов (три уровня: завод → розничная сеть → ИП)
   - Каждое звено ссылается на одного родителя (поставщика).
   - Автоматический расчет `level` и запрет создания звена с уровнем > 2.
   - Админка:
       - кликабельные ссылки на продукт и поставщика,
       - фильтр по городу,
       - admin action для обнуления задолженности.
   - API (через DRF):
       - полный CRUD (`network-node/`),
       - фильтрация по стране (`country`),
       - права доступа: только активные сотрудники.


5. Про API-интерфейс (работа сотрудников онлайн-платформы *"Торговая сеть электроники"* через API с использованием Django REST Framework):
   - `API для авторизации сотрудников (users)`: используется ***JSON Web Token*** поэтому необходимо выполнить авторизацию и получить access-токен для работы с API:
   Эндпоинты:
     - http://base_url/api/token/

   - `API для работы с продуктами (products)`: управление базой ***Продуктов*** (создавать, редактировать, удалять).  
   Эндпоинты:
     - http://base_url/api/product/ - создание продукта (POST).
     - http://base_url/api/product/{pk}/update/ - частичное обновление продукта (PATCH).
     - http://base_url/api/product/{pk}/delete/ - удаление продукта (DELETE).

   - `API для работы с сетью (network)`: управление структурой ***Торговой сети*** (полный CRUD).  
   Эндпоинты для звена сети:
     - http://base_url/api/network-node/ - просмотр списка всех звеньев (GET).
     - http://base_url/api/network-node/?country=Japan - просмотр списка всех звеньев с фильтрацией по стране (GET).
     - http://base_url/api/network-node/ - создание звена торговой сети (POST).
     - http://base_url/api/network-node/{pk}/ - просмотр одного звена (GET).
     - http://base_url/api/network-node/{pk}/ - полное обновление звена (PUT).
     - http://base_url/api/network-node/{pk}/ - частичное обновление звена (PATCH).
     - http://base_url/api/network-node/{pk}/ - удаление звена (DELETE).
   Эндпоинты для адресов звеньев сети:
     - http://base_url/api/address/ - просмотр списка всех адресов (GET).
     - http://base_url/api/address/?country=Россия&city=Москва&street=Мира - просмотр списка всех адресов с фильтрацией по 3 полям: страна, город, улица (GET).
     - http://base_url/api/address/ - создание адреса (POST).
     - http://base_url/api/address/{pk}/ - просмотр одного адреса (GET).
     - http://base_url/api/address/{pk}/ - полное обновление адреса (PUT).
     - http://base_url/api/address/{pk}/ - частичное обновление адреса (PATCH).
     - http://base_url/api/address/{pk}/ - удаление адреса (DELETE).


6. Документация API (Swagger/ReDoc) будет доступна по адресу:
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
- [Users (app_users_info.md)](docs/app_users_info.md): описание модели, админки, кастомной команды для создания новых пользователей, констант, прав доступа, сериализатора, вьюх, путей.

Приложение `products`:
- [Products (app_products_info.md)](docs/app_products_info.md): описание моделей, админки, валидатора, сериализатора, вьюх, путей.

Приложение `network`:
- [Network (app_network_info.md)](docs/app_network_info.md): описание моделей, админки, валидатора, фильтрации, сериализатора, вьюх, путей, логики расчета и соблюдения иерархической структуры из трех уровней.

---

## <a id="title8"> 🛣 Roadmap </a>

#### MVP (minimum viable product):
- [x] Разработано приложение users (модели, админки, константы, сериализатор, вью, маршруты)
- [x] Для работы с API-интерфейсом реализованы JWT endpoints: /token/, /token/refresh/
- [x] В "users/migrations/0002_create_employee_group.py" реализовано автоматическое создание группы "Employees" на всех контурах (dev/prom)
- [x] Реализован кастомный класс-permission IsActiveEmployee(), который проверяет, что пользователь является действующим сотрудником (доступ к API)
- [x] Приложение products (модели, админка, валидатор, сериализотор, вью, маршруты)
- [x] Приложение network (модели, админка, валидатор, сериализотор, вью, маршруты)
- [x] Реализован кастомный FilterSet (фильтр) для модели NetworkNode (фильтрация по "Стране")
- [x] "network/services.py" - реализована логика расчета, соблюдения иерархической структуры из трех уровней для звеньев сети и устранение циклических ловушек
- [x] Подключена API-документация
- [x] Оформлен README.md


#### Будущие доработки (развитие системы):
- [ ] Подготовка тестов для веб-сервисов API (использование модуля unittest).
- [ ] Настройка логирования.
- [ ] Добавление кэширование вычисляемого поля level (использование Redis).
- [ ] CI/CD для продакшн-сервера.

---

## <a id="title9"> 👨‍💻 Автор </a>
 
**Автор**: Максим Лакович  
GitHub: [MaksimLakovich](https://github.com/MaksimLakovich)  
LinkedIn: [Maksim Lakovich](https://t.me/maksim_lakovich)  
Telegram: [@maksim_lakovich](https://t.me/maksim_lakovich)

---
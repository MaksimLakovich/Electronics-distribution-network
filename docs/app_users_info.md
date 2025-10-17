# 👤 Пользователи системы

В проекте используется **кастомная модель пользователя** (`AppUser(AbstractUser)`), которая заменяет стандартного `User` в Django.

---

## 🔑 Основные особенности

- Авторизация по **email** (поле `username` удалено).
- Поддержка обычных пользователей и сотрудников (админов) через роли (`is_staff`, `is_superuser`).
- Возможность расширения профиля: имя, фамилия.
- Используется кастомный менеджер `AppUserManager(BaseUserManager)` для создания пользователей и суперпользователей.

---

## 📲 Авторизация

1. Авторизация в админке (http://base_url/admin/) через встроенные механизмы Django.


2. Работа с API-интерфейсом с помощью access-токена в ***JSON Web Token***:
   - http://base_url/api/token/

---

## 🗂 Модель `AppUser(AbstractUser)` в users/models.py

| Поле           | Тип         | Описание                                     |
|----------------| ----------- |----------------------------------------------|
| `id`           | IntegerField  | ID пользователя в БД                         |
| `password`     | CharField  | Кешируется с помощью set_password()          |
| `email`        | EmailField  | Уникальный логин (используется как username) |
| `first_name`   | CharField | Имя пользователя (опционально)               |
| `last_name`    | CharField | Фамилия пользователя (опционально)           |
| `is_active`    | Boolean  | Активен ли пользователь                      |
| `is_staff`     | Boolean  | Может ли войти в админку                     |
| `is_superuser` | Boolean  | Полные права администратора                  |
| `date_joined`  | DateTime | Дата регистрации                             |
| `last_login`   | DateTime | Дата последнего входа                        |

---

## ⚙️ Менеджер `AppUserManager(BaseUserManager)` в users/managers.py

Кастомный менеджер для работы с пользователями.

### Методы
- `create_user(email, password, **extra_fields)` - создание обычного пользователя.
- `create_superuser(email, password, **extra_fields)` - создание суперпользователя.

> ⚠️ Валидация: Email и пароль обязательны.

---

## 🖥 Админка `AppUserAdmin(UserAdmin)` в users/admin.py

В административной панели реализованы:
- Список пользователей с полями: "id", "email", "first_name", "last_name", "is_staff", "is_superuser", "is_active".
- Поиск по: "email", "first_name", "last_name".
- Фильтрация по: "is_staff", "is_superuser", "is_active".
- Редактирование профиля: все, кроме "last_login", "date_joined".
- Управление правами доступа.

---

## 📌 Пример использования

Создание суперпользователя
```commandline
python manage.py createsuperuser
```
# 📦 Продукты

Приложение `products` отвечает за управление продуктами в данной торговой сети электроники.

---

## 🧱 Модель `Product(TimeStampedModel)` в products/models.py

| Поле            | Тип          | Описание                      |
|-----------------|--------------|-------------------------------|
| `name`          | CharField    | Название продукта             |
| `model`         | CharField    | Модель продукта               |
| `release_date`  | DateField    | Дата выхода на рынок          |
| `description`    | TextField     | Описание продукта   |
| `serial_number`    | CharField     | Серийный номер продукта   |
| `is_available`    | BooleanField     | Факт наличия продукта   |
| `price`    | DecimalField     | Цена продукта (usd)   |
| `created_at`    | DateTimeField    | Автоматически при создании    |
| `updated_at`    | DateTimeField    | Автоматически при изменении   |

> Валидация (products/validators.py): `ReleaseDateValidator` не допускает будущих дат.

---

## 🖥 Админка `ProductAdmin(admin.ModelAdmin)` в products/admin.py

В административной панели доступны:
- поля: "id", "name", "model", "release_date", "description", "is_available", "created_at", "updated_at"
- поиск по "name", "model", "description", "serial_number"
- фильтрация по "name", "model", "release_date", "is_available"

---

## 🔒 Права доступа

1. Доступ к API ограничен кастомным классом `users.permissions.IsActiveEmployee`  


2. Условия допуска:
   - Пользователь аутентифицирован
   - is_active=True
   - Состоит в группе "Employees"


3. Группа создается автоматически миграцией:
   - users/migrations/0002_create_employee_group.py

---

## ⚙️ API (через Django REST Framework)

| Метод  | Эндпоинт                        | Описание            | Доступ               |
| ------ | ------------------------------- | ------------------- | -------------------- |
| POST   | `/api/product/`                 | Создание продукта   | 👤 Только сотрудники |
| PUT    | `/api/product/<int:pk>/update/` | Обновление продукта | 👤 Только сотрудники |
| DELETE | `/api/product/<int:pk>/delete/` | Удаление продукта   | 👤 Только сотрудники |


---

## 🧩 ViewSet

`ProductViewSet(viewsets.ViewSet)` реализует методы:
- create() - создание продукта
- partial_update() - частичное обновление
- destroy() - удаление продукта

---

## 🧱 Serializer

`ProductSerializer(serializers.ModelSerializer)` - определяет сериализацию и валидацию модели Product.

---

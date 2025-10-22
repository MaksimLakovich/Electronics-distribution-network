# 🌐 Торговая сеть

Приложение `network` отвечает за управление звеньями торговой сети электроники и построение иерархической структуры поставщиков и продавцов.

---

## 🧱 Модели в network/models.py

### 1. Модель AddressNode(TimeStampedModel)

| Поле               | Тип              | Описание                                                                                                            |
|-------------------|-----------------|---------------------------------------------------------------------------------------------------------------------|
| `country`          | CharField        | Страна                                                                                                              |
| `city`             | CharField        | Город                                                                                                               |
| `street`           | CharField        | Улица                                                                                                               |
| `house_number`     | CharField        | Дом                                                                                                                 |
| `created_at`       | DateTimeField    | Автоматическое время создания                                                                                       |
| `updated_at`       | DateTimeField    | Автоматическое время изменения                                                                                      |

### 2. Модель NetworkNode(TimeStampedModel)

| Поле               | Тип              | Описание                                                                                                            |
|--------------------|-----------------|---------------------------------------------------------------------------------------------------------------------|
| `name`             | CharField        | Название звена сети                                                                                                 |
| `email`            | EmailField       | Email контактного лица/офиса                                                                                        |
| `address`          | ForeignKey       | Адресс, связанный с данным звеном                                                                                   |
| `product`          | ForeignKey       | Продукт, связанный с данным звеном                                                                                  |
| `parent`           | ForeignKey       | Родительское звено (поставщик). Ссылка на другое звено сети                                                         |
| `level`            | PositiveSmallIntegerField | Уровень иерархии (0 - завод, 1 - розничная сеть, 2 - индивидуальный предприниматель). Рассчитывается автоматически. |
| `debt_to_supplier` | DecimalField     | Задолженность перед поставщиком                                                                                     |
| `created_at`       | DateTimeField    | Автоматическое время создания                                                                                       |
| `updated_at`       | DateTimeField    | Автоматическое время изменения                                                                                      |

> ⚠️ 
> 1. Валидация (network/validators.py): `NetworkLevelValidator` не допускает создание звена с уровнем выше 2.  
> 2. В модели метод `save()` рассчитывает: 
>    - **validate_no_cycles_in_level()** - метод проверяет циклы для поля `level`.
>    - **validate_level()** - метод проверяет level иерархии перед созданием объекта.
>    - **calculate_level()** - метод рассчитывает и присваивает level.

---

## 🖥 Админки в network/admin.py

###  1. AddressNodeAdmin(admin.ModelAdmin)

В административной панели доступны:
- поля: "id", "country", "city", "street", "house_number", "updated_at"
- фильтрация по "country", "city", "street"

###  2. Админка NetworkNodeAdmin(admin.ModelAdmin)

В административной панели доступны:
- поля: "id", "name", "level", "address_link", "product_link", "parent_link", "debt_to_supplier", "updated_at"
- фильтрация по "address__city"
- поиск по "name", "address__city", "product__name"
- кликабельные ссылки на продукт и поставщика (`product_link`, `parent_link`, `address_link`)
- **Admin action**: очищение задолженности перед поставщиком для выбранных объектов (`clear_debt`)

> Поля `level`, `created_at`, `updated_at` только для чтения, нельзя редактировать вручную.

---

## 🔒 Права доступа

1. Доступ к API ограничен кастомным классом `users.permissions.IsActiveEmployee`  

2. Условия допуска:
   - Пользователь аутентифицирован
   - is_active=True
   - Состоит в группе "Employees"

3. Группа *Employee* создается автоматически миграцией:
   - users/migrations/0002_create_employee_group.py

---

## ⚙️ API (через Django REST Framework)

| Метод  | Эндпоинт                            | Описание                                                                    | Доступ               |
| ------ | ---------------------------------- |-----------------------------------------------------------------------------| -------------------- |
| GET    | `/api/network-node/`               | Просмотр списка всех звеньев                                                | 👤 Только сотрудники |
| GET    | `/api/network-node/?country=Japan` | Просмотр списка всех звеньев с фильтрацией по стране                        | 👤 Только сотрудники |
| POST   | `/api/network-node/`               | Создание нового звена сети                                                  | 👤 Только сотрудники |
| GET    | `/api/network-node/<int:pk>/`     | Просмотр одного звена                                                       | 👤 Только сотрудники |
| PUT    | `/api/network-node/<int:pk>/`     | Полное обновление звена                                                     | 👤 Только сотрудники |
| PATCH  | `/api/network-node/<int:pk>/`     | Частичное обновление звена                                                  | 👤 Только сотрудники |
| DELETE | `/api/network-node/<int:pk>/`     | Удаление звена                                                              | 👤 Только сотрудники |
| GET    | `/api/address/`               | Просмотр списка всех адресов                                                | 👤 Только сотрудники |
| GET    | `/api/address/?country=Россия&city=Москва&street=Мира` | Просмотр списка всех звеньев с фильтрацией по 3 полям: страна, город, улица | 👤 Только сотрудники |
| POST   | `/api/address/`               | Создание нового адреса                                                      | 👤 Только сотрудники |
| GET    | `/api/address/<int:pk>/`     | Просмотр одного адреса                                                       | 👤 Только сотрудники |
| PUT    | `/api/address/<int:pk>/`     | Полное обновление адреса                                                     | 👤 Только сотрудники |
| PATCH  | `/api/address/<int:pk>/`     | Частичное обновление адреса                                                  | 👤 Только сотрудники |
| DELETE | `/api/address/<int:pk>/`     | Удаление адреса                                                              | 👤 Только сотрудники |

> ⚠️ Для удобной фильтрации по полю **"Страна"** в звеньях торговой сети создан alias (filterset_class = NetworkNodeFilter) 
> в модуле `network/filters.py`, который обеспечивает удобный параметра `?country=` 
> (например, "/api/network-node/?country=Корея"), вместо изначально доступного `?address__country=`

---

## 🧩 ViewSet и Generics

1. ***NetworkNodeViewSet(viewsets.ModelViewSet)*** реализует полный CRUD для модели `NetworkNode`:
   - Автоматический расчет `level` на основе родителя при создании и обновлении.
   - Валидация уровня через `NetworkLevelValidator` (не более 2).
   - Поддержка фильтрации по стране (`country`).

2. ***AddressNodeListCreateAPIView(generics.ListCreateAPIView)*** и ***AddressNodeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView)*** реализуют полный CRUD для модели `AddressNode`:
   - Поддержка фильтрации по стране (`country`, `city`, `street`).

---

## 🧱 Serializer

1. `AddressNodeSerializer(serializers.ModelSerializer)`:
   - Определяет сериализацию и десериализацию всех полей модели.


2. `NetworkNodeSerializer(serializers.ModelSerializer)`:
   - Определяет сериализацию и десериализацию всех полей модели.
   - `parent` проверяется на валидность уровня через `NetworkLevelValidator`.
   - `debt_to_supplier` поле только для чтения (запрет изменения через API).

---

## 📌 Особенности иерархии

- Иерархия строго трех уровней:
  - 0 - завод
  - 1 - розничная сеть
  - 2 - индивидуальный предприниматель
- Уровень (`level`) **не редактируется вручную**.
- Любое звено всегда ссылается на одного родителя (`parent`) - поставщика.
- Запрещено создавать звено с уровнем выше 2 (контролируется и в админке, и через API).

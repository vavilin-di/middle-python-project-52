## Интеграция тестов с manage.py

Проект использует pytest-django в качестве тестового раннера для стандартной команды Django `manage.py test`. Это позволяет запускать тесты как через `pytest`, так и через `python manage.py test`.

### Настройка

1. В `settings.py` добавлен параметр:
   ```python
   TEST_RUNNER = "pytest_django.runner.TestRunner"
   ```

2. Тестовые файлы должны соответствовать шаблону именования pytest (`test_*.py` или `*_tests.py`). Тесты организованы по приложениям:
   - `task_manager/applications/users/tests/` — тесты пользователей
   - `task_manager/applications/statuses/tests.py` — тесты статусов
   - `task_manager/applications/labels/tests.py` — тесты меток
   - `task_manager/applications/tasks/tests/` — тесты задач
   - `task_manager/utilities/tests/` — тесты утилит

3. Общие фикстуры и моки определены в корневом [`conftest.py`](../conftest.py). Фикстуры автоматически доступны всем тестам.

### Запуск тестов

- **Через pytest** (рекомендуется для разработки):
  ```bash
  pytest
  ```
  или для конкретного приложения:
  ```bash
  pytest task_manager/applications/users/tests/
  pytest task_manager/applications/statuses/tests.py
  pytest task_manager/applications/labels/tests.py
  pytest task_manager/applications/tasks/tests/
  ```

- **Через manage.py** (для совместимости с Django-инфраструктурой):
  ```bash
  python manage.py test
  ```
  Можно указать конкретное приложение:
  ```bash
  python manage.py test task_manager.applications.users
  ```

- **С переменной окружения** (для использования SQLite вместо PostgreSQL):
  ```bash
  export USE_SQLITE_FOR_TESTS=1 && python manage.py test
  ```
  В Windows (cmd):
  ```cmd
  set USE_SQLITE_FOR_TESTS=1 && python manage.py test
  ```

### База данных для тестов

В режиме тестов автоматически используется SQLite, даже если в `.env` задан `DATABASE_URL` для PostgreSQL. Это обеспечивается условием в `settings.py`:
```python
if environ.get("DJANGO_ENV") == "test" or environ.get("USE_SQLITE_FOR_TESTS"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

Таким образом, тесты изолированы от production-базы и выполняются быстро.

### Структура тестов

Каждый тестовый класс соответствует одному представлению (View) и покрывает сценарии GET/POST, аутентификацию, проверку прав доступа и редиректы. Всего реализовано **78 тестов**, покрывающих CRUD-операции всех сущностей приложения.

#### Пользователи (13 тестов)

Файлы: [`test_create.py`](../task_manager/applications/users/tests/test_create.py), [`test_list.py`](../task_manager/applications/users/tests/test_list.py), [`test_update.py`](../task_manager/applications/users/tests/test_update.py), [`test_delete.py`](../task_manager/applications/users/tests/test_delete.py)

- **UserCreateView** (3 теста): GET-форма создания, POST с валидными данными, POST с невалидными данными
- **UserListView** (2 теста): список для аутентифицированного и неаутентифицированного пользователя
- **UserUpdateView** (4 теста): GET своего профиля, GET чужого профиля (редирект), POST с валидными/невалидными данными
- **UserDeleteView** (4 теста): GET своего профиля, GET чужого профиля (редирект), POST удаление своего/чужого профиля

#### Статусы (15 тестов)

Файл: [`tests.py`](../task_manager/applications/statuses/tests.py)

- **StatusCreateView** (5 тестов): неаутентифицированный доступ, GET формы, POST создание, POST с пустым именем, POST с дубликатом
- **StatusListView** (3 теста): неаутентифицированный доступ, список с данными, пустой список
- **StatusUpdateView** (4 теста): неаутентифицированный доступ, GET формы, POST обновление, POST с пустым именем, POST с дубликатом
- **StatusDeleteView** (3 теста): неаутентифицированный доступ, GET подтверждения, POST удаление без задач, POST с привязанными задачами (защита от удаления)

#### Метки (15 тестов)

Файл: [`tests.py`](../task_manager/applications/labels/tests.py)

- **LabelCreateView** (5 тестов): неаутентифицированный доступ, GET формы, POST создание, POST с пустым именем, POST с дубликатом
- **LabelListView** (3 теста): неаутентифицированный доступ, список с данными, пустой список
- **LabelUpdateView** (4 теста): неаутентифицированный доступ, GET формы, POST обновление, POST с пустым именем, POST с дубликатом
- **LabelDeleteView** (3 теста): неаутентифицированный доступ, GET подтверждения, POST удаление без задач, POST с привязанными задачами (защита от удаления)

#### Задачи (19 тестов)

Файлы: [`test_create.py`](../task_manager/applications/tasks/tests/test_create.py), [`test_list.py`](../task_manager/applications/tasks/tests/test_list.py), [`test_detail.py`](../task_manager/applications/tasks/tests/test_detail.py), [`test_update.py`](../task_manager/applications/tasks/tests/test_update.py), [`test_delete.py`](../task_manager/applications/tasks/tests/test_delete.py)

- **TaskCreateView** (3 теста): неаутентифицированный доступ, GET формы, POST создание с метками, POST с невалидными данными
- **TaskListView** (5 тестов): неаутентифицированный доступ, список с данными, пустой список, фильтр по статусу, фильтр "только свои задачи"
- **TaskDetailView** (3 теста): неаутентифицированный доступ, детальный просмотр, 404 для несуществующей задачи
- **TaskUpdateView** (3 теста): неаутентифицированный доступ, GET формы, POST обновление, POST с невалидными данными
- **TaskDeleteView** (5 тестов): неаутентифицированный доступ, GET автора, GET чужого пользователя, POST автора, POST чужого пользователя

#### Утилиты (16 тестов)

Файл: [`test_aggregates.py`](../task_manager/utilities/tests/test_aggregates.py)

- **ArrayAggregation (SQLite)** (6 тестов): проверка подкласса Aggregate, SQL-функции JSON_GROUP_ARRAY, output_field, шаблона, интеграционный тест с annotate
- **ArrayAggregation (PostgreSQL)** (4 теста): проверка через mock, что при vendor=postgresql используется ArrayAgg, и проверка ошибок для неподдерживаемых vendor

### Общие фикстуры

Для повторного использования кода в корневом [`conftest.py`](../conftest.py) определены фикстуры:
- `client` – тестовый клиент Django
- `user_data` – словарь с валидными данными пользователя
- `create_user` – создает и возвращает экземпляр пользователя
- `authenticated_client` – клиент, аутентифицированный под созданным пользователем

Локальные фикстуры для каждого приложения определены в соответствующих `conftest.py` или в самом файле тестов.

Тесты помечены декоратором `@pytest.mark.django_db` для доступа к базе данных.

### Проверка flash-сообщений

Во всех тестах, где представление отправляет flash-сообщение (через `SuccessMessageMixin`, `MessageSendingLoginRequiredMixin` или `MessageSendingUserPassesTestMixin`), выполняется проверка наличия и содержимого сообщения.

Для этого используется `follow=True` в запросах, чтобы перейти по редиректу, и `django.contrib.messages.get_messages()` для получения списка сообщений:

```python
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _

response = authenticated_client.post(url, data=data, follow=True)

assert response.status_code == HTTPStatus.OK
assert response.redirect_chain == [(reverse("statuses:list"), HTTPStatus.FOUND)]

messages = list(get_messages(response.wsgi_request))
assert len(messages) == 1
assert str(messages[0]) == str(_("Статус успешно создан"))
```

**Правила проверки flash-сообщений:**

1. Для запросов, завершающихся редиректом, используется `follow=True`, чтобы получить финальный ответ после редиректа.
2. Проверяется `response.redirect_chain` — список кортежей `(url, status_code)`, где `status_code` указывается через константу `HTTPStatus.FOUND`.
3. Сообщения извлекаются через `get_messages(response.wsgi_request)` и преобразуются в список.
4. Сравнение текста сообщения выполняется через `str(messages[0]) == str(_("..."))`, где `_` — `gettext_lazy`, что гарантирует корректное сравнение с учётом локализации.
5. Проверяется точное количество сообщений (`len(messages) == 1`), чтобы убедиться, что не отправляются лишние сообщения.
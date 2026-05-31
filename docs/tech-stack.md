# Стек технологий

| Компонент          | Технология                              |
| ------------------ | --------------------------------------- |
| Backend            | Python 3.14, Django 5.2                 |
| База данных        | PostgreSQL (production), SQLite (тесты) |
| ASGI-сервер        | Uvicorn                                 |
| Фронтенд           | Django Templates, Bootstrap 5           |
| Иконки             | Bootstrap Icons                         |
| Фильтрация         | django-filter                           |
| Локализация        | GNU gettext                             |
| Пакетный менеджер  | UV                                      |
| Тестирование       | pytest, pytest-django, pytest-xdist     |
| Статический анализ | Ruff, Black, mypy, djlint               |
| CI/CD              | GitHub Actions, Render.com              |

## Зависимости

### Production

| Пакет                  | Назначение                    |
| ---------------------- | ----------------------------- |
| Django                 | Веб-фреймворк                 |
| dj-database-url        | Парсинг DATABASE_URL          |
| django-bootstrap5      | Интеграция Bootstrap 5        |
| django-bootstrap-icons | Иконки Bootstrap              |
| django-filter          | Фильтрация queryset'ов        |
| psycopg2               | Адаптер PostgreSQL для Python |
| python-dotenv          | Загрузка переменных из .env   |
| uvicorn                | ASGI-сервер                   |

### Dev

| Пакет               | Назначение                    |
| ------------------- | ----------------------------- |
| black               | Форматирование кода           |
| django-stubs        | type hints для Django         |
| djlint              | Линтер HTML-шаблонов          |
| mypy                | Статическая типизация         |
| pytest              | Тестовый раннер               |
| pytest-django       | Интеграция pytest с Django    |
| pytest-xdist        | Параллельный запуск тестов    |
| ruff                | Линтер и сортировщик импортов |
| types-django-filter | type hints для django-filter  |
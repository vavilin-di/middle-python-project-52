# Быстрый старт

## Требования

- Python 3.14+
- [UV](https://docs.astral.sh/uv/) — пакетный менеджер

## Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/vavilin-di/middle-python-project-52.git
cd middle-python-project-52

# Установить зависимости
make install

# Выполнить миграции
make migrate

# Запустить сервер разработки
make dev
```

Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).

## Переменные окружения

Создайте файл `.env` в корне проекта (опционально):

```env
DATABASE_URL=postgres://user:password@host:port/dbname
SECRET_KEY=your-secret-key
DEBUG=True
```

Если `DATABASE_URL` не задан, используется SQLite.

## Production-сборка

```bash
make build
make start
```

Скрипт сборки (`build.sh`) автоматически устанавливает UV, зависимости, собирает статику и применяет миграции.
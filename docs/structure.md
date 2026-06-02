# Структура проекта

```
task_manager/
├── applications/
│   ├── index/              # Главная страница, вход/выход
│   │   ├── views.py        #   index, CustomLoginView, CustomLogoutView
│   │   └── apps.py
│   ├── users/              # Управление пользователями
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── statuses/           # Управление статусами
│   │   ├── models.py       #   Status
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── tests.py
│   ├── labels/             # Управление метками
│   │   ├── models.py       #   Label
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── tests.py
│   └── tasks/              # Управление задачами
│       ├── models.py       #   Task
│       ├── forms.py
│       ├── urls.py
│       └── views/
│           ├── list.py
│           ├── create.py
│           ├── update.py
│           └── delete.py
├── locale/
│   ├── en/              # Английский перевод (django.po)
│   └── ru/              # Русский перевод (django.po)
├── templates/
│   ├── common/             # Базовые шаблоны (header, footer, head)
│   ├── index.html
│   ├── login.html
│   ├── users/
│   ├── statuses/
│   ├── labels/
│   └── tasks/
├── utilities/
│   ├── aggregates.py       # Кастомные агрегатные функции
│   ├── annotations.py      # Аннотации для queryset'ов
│   ├── views_mixins.py     # Переиспользуемые примеси для View
│   └── tests/
├── settings.py             # Конфигурация Django
├── urls.py                 # Маршрутизация
├── wsgi.py                 # WSGI-точка входа
└── asgi.py                 # ASGI-точка входа
```

## Ключевые файлы

| Файл             | Назначение                          |
| ---------------- | ----------------------------------- |
| `pyproject.toml` | Конфигурация проекта и зависимостей |
| `manage.py`      | Точка входа Django CLI              |
| `Makefile`       | Автоматизация команд                |
| `build.sh`       | Скрипт сборки для Render.com        |
| `conftest.py`    | Общие фикстуры pytest               |
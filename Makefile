PORT ?= 8000

install:
	uv sync
	make collectstatic
	make migrate
	make compilemessages

build:
	./build.sh

collectstatic:
	uv run manage.py collectstatic

migrate:
	uv run manage.py migrate

compilemessages:
	uv run manage.py compilemessages

test:
	uv run manage.py test

code-quality:
	uv run black --check --diff .
	uv run ruff check .
	uv run djlint --check task_manager/templates/
	uv run mypy .

dev:
	uv run manage.py runserver

start:
	uv run uvicorn --host 127.0.0.1 --port $(PORT) task_manager.asgi:application

render-start:
	uv run uvicorn --host 0.0.0.0 --port $(PORT) task_manager.asgi:application

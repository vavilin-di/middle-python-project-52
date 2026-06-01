PORT ?= 8000

install:
	uv sync

build:
	./build.sh

collectstatic:
	uv run manage.py collectstatic

migrate:
	uv run manage.py migrate

dev:
	uv run manage.py runserver

test:
	uv run manage.py test

start:
	uv run uvicorn --host 0.0.0.0 --port $(PORT) task_manager.asgi:application

render-start:
	uvicorn --host 0.0.0.0 --port $(PORT) task_manager.asgi:application

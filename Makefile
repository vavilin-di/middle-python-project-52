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

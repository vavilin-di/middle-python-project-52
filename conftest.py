"""
Общие фикстуры для тестов проекта.
"""

import os
import secrets

# Устанавливаем переменную окружения для использования SQLite в тестах
os.environ.setdefault("USE_SQLITE_FOR_TESTS", "1")

import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def client() -> Client:
    """Фикстура для Django тестового клиента."""
    return Client()


@pytest.fixture
def existing_password() -> str:
    """Генерирует пароль для тестов."""
    return secrets.token_urlsafe(16)


@pytest.fixture
def other_user_password() -> str:
    """Генерирует пароль для тестов."""
    return secrets.token_urlsafe(16)


@pytest.fixture
def user_data() -> dict:
    """Данные для создания пользователя."""
    return {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password1": "TestPassword123",
        "password2": "TestPassword123",
    }


@pytest.fixture
def create_user(db, existing_password: str) -> User:
    """Создает и возвращает пользователя в базе данных."""
    return User.objects.create_user(
        username="existinguser",
        first_name="Existing",
        last_name="User",
        password=existing_password,
    )


@pytest.fixture
def authenticated_client(client: Client, create_user: User) -> Client:
    """Возвращает аутентифицированный клиент."""
    client.force_login(create_user)
    return client

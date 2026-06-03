"""
Тесты для форм приложения users.

Модуль task_manager.applications.users.forms содержит:
- CustomUserCreateForm — форма регистрации пользователя
- CustomUserUpdateForm — форма обновления пользователя
"""

from __future__ import annotations

from task_manager.applications.users.forms import CustomUserCreateForm, CustomUserUpdateForm


class TestCustomUserCreateForm:
    """Тесты для CustomUserCreateForm."""

    def test_valid_form_creates_user(self, db, existing_password: str):
        """Валидная форма создаёт пользователя."""
        form = CustomUserCreateForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "password1": existing_password,
                "password2": existing_password,
            }
        )
        assert form.is_valid()
        user = form.save()
        assert user.username == "johndoe"
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_invalid_form_missing_fields(self):
        """Форма с пустыми данными невалидна."""
        form = CustomUserCreateForm(data={})
        assert not form.is_valid()
        assert "username" in form.errors
        assert "password1" in form.errors
        assert "password2" in form.errors

    def test_form_has_first_name_and_last_name_fields(self):
        """Форма содержит поля first_name и last_name."""
        form = CustomUserCreateForm()
        assert "first_name" in form.fields
        assert "last_name" in form.fields


class TestCustomUserUpdateForm:
    """Тесты для CustomUserUpdateForm."""

    def test_clean_username_returns_username(self, db, existing_password: str):
        """clean_username возвращает имя пользователя без изменений."""
        form = CustomUserUpdateForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "newuser",
                "password1": existing_password,
                "password2": existing_password,
            }
        )
        assert form.is_valid()
        assert form.clean_username() == "newuser"

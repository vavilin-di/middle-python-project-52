"""
Тесты для форм приложения tasks.

Модуль task_manager.applications.tasks.forms содержит:
- _UserFullNameModelChoiceField — кастомное поле выбора пользователя
- _get_executor_field() — фабричная функция для поля executor
- TaskCreateForm — форма создания задачи
- TaskUpdateForm — форма обновления задачи
"""

from __future__ import annotations

from django.contrib.auth.models import User

from task_manager.applications.tasks.forms import (
    TaskCreateForm,
    TaskUpdateForm,
    _get_executor_field,
    _UserFullNameModelChoiceField,
)
from task_manager.applications.tasks.models import Task


class TestUserFullNameModelChoiceField:
    """Тесты для _UserFullNameModelChoiceField."""

    def test_label_from_instance_returns_full_name(self, db, existing_password: str):
        """label_from_instance возвращает full_name пользователя."""
        User.objects.create_user(
            username="testuser",
            password=existing_password,
            first_name="John",
            last_name="Doe",
        )
        field = _get_executor_field()
        user = field.queryset.first()  # type: ignore[union-attr]
        assert user is not None
        assert field.label_from_instance(user) == "John Doe"

    def test_label_from_instance_returns_space_when_no_name_parts(self, db, existing_password: str):
        """label_from_instance возвращает пробел, если first_name и last_name пусты."""
        User.objects.create_user(
            username="testuser",
            password=existing_password,
        )
        field = _get_executor_field()
        user = field.queryset.first()  # type: ignore[union-attr]
        assert user is not None
        assert field.label_from_instance(user) == " "


class TestGetExecutorField:
    """Тесты для _get_executor_field."""

    def test_returns_user_full_name_model_choice_field(self, db):
        """_get_executor_field возвращает _UserFullNameModelChoiceField."""
        field = _get_executor_field()
        assert isinstance(field, _UserFullNameModelChoiceField)

    def test_field_is_not_required(self, db):
        """Поле executor не обязательное."""
        field = _get_executor_field()
        assert field.required is False

    def test_field_queryset_has_full_name_annotation(self, db, existing_password: str):
        """Queryset поля содержит аннотацию full_name."""
        User.objects.create_user(
            username="testuser",
            password=existing_password,
            first_name="John",
            last_name="Doe",
        )
        field = _get_executor_field()
        user = field.queryset.first()  # type: ignore[union-attr]
        assert user is not None
        assert hasattr(user, "full_name")
        assert user.full_name == "John Doe"


class TestTaskCreateForm:
    """Тесты для TaskCreateForm."""

    def test_form_has_all_fields(self):
        """Форма содержит все необходимые поля."""
        form = TaskCreateForm()
        assert "name" in form.fields
        assert "description" in form.fields
        assert "status" in form.fields
        assert "executor" in form.fields
        assert "labels" in form.fields

    def test_executor_field_is_user_full_name_model_choice_field(self):
        """Поле executor является _UserFullNameModelChoiceField."""
        form = TaskCreateForm()
        assert isinstance(form.fields["executor"], _UserFullNameModelChoiceField)

    def test_executor_field_not_required(self):
        """Поле executor не обязательное."""
        form = TaskCreateForm()
        assert form.fields["executor"].required is False

    def test_form_meta_model(self):
        """Форма связана с моделью Task."""
        assert TaskCreateForm._meta.model is Task


class TestTaskUpdateForm:
    """Тесты для TaskUpdateForm."""

    def test_form_has_all_fields(self):
        """Форма содержит все необходимые поля."""
        form = TaskUpdateForm()
        assert "name" in form.fields
        assert "description" in form.fields
        assert "status" in form.fields
        assert "executor" in form.fields
        assert "labels" in form.fields

    def test_executor_field_is_user_full_name_model_choice_field(self):
        """Поле executor является _UserFullNameModelChoiceField."""
        form = TaskUpdateForm()
        assert isinstance(form.fields["executor"], _UserFullNameModelChoiceField)

    def test_executor_field_not_required(self):
        """Поле executor не обязательное."""
        form = TaskUpdateForm()
        assert form.fields["executor"].required is False

    def test_form_meta_model(self):
        """Форма связана с моделью Task."""
        assert TaskUpdateForm._meta.model is Task

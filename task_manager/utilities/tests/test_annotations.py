"""
Тесты для модуля annotations.py.

Модуль task_manager.utilities.annotations содержит вспомогательные функции
для создания аннотаций Django ORM.
"""

from __future__ import annotations

from django.db.models.functions import Concat

from task_manager.utilities.annotations import get_user_full_name_annotation


class TestGetUserFullNameAnnotation:
    """Тесты для функции get_user_full_name_annotation."""

    def test_returns_dict(self):
        """Функция должна возвращать словарь."""
        result = get_user_full_name_annotation()
        assert isinstance(result, dict)

    def test_has_full_name_key(self):
        """Словарь должен содержать ключ 'full_name'."""
        result = get_user_full_name_annotation()
        assert "full_name" in result

    def test_full_name_is_concat_expression(self):
        """Значение должно быть экземпляром Concat."""
        result = get_user_full_name_annotation()
        assert isinstance(result["full_name"], Concat)

    def test_can_be_used_in_annotation(self, db, create_user):
        """Аннотация должна работать в annotate() на реальной модели User."""
        from django.contrib.auth.models import User

        create_user.first_name = "John"
        create_user.last_name = "Doe"
        create_user.save()

        result = (
            User.objects.filter(pk=create_user.pk)
            .annotate(**get_user_full_name_annotation())
            .values("id", "full_name")
            .first()
        )

        assert result is not None
        assert result["full_name"] == "John Doe"
